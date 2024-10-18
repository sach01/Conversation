# maramari_app/utils.py

from .models import UserProfile, TranslateSentence, SentencePair, Notification
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg

# Level-based batch sizes
LEVEL_BATCH_SIZES = {
    1: 50,   # Level 1: 50 sentences
    2: 100,  # Level 2: 100 sentences
    3: 150,  # Level 3: 150 sentences
    4: 200   # Level 4: 200 sentences
}

def get_batch_size_for_level(level):
    """Get the batch size based on the user's level."""
    return LEVEL_BATCH_SIZES.get(level, 50)  # Default to 50 if the level isn't found

def add_points_to_user(user, points):
    """Adds points to the user's profile and checks for level-up."""
    profile = user.profile
    profile.add_points(points)

def allocate_sentences_to_user(user):
    """
    Allocate a unique batch of sentence pairs to the user based on their level.
    Ensures that sentences are not already allocated to other users.
    """
    batch_size = get_batch_size_for_level(user.profile.level)

    # Get sentence pairs that have not been translated or allocated to this user
    already_translated_ids = TranslateSentence.objects.filter(user=user).values_list('sentence_pair_id', flat=True)
    unallocated_sentences = SentencePair.objects.exclude(id__in=already_translated_ids)

    # Limit to the batch size
    sentences_to_allocate = unallocated_sentences[:batch_size]

    # Allocate sentences for translation
    for sentence in sentences_to_allocate:
        TranslateSentence.objects.create(
            user=user,
            sentence_pair=sentence,
            dialect=user.profile.dialect
        )

def check_translation_completion(user):
    """
    Check if the user has completed all of their allocated translations.
    If so, unlock the next batch of translations.
    """
    incomplete_translations = TranslateSentence.objects.filter(user=user, is_translated=False)
    if not incomplete_translations.exists():
        allocate_sentences_to_user(user)  # Allocate the next batch

def handle_expired_allocations():
    """
    Check for expired allocations and reallocate them to other users if not translated in time.
    """
    expired_allocations = TranslateSentence.objects.filter(is_translated=False).filter(
        allocated_at__lt=timezone.now() - timedelta(days=7)
    )

    for expired_allocation in expired_allocations:
        # Notify the user about expired allocations
        Notification.objects.create(
            user=expired_allocation.user,
            message=f"The translation for '{expired_allocation.sentence_pair.english_sentence}' has expired."
        )

        # Delete the expired allocation to make the sentence available for others
        expired_allocation.delete()

def unlock_timed_out_translations():
    """Unlock any translations locked by a user for more than 10 minutes."""
    timed_out = timezone.now() - timedelta(minutes=10)
    TranslateSentence.objects.filter(
        locked_by__isnull=False,
        allocated_at__lt=timed_out
    ).update(locked_by=None)

def calculate_progress(user):
    """Calculate the user's progress in terms of completed tasks in the current batch."""
    total_allocations = TranslateSentence.objects.filter(user=user).count()
    completed_allocations = TranslateSentence.objects.filter(user=user, is_translated=True).count()

    if total_allocations > 0:
        progress_percentage = (completed_allocations / total_allocations) * 100
    else:
        progress_percentage = 0

    remaining_tasks = total_allocations - completed_allocations

    return progress_percentage, remaining_tasks

def send_notification(user, message):
    """Send a notification to the user."""
    Notification.objects.create(user=user, message=message)

from django.test import TestCase

# Create your tests here.
# maramari_app/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Language, Dialect, SentencePair, TranslateSentence
from .utils import allocate_sentences_to_user

User = get_user_model()

class AllocationTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create language and dialect
        self.language = Language.objects.create(name='English', code='EN')
        self.dialect = Dialect.objects.create(user=self.user, language=self.language, name='US English', region='United States')
        
        # Create UserProfile
        self.user.profile.dialect = self.dialect
        self.user.profile.save()
        
        # Create sentence pairs
        for i in range(1, 201):
            SentencePair.objects.create(
                english_sentence=f"Sentence {i} in English.",
                kiswahili_sentence=f"Sentensi {i} katika Kiswahili."
            )
    
    def test_allocate_sentences_to_user(self):
        allocate_sentences_to_user(self.user)
        allocations = TranslateSentence.objects.filter(user=self.user)
        self.assertEqual(allocations.count(), 50)  # Level 1 batch size is 50
        # Check uniqueness
        sentence_ids = allocations.values_list('sentence_pair_id', flat=True)
        self.assertEqual(len(sentence_ids), len(set(sentence_ids)))
    
    def test_translation_submission(self):
        allocate_sentences_to_user(self.user)
        allocation = TranslateSentence.objects.first()
        allocation.translation = "Translated sentence."
        allocation.is_translated = True
        allocation.save()
        self.assertTrue(allocation.is_translated)
    
    def test_handle_expired_allocations(self):
        allocate_sentences_to_user(self.user)
        allocation = TranslateSentence.objects.first()
        allocation.allocated_at = timezone.now() - timedelta(days=8)
        allocation.save()
        handle_expired_allocations()
        self.assertFalse(TranslateSentence.objects.filter(id=allocation.id).exists())

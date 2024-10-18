from django.db import models

# maramari_app/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Use email for login
    groups = models.ManyToManyField(Group, related_name='translation_app_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='translation_app_users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Set email as the username field for authentication
    REQUIRED_FIELDS = ['username']  # Keep username as an additional field

    def __str__(self):
        return self.email


# Language Model
class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="languages", null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

# Dialect Model
class Dialect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dialects", null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='dialects')
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language.name} - {self.name} - {self.region}"

# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dialect = models.ForeignKey(Dialect, on_delete=models.SET_NULL, null=True, related_name="user_profiles")
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    total_contributions = models.IntegerField(default=0)
    badges = models.ManyToManyField('Badge', blank=True)
    achievements = models.ManyToManyField('Achievement', blank=True)

    def __str__(self):
        return f"{self.user.username} - Level: {self.level}, Points: {self.points}"

    def add_points(self, points):
        """Add points and check for level-up."""
        self.points += points
        self.total_contributions += 1
        self.check_level_up()
        self.save()

    def check_level_up(self):
        """Check if the user qualifies for a new level."""
        levels = {1: 100, 2: 300, 3: 600, 4: 1000}
        new_level = self.level
        for level, points_required in sorted(levels.items()):
            if self.points >= points_required:
                new_level = level
        if new_level != self.level:
            self.level = new_level
            self.award_badges()
            self.award_achievements()

    def award_badges(self):
        """Award badges based on the user's level."""
        badges = {
            1: 'Bronze Contributor',
            2: 'Silver Contributor',
            3: 'Gold Contributor',
            4: 'Platinum Contributor'
        }
        badge_name = badges.get(self.level)
        if badge_name:
            badge, created = Badge.objects.get_or_create(name=badge_name)
            if created:
                badge.description = f"Earned by reaching level {self.level}"
                badge.points_required = LEVEL_BATCH_SIZES.get(self.level, 50)
                badge.save()
            self.badges.add(badge)

    def award_achievements(self):
        """Award achievements for specific milestones."""
        milestones = {
            10: 'First 10 Contributions',
            50: '50 Contributions',
            100: '100 Contributions'
        }
        achievement_name = milestones.get(self.total_contributions)
        if achievement_name:
            achievement, created = Achievement.objects.get_or_create(name=achievement_name)
            if created:
                achievement.description = f"Achieved after {self.total_contributions} contributions."
                achievement.save()
            if achievement not in self.achievements.all():
                self.achievements.add(achievement)
                Notification.objects.create(
                    user=self.user,
                    message=f"Congratulations! You've unlocked the achievement: {achievement.name}"
                )

# Badge Model
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()

    def __str__(self):
        return self.name

# Achievement Model
class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Achievement: {self.name}"

# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

# SentencePair Model
class SentencePair(models.Model):
    english_sentence = models.TextField()
    kiswahili_sentence = models.TextField()

    def __str__(self):
        return f"{self.english_sentence[:50]} - {self.kiswahili_sentence[:50]}"

# TranslateSentence Model
class TranslateSentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence_pair = models.ForeignKey(SentencePair, on_delete=models.CASCADE, related_name="translations")
    dialect = models.ForeignKey(Dialect, on_delete=models.CASCADE)
    translation = models.TextField(blank=True, null=True)
    allocated_at = models.DateTimeField(auto_now_add=True)
    locked_by = models.ForeignKey(User, null=True, blank=True, related_name='locked_translations', on_delete=models.SET_NULL)
    is_translated = models.BooleanField(default=False)
    time_started = models.DateTimeField(null=True, blank=True)
    time_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sentence_pair.english_sentence[:50]} - {self.translation[:50]}"

    def is_allocation_expired(self):
        """Check if the allocation has expired (e.g., after 7 days)."""
        expiration_time = self.allocated_at + timezone.timedelta(days=7)
        return timezone.now() > expiration_time

    def save(self, *args, **kwargs):
        if self.is_translated and not self.time_completed:
            self.time_completed = timezone.now()
        super().save(*args, **kwargs)

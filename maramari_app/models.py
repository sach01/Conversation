from django.db import models

# Create your models here.
from django.db import models

class SentencePair(models.Model):
    english_sentence = models.TextField()
    kiswahili_sentence = models.TextField()

    def __str__(self):
        return f"{self.english_sentence[:50]} - {self.kiswahili_sentence[:50]}"


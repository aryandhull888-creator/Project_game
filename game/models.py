from django.db import models

class Word(models.Model):
    text = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.text.upper()

from django.contrib.auth.models import User

class GameSession(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    word_to_guess = models.ForeignKey(Word, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)

    is_won = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    
    guess1 = models.CharField(max_length=5, blank=True, null=True)
    guess2 = models.CharField(max_length=5, blank=True, null=True)
    guess3 = models.CharField(max_length=5, blank=True, null=True)
    guess4 = models.CharField(max_length=5, blank=True, null=True)
    guess5 = models.CharField(max_length=5, blank=True, null=True)

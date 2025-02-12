from django.db import models

class GameScore(models.Model):
    user_score = models.IntegerField(default=0)
    computer_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_score} | Computer: {self.computer_score}"

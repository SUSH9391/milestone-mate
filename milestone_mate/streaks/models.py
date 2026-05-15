from django.db import models
from django.contrib.auth.models import User

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


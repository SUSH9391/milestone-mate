from django.db import models

# Create your models here.
class Streak(models.Model):
    name = models.CharField(max_length=255)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


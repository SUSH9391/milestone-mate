from django.db import models
from datetime import date

class Goal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('long_term', 'Long-Term'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    goal_type = models.CharField(
        max_length=10,
        choices=GOAL_TYPE_CHOICES,
        default='daily'
    )
    target_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='goal_attachments/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.goal_type == 'daily':
            self.target_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subgoal(models.Model):
    goal = models.ForeignKey(Goal, related_name='subgoals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
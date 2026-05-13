from django.db import models

# Create your models here.
class Goal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    target_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Subgoal(models.Model):
    goal = models.ForeignKey(Goal, related_name='subgoals', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
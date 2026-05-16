from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Goal
from .utils import sync_goal_to_google_calendar, delete_google_calendar_event

@receiver(post_save, sender=Goal)
def handle_goal_save(sender, instance, created, **kwargs):
    """
    Automatically syncs the goal to Google Calendar whenever it's saved.
    """
    # We avoid syncing if it's already being updated (to prevent recursion if we updated in utils)
    # But in utils we used .update() which doesn't trigger signals.
    sync_goal_to_google_calendar(instance)

@receiver(post_delete, sender=Goal)
def handle_goal_delete(sender, instance, **kwargs):
    """
    Automatically deletes the Google Calendar event when the goal is deleted.
    """
    delete_google_calendar_event(instance)

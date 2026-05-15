from datetime import date, timedelta
from goals.models import Goal
from .models import Streak

def update_streak(user, name="main_streak"):
    if not user.is_authenticated:
        return None

    streak, created = Streak.objects.get_or_create(
        user=user,
        name=name
    )

    today = date.today()
    yesterday = today - timedelta(days=1)

    completed_today = Goal.objects.filter(
        user=user,
        completed_at=today
    ).exists()

    # Determine if they missed a day
    # A streak is broken if the last update was before yesterday,
    # AND they haven't completed anything today.
    # Wait, if last_updated < yesterday, the streak is definitely broken regardless of today.
    # We will handle breaking the streak first.
    if streak.last_updated and streak.last_updated < yesterday:
        # If they haven't completed anything today, reset to 0.
        # If they HAVE completed something today, it resets to 1 (handled below).
        if not completed_today:
            streak.current_streak = 0
            # Don't update last_updated so we remember the last time they actually did something
            streak.save()
            return streak

    if completed_today:
        if streak.last_updated == today:
            # Already counted today, do nothing but ensure it's at least 1
            streak.current_streak = max(streak.current_streak, 1)
        elif streak.last_updated == yesterday:
            # Maintained streak
            streak.current_streak += 1
            streak.last_updated = today
        else:
            # Streak broke, start over at 1
            streak.current_streak = 1
            streak.last_updated = today
            
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.save()
        return streak

    # If not completed today, we just wait. 
    # The streak hasn't broken yet (they have until midnight).
    # No changes are saved unless we needed to break the streak above.
    return streak


def get_streak_data(user, name="main_streak"):
    if not user.is_authenticated:
        return {'current_streak': 0, 'longest_streak': 0, 'last_updated': None}

    streak = update_streak(user, name)

    return {
        'current_streak': streak.current_streak,
        'longest_streak': streak.longest_streak,
        'last_updated': streak.last_updated,
    }
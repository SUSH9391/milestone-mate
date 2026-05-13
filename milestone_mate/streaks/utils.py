from datetime import date, timedelta

from goals.models import Goal
from .models import Streak


def update_streak(name="global_streak"):

    streak, created = Streak.objects.get_or_create(
        name=name
    )

    today = date.today()
    yesterday = today - timedelta(days=1)

    completed_today = Goal.objects.filter(
        completed_at=today
    ).exists()


    if streak.last_updated == today:
        return streak

    if completed_today:

        if streak.last_updated == yesterday:
            streak.current_streak += 1

        else:
            streak.current_streak = 1

        if (
            streak.current_streak >
            streak.longest_streak
        ):
            streak.longest_streak = (
                streak.current_streak
            )

    else:
        streak.current_streak = 0

    streak.last_updated = today

    streak.save()

    return streak


def get_streak_data(name="global_streak"):

    streak = update_streak(name)

    return {
        'current_streak': streak.current_streak,
        'longest_streak': streak.longest_streak,
        'last_updated': streak.last_updated,
    }
from datetime import date, timedelta
from goals.models import Goal

def calculate_weekly_consistency(goals):
    today = date.today()
    week_ago = today - timedelta(days=7)
    recent_goals = goals.filter(target_date__gte=week_ago, target_date__lte=today)
    daily_goals = recent_goals.filter(goal_type='daily')
    completed_daily = daily_goals.filter(is_completed=True).count()
    return {
        'total_daily_goals': daily_goals.count(),
        'completed_daily_goals': completed_daily,
    }

def long_term_frequency(goals):
    long_term_goals = goals.filter(goal_type='long_term')
    total_long_term = long_term_goals.count()
    completed_long_term = long_term_goals.filter(is_completed=True).count()
    return {
        'total_long_term_goals': total_long_term,
        'completed_long_term_goals': completed_long_term,
    }

def long_term_completion_rate(goals):
    long_term_goals = goals.filter(goal_type='long_term')
    total_long_term = long_term_goals.count()
    completed_long_term = long_term_goals.filter(is_completed=True).count()
    if total_long_term == 0:
        return 0.0
    return completed_long_term / total_long_term
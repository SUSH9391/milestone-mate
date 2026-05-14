from django.shortcuts import render

from goals.models import Goal

from .utils import (
    calculate_weekly_consistency,
    long_term_frequency,
    long_term_completion_rate,
)


def dashboard(request):
    user_goals = Goal.objects.all()  # Replace with user-specific filtering if/when auth is added

    weekly_consistency = calculate_weekly_consistency(user_goals)
    long_term_freq = long_term_frequency(user_goals)
    completion_rate = long_term_completion_rate(user_goals)

    # Chart-ready values (encode as JSON-like Python lists/ints)
    # dashboard.html expects *_json variables.
    weekly_daily_labels = weekly_consistency.get('daily_labels', [])
    weekly_daily_completed = weekly_consistency.get('daily_completed_per_day', [])

    long_term_completed = long_term_freq.get('completed_long_term_goals', 0)
    long_term_total = long_term_freq.get('total_long_term_goals', 0)

    return render(
        request,
        'dashboard.html',
        {
            'weekly_consistency': weekly_consistency,
            'long_term_freq': long_term_freq,
            'completion_rate': completion_rate,
            'weekly_daily_labels_json': weekly_daily_labels,
            'weekly_daily_completed_json': weekly_daily_completed,
            'long_term_completed_json': long_term_completed,
            'long_term_total_json': long_term_total,
        },
    )


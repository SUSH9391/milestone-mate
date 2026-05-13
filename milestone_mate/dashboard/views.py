from django.shortcuts import render
from .utils import calculate_weekly_consistency, long_term_frequency, long_term_completion_rate
def dashboard(request):
    user_goals = Goal.objects.all()  # Replace with user-specific filtering if needed
    weekly_consistency = calculate_weekly_consistency(user_goals)
    long_term_freq = long_term_frequency(user_goals)
    completion_rate = long_term_completion_rate(user_goals)

    return render(request, 'dashboard.html', {
        'weekly_consistency': weekly_consistency,
        'long_term_freq': long_term_freq,
        'completion_rate': completion_rate,
    })
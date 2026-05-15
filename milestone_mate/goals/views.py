from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Goal, Subgoal
from .forms import GoalForm
from streaks.utils import get_streak_data
from datetime import date
from django.core.paginator import Paginator

from dashboard.utils import (
    calculate_weekly_consistency,
    long_term_frequency,
    long_term_completion_rate,
)


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')


@login_required
def home(request):
    streak_data = get_streak_data(request.user)

    user_goals = Goal.objects.filter(user=request.user)
    weekly_consistency = calculate_weekly_consistency(user_goals)
    long_term_freq = long_term_frequency(user_goals)
    completion_rate = long_term_completion_rate(user_goals)

    # Pre-encode chart data for safe inline JS usage
    weekly_labels = weekly_consistency.get('daily_labels', [])
    weekly_completed = weekly_consistency.get('daily_completed_per_day', [])

    context = {
        'streak_data': streak_data,
        'weekly_consistency': weekly_consistency,
        'long_term_freq': long_term_freq,
        'completion_rate': completion_rate,
        'weekly_daily_labels_json': __import__('json').dumps(weekly_labels),
        'weekly_daily_completed_json': __import__('json').dumps(weekly_completed),
        'long_term_completed_json': __import__('json').dumps(long_term_freq.get('completed_long_term_goals', 0)),
        'long_term_total_json': __import__('json').dumps(long_term_freq.get('total_long_term_goals', 0)),
    }

    return render(
        request,
        'home/home.html',
        context
    )


@login_required
def list_goals(request):
    goal_type = request.GET.get('type', None)
    goals = Goal.objects.filter(user=request.user, is_completed=False)
    
    if goal_type in ['daily', 'long_term']:
        goals = goals.filter(goal_type=goal_type)

    paginator = Paginator(goals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'goals/list_goals.html', {
        'goals': page_obj,  # Using goals instead of page_obj for template compatibility
        'page_obj': page_obj,
        'goal_type_filter': goal_type,
    })


@login_required
def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST, request.FILES)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            if goal.goal_type == 'long_term' and not goal.target_date:
                form.add_error('target_date', 'Please select a target date for long-term goals.')
            else:
                goal.save()
                return redirect('list_goals')
    else:
        form = GoalForm()
    return render(request, 'goals/create_goal.html', {'form': form})


@login_required
def create_subgoal(request, goal_id):
    if request.method != "POST":
        return JsonResponse(
            {'detail': 'Method not allowed'},
            status=405
        )

    goal = get_object_or_404(
        Goal,
        id=goal_id,
        user=request.user
    )

    title = request.POST.get("title")

    if title:
        Subgoal.objects.create(
            goal=goal,
            name=title
        )

    return redirect("list_goals")


@login_required
def delete_goal(request, goal_id):
    if request.method != "POST":
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    goal = get_object_or_404(
        Goal, 
        id=goal_id,
        user=request.user
    )
    goal.delete()
    return redirect("list_goals")


@login_required
def delete_subgoal(request, subgoal_id):
    if request.method != "POST":
        return JsonResponse(
            {'detail': 'Method not allowed'},
            status=405
        )

    subgoal = get_object_or_404(
        Subgoal,
        id=subgoal_id,
        goal__user=request.user
    )

    subgoal.delete()
    return redirect("list_goals")


@login_required
def toggle_goal(request, goal_id):
    if request.method != "POST":
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.is_completed = not goal.is_completed

    if goal.is_completed:
        goal.completed_at = date.today()
    else:   
        goal.completed_at = None

    goal.save(
        update_fields=[
            'is_completed',
            'completed_at'
        ]
    )
    return JsonResponse({'is_completed': goal.is_completed})


@login_required
def toggle_subgoal(request, subgoal_id):
    if request.method != "POST":
        return JsonResponse(
            {'detail': 'Method not allowed'},
            status=405
        )

    subgoal = get_object_or_404(
        Subgoal,
        id=subgoal_id,
        goal__user=request.user
    )

    subgoal.is_completed = (
        not subgoal.is_completed
    )

    subgoal.save(
        update_fields=['is_completed']
    )

    return JsonResponse({
        'is_completed':
            subgoal.is_completed
    })


@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    return render(request, 'goals/goal_des.html', {'goal': goal})

@login_required
def profile(request):
    user_goals = Goal.objects.filter(user=request.user)
    total_goals = user_goals.count()
    completed_goals = user_goals.filter(is_completed=True).count()
    
    streak_data = get_streak_data(request.user)
    
    context = {
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'streak_data': streak_data,
    }
    return render(request, 'goals/profile.html', context)

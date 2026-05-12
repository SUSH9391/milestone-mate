from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Goal, Subgoal


def home(request):
    return render(request, 'home/home.html')


def list_goals(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        target_date = request.POST.get("target_date")

        Goal.objects.create(
            name=title,
            description=description,
            target_date=target_date,
        )
        return redirect("list_goals")

    goals = Goal.objects.all()
    return render(
        request,
        'goals/list_goals.html',
        {'goals': goals},
    )
def create_subgoal(request, goal_id):

    if request.method != "POST":
        return JsonResponse(
            {'detail': 'Method not allowed'},
            status=405
        )

    goal = get_object_or_404(
        Goal,
        id=goal_id
    )

    title = request.POST.get("title")

    if title:
        Subgoal.objects.create(
            goal=goal,
            name=title
        )

    return redirect("list_goals")

def delete_goal(request, goal_id):
    if request.method != "POST":
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    goal = get_object_or_404(
        Goal, 
        id=goal_id
        )
    goal.delete()
    return redirect("list_goals")

def toggle_goal(request, goal_id):
    if request.method != "POST":
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    goal = get_object_or_404(Goal, id=goal_id)
    goal.is_completed = not goal.is_completed
    goal.save(update_fields=['is_completed'])
    return JsonResponse({'is_completed': goal.is_completed})

def toggle_subgoal(request, subgoal_id):

    if request.method != "POST":
        return JsonResponse(
            {'detail': 'Method not allowed'},
            status=405
        )

    subgoal = get_object_or_404(
        Subgoal,
        id=subgoal_id
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

def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    return render(request, 'goals/goal_des.html', {'goal': goal})


from django.shortcuts import render, redirect
from .models import Goal

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
            target_date=target_date
        )

        return redirect("list_goals")

    goals = Goal.objects.all()

    return render(
        request,
        'goals/list_goals.html',
        {'goals': goals}
    )
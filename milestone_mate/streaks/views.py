from django.shortcuts import render

from .utils import get_streak_data


def streak_dashboard(request):
    streak_data = get_streak_data()

    return render(
        request,
        'home/home.html',
        {
            'streak_data': streak_data,
        },
    )


def get_streak_data_view(request, name="global_streak"):
    # Convenience wrapper so URLconf can call a proper view.
    data = get_streak_data(name=name)
    return data


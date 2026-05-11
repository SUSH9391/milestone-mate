from .views import list_goals
from django.urls import path
from .views import home

urlpatterns = [
    path('', list_goals, name='list_goals'),
    path('', home, name='home'),
]
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('goals/', views.list_goals, name='list_goals'),
    path('goals/toggle/<int:goal_id>/', views.toggle_goal, name='toggle_goal'),
    path('goals/detail/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('goals/delete/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path(
    '<int:goal_id>/subgoal/create/',
    views.create_subgoal,
    name='create_subgoal'
),
path(
    'subgoal/toggle/<int:subgoal_id>/',
    views.toggle_subgoal,
    name='toggle_subgoal'
),
path(
    'subgoal/delete/<int:subgoal_id>/',
    views.delete_subgoal,
    name='delete_subgoal'
),
]


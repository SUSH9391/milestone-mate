from django.urls import path

from . import views

urlpatterns = [
    # Example: /streaks/global_streak/
    path('streaks/<str:name>/', views.get_streak_data_view, name='get_streak_data'),
    # Optional alias for convenience:
    path('streaks/', views.streak_dashboard, name='streak_dashboard'),
]





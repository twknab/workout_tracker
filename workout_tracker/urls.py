"""workout_tracker URL Configuration

Points our project to our workout application.
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include("apps.workout.urls")),
]

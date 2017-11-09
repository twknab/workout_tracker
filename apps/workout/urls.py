"""workout app URL Configuration

Our workout application URLs.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login), # index / login page
    url(r'^user/register$', views.register), # get register page / register user
    url(r'^user/login$', views.login), # logs in existing user
    url(r'^user/logout$', views.logout), # destroys user session
    url(r'^dashboard$', views.dashboard), # get dashboard
    url(r'^workout$', views.new_workout), # get workout page / add workout
    url(r'^workout/(?P<id>\d*)$', views.workout), # get workout / update workout
    url(r'^workout/(?P<id>\d*)/exercise$', views.exercise), # add exercise
    url(r'^workout/(?P<id>\d*)/complete$', views.complete_workout), # complete workout
    url(r'^workout/(?P<id>\d*)/edit$', views.edit_workout), # edit workout
    url(r'^workout/(?P<id>\d*)/delete$', views.delete_workout), # delete workout
    url(r'^workouts$', views.all_workouts), # get all workouts
    url(r'^legal/tos$', views.tos), # get terms of service
]

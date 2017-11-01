"""workout app URL Configuration

Our workout application URLs.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login), # index / login page
    url(r'^user/register$', views.register), # register page / registers user
    url(r'^user/login$', views.login), # logs in existing user
    url(r'^user/logout$', views.logout), # destroys user session
    url(r'^dashboard$', views.dashboard), # loads dashboard
    url(r'^workout$', views.workout), # workout page / submit workout
    url(r'^tables$', views.tables),
    url(r'^charts$', views.charts),
    url(r'^forms$', views.forms),
]

"""workout app URL Configuration

Our workout application URLs.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login), # index / login page
    url(r'^register$', views.register), # register page / registers user
    url(r'^login$', views.login), # logs in existing user
    url(r'^dashboard$', views.dashboard), # loads dashboard
    url(r'^tables$', views.tables),
    url(r'^charts$', views.charts),
    url(r'^forms$', views.forms),
    url(r'^logout$', views.logout), # destroys user session
]

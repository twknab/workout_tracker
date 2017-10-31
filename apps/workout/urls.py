"""workout app URL Configuration

Our workout application URLs.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^tables$', views.tables),
    url(r'^charts$', views.charts),
    url(r'^forms$', views.forms),
]

"""workout app URL Configuration

Our workout application URLs.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
]

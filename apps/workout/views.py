from django.shortcuts import render, redirect

def login(request):
    """Loads login."""

    if request.method == "GET":
        return render(request, "workout/index.html")

def register(request):
    """Register a user."""

    if request.method == "GET":
        return render(request, "workout/register.html")

def dashboard(request):
    """Loads dashboard."""

    return render(request, "workout/dashboard.html")

def tables(request):
    """Loads tables."""

    return render(request, "workout/tables.html")

def charts(request):
    """Loads charts."""

    return render(request, "workout/charts.html")

def forms(request):
    """Loads forms."""

    return render(request, "workout/forms.html")

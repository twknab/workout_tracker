from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    """Loads homepage."""

    return render(request, "workout/index.html")

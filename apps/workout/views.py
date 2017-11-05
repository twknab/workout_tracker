from django.shortcuts import render, redirect
from django.contrib import messages # access django's `messages` module.
from .models import User, Workout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def login(request):
    """If GET, load login page, if POST, login user."""

    if request.method == "GET":
        return render(request, "workout/index.html")

    if request.method == "POST":
        # Validate login data:
        validated = User.objects.login(**request.POST)
        try:
            # If errors, reload login page with errors:
            if len(validated["errors"]) > 0:
                print("User could not be logged in.")
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.error(request, error, extra_tags='login')
                # Reload login page:
                return redirect("/")
        except KeyError:
            # If validation successful, set session, and load dashboard based on user level:
            print("User passed validation and is logged in.")

            # Set session to validated User:
            request.session["user_id"] = validated["logged_in_user"].id

            # Fetch dashboard data and load appropriate dashboard page:
            return redirect("/dashboard")

def register(request):
    """If GET, load registration page; if POST, register user."""

    if request.method == "GET":
        return render(request, "workout/register.html")

    if request.method == "POST":
        # Validate registration data:
        validated = User.objects.register(**request.POST)
        # If errors, reload register page with errors:
        try:
            if len(validated["errors"]) > 0:
                print("User could not be registered.")
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.error(request, error, extra_tags='registration')
                # Reload register page:
                return redirect("/user/register")
        except KeyError:
            # If validation successful, set session and load dashboard based on user level:
            print("User passed validation and has been created.")
            # Set session to validated User:
            request.session["user_id"] = validated["logged_in_user"].id
            # Load Dashboard:
            return redirect('/dashboard')

def dashboard(request):
    """Loads dashboard."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Get recent workouts:
        recent_workouts = Workout.objects.all().order_by('-id')[:4]

        # Gather any page data:
        data = {
            'user': user,
            'recent_workouts': recent_workouts,
        }

        # Load dashboard with data:
        return render(request, "workout/dashboard.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def new_workout(request):
    """If GET, load new workout; if POST, submit new workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Gather any page data:
        data = {
            'user': user,
        }

        if request.method == "GET":
            # If get request, load `add workout` page with data:
            return render(request, "workout/add_workout.html", data)

        if request.method == "POST":
            print("$$$$$")
            print(request.POST)
            print("$$$$$")
            # Begin validation of a new workout:
            validated = Workout.objects.new(**request.POST)
            # If errors, reload register page with errors:
            try:
                if len(validated["errors"]) > 0:
                    print("Workout could not be created.")
                    # Loop through errors and Generate Django Message for each with custom level and tag:
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='workout')
                    # Reload workout page:
                    return redirect("/workout")
            except KeyError:
                # If validation successful, load newly created hike page:
                print("Workout passed validation and has been created.")

                id = str(validated['new_workout'].id)
                # Load workout:
                return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def workout(request, id):
    """If GET, load workout; if POST, update workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Gather any page data:
        data = {
            'user': user,
            'workout': Workout.objects.get(id=id),
        }

        if request.method == "GET":
            # If get request, load workout page with data:
            return render(request, "workout/workout.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def all_workouts(request):
    """Loads `View All` Workouts page."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        workout_list = Workout.objects.all().order_by('-id')

        page = request.GET.get('page', 1)

        paginator = Paginator(workout_list, 12)
        try:
            workouts = paginator.page(page)
        except PageNotAnInteger:
            workouts = paginator.page(1)
        except EmptyPage:
            workouts = paginator.page(paginator.num_pages)

        # Gather any page data:
        data = {
            'user': user,
            'workouts': workouts,
        }

        # Load dashboard with data:
        return render(request, "workout/all_workouts.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def logout(request):
    """Logs out current user."""

    try:
        # Deletes session:
        del request.session['user_id']
        # Adds success message:
        messages.success(request, "You have been logged out.", extra_tags='logout')

    except KeyError:
        pass

    # Return to index page:
    return redirect("/")

from django.db import models
import re # regex for email validation
import bcrypt # bcrypt for password encryption/decryption
from decimal import * # for decimal number purposes

class UserManager(models.Manager):
    """Additional instance method functions for `User`"""

    def register(self, **kwargs):
        """
        Validates and registers a new user.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of registration values from controller to be validated.

        Validations:
        - Username - Required; No fewer than 2 characters; letters only
        - Email - Required, Valid Format, Not Taken
        - Password - Required; Min 8 char, Matches Password Confirmation
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        #---------------#
        #-- USERNAME: --#
        #---------------#
        # Check if username is less than 2 characters:
        if len(kwargs["username"][0]) < 2:
            errors.append('Username is required and must be at least 2 characters long.')

        # Check if username contains letters, numbers and basic characters only:
        USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9!@#$%^&*()?]*$') # Create regex object
        # Test username against regex object:
        if not USERNAME_REGEX.match(kwargs["username"][0]):
            errors.append('Username must contain letters, numbers and basic characters only.')

        #---------------#
        #-- EXISTING: --#
        #---------------#
        # Check for existing User via username:
        if len(User.objects.filter(username=kwargs["username"][0])) > 0:
            errors.append('Username is already registered to another user.')

        #------------#
        #-- EMAIL: --#
        #------------#
        # Check if email field is empty:
        if len(kwargs["email"][0]) < 5:
            errors.append('Email field must be at least 5 characters.')

        # Else if email is greater than 5 characters:
        else:
            # Check if email is in valid format (using regex):
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
            if not EMAIL_REGEX.match(kwargs["email"][0]):
                errors.append('Email field is not a valid email format.')
            else:
                #---------------#
                #-- EXISTING: --#
                #---------------#
                # Check for existing User via email:
                if len(User.objects.filter(email=kwargs["email"][0])) > 0:
                    errors.append('Email address is already registered to another user.')

        #---------------#
        #-- PASSWORD: --#
        #---------------#
        # Check if password is less than 8 characters:
        if len(kwargs["password"][0]) < 8 or len(kwargs["password_confirmation"][0]) < 8:
            errors.append('Password fields are required and must be at least 8 characters.')
        else:
            # Check if password matches confirmation password:
            if kwargs["password"][0] != kwargs["password_confirmation"][0]:
                errors.append('Password and confirmation must match.')

        #-----------------#
        #-- TOS ACCEPT: --#
        #-----------------#
        # Check if TOS box is accepted:
        # Note: HTML5 required attribute is set, but just in case:
        if kwargs["tos_accept"][0] == "on":
            kwargs["tos_accept"][0] = True
        else:
            errors.append("Terms of service must be accepted.")

        # Check for validation errors:
        # If none, hash password, create user and send new user back:
        if len(errors) == 0:
            kwargs["password"][0] = bcrypt.hashpw((kwargs["password"][0]).encode(), bcrypt.gensalt(14))
            # Create new validated User:
            validated_user = {
                "logged_in_user": User(username=kwargs["username"][0], email=kwargs["email"][0], password=kwargs["password"][0], tos_accept=kwargs["tos_accept"][0]),
            }
            # Save new User:
            validated_user["logged_in_user"].save()
            # Return created User:
            return validated_user
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

    def login(self, **kwargs):
        """
        Validates and logs in a new user.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of login values from controller.

        Validations:
        - All fields required.
        - Existing User is found.
        - Password matches User's stored password.
        """

        # Create empty errors list:
        errors = []

        #------------------#
        #--- ALL FIELDS ---#
        #------------------#
        # Check that all fields are required:
        if len(kwargs["username"][0]) < 1 or len(kwargs["password"][0]) < 1:
            errors.append('All fields are required.')
        else:
            #------------------#
            #---- EXISTING ----#
            #------------------#
            # Look for existing User to login by username:
            try:
                logged_in_user = User.objects.get(username=kwargs["username"][0])

                #------------------#
                #---- PASSWORD ----#
                #------------------#
                # Compare passwords with bcrypt:
                # Note: We must encode both prior to testing
                try:

                    password = kwargs["password"][0].encode()
                    hashed = logged_in_user.password.encode()

                    if not (bcrypt.checkpw(password, hashed)):
                        print("ERROR: PASSWORD IS INCORRECT")
                        # Note: We send back a general error that does not specify what credential is invalid: this is for security purposes and is admittedly a slight inconvenience to our user, but makes it harder to gather information from the server during brute for attempts
                        errors.append("Username or password is incorrect.")

                except ValueError:
                    # If user's stored password is unable to be used by bcrypt (likely b/c password is not hashed):
                    errors.append('This user is corrupt. Please contact the administrator.')

            # If existing User is not found:
            except User.DoesNotExist:
                print("ERROR: USERNAME IS INVALID")
                # Note: See password validation note above:
                errors.append('Username or password is incorrect.')

        # If no validation errors, return logged in user:
        if len(errors) == 0:
            # Prepare data for controller:
            validated_user = {
                "logged_in_user": logged_in_user,
            }
            # Send back validated logged in User:
            return validated_user
        # Else, if validation fails print errors and return errors to controller:
        else:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

class WorkoutManager(models.Manager):
    """Additional instance method functions for `Workout`"""

    def new(self, **kwargs):
        """
        Validates and registers a new workout.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of workout values from controller to be validated.

        Validations:
        - Name - Required; No fewer than 2 characters; letters, basic characters, numbers only
        - Description - Required; letters, basic characters, numbers only
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        #-----------#
        #-- NAME: --#
        #-----------#
        # Check if name is less than 2 characters:
        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        # Check if name contains letters, numbers and basic characters only:
        '''
        Note: The following regex pattern matches for strings which start or do not start with spaces, whom contain letters, numbers and some basic character sequences, followed by either more spaces or more characters. This prevents empty string submissions.
        '''
        WORKOUT_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        # Test name against regex object:
        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        #------------------#
        #-- DESCRIPTION: --#
        #------------------#
        # Check if description is less than 2 characters:
        if len(kwargs["description"]) < 2:
            errors.append('Description is required and must be at least 2 characters long.')

        # Check if description contains letters, numbers and basic characters only:
        # Test description against regex object (we'll just use WORKOUT_REGEX again since the pattern has not changed):
        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Description must contain letters, numbers and basic characters only.')

        # Check for validation errors:
        # If none, create workout and return new workout:
        if len(errors) == 0:
            # Create new validated workout:
            validated_workout = {
                "workout": Workout(name=kwargs["name"], description=kwargs["description"], user=kwargs["user"]),
            }
            # Save new Workout:
            validated_workout["workout"].save()
            # Return created Workout:
            return validated_workout
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

    def update(self, **kwargs):
        """
        Validates and updates a workout.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of workout values from controller to be validated.

        Validations:
        - Name - Required; No fewer than 2 characters; letters, basic characters, numbers only
        - Description - Required; letters, basic characters, numbers only

        Developer Note:
        - This section utilizes essentially the exact same validations as the `new()` method above (in this same WorkoutManager class). However, in this particular case, we're updating a record rather than creating one. At a later point, it might be good to refactor this section/these validations.
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        #-----------#
        #-- NAME: --#
        #-----------#
        # Check if name is less than 2 characters:
        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        # Check if name contains letters, numbers and basic characters only:
        '''
        Note: The following regex pattern matches for strings which start or do not start with spaces, whom contain letters, numbers and some basic character sequences, followed by either more spaces or more characters. This prevents empty string submissions.
        '''
        WORKOUT_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        # Test name against regex object:
        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        #------------------#
        #-- DESCRIPTION: --#
        #------------------#
        # Check if description is less than 2 characters:
        if len(kwargs["description"]) < 2:
            errors.append('Description is required and must be at least 2 characters long.')

        # Check if description contains letters, numbers and basic characters only:
        # Test description against regex object (we'll just use WORKOUT_REGEX again since the pattern has not changed):
        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Description must contain letters, numbers and basic characters only.')

        # Check for validation errors:
        # If none, create workout and return new workout:
        if len(errors) == 0:

            # Update workout:
            workout = Workout.objects.filter(id=kwargs['workout_id']).update(name=kwargs['name'], description=kwargs["description"])

            # Return updated Workout:
            updated_workout = {
                "updated_workout": workout
            }
            return updated_workout
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

class ExerciseManager(models.Manager):
    """Additional instance method functions for `Exercise`"""

    def new(self, **kwargs):
        """
        Validates and registers a new exercise.

        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of exercise values from controller to be validated.

        Validations:
        - Name - Required; No fewer than 2 characters; letters, basic characters, numbers only
        - Weight (lbs) - Required; Numbers only, Decimals allowed.
        - Repetitions - Required; Numbers only, no Decimals.
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        #---------------#
        #-- REQUIRED: --#
        #---------------#
        # Check if all fields are present:
        if not kwargs['name'] or not kwargs['weight'] or not kwargs['repetitions']:
            errors.append('All fields are required.')

        #-----------#
        #-- NAME: --#
        #-----------#
        # Check if name is less than 2 characters:
        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        # Check if name contains letters, numbers and basic characters only:
        '''
        Note: The following regex pattern matches for strings which start or do not start with spaces, whom contain letters, numbers and some basic character sequences, followed by either more spaces or more characters. This prevents empty string submissions.
        '''
        EXERCISE_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        # Test name against regex object:
        if not EXERCISE_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        #---------------------------#
        #-- WEIGHT & REPETITIONS: --#
        #---------------------------#
        # Try converting weight and repetitions to floating numbers, rounded to tenth place:
        try:
            kwargs["weight"] = round(float(kwargs["weight"]), 1)
            kwargs["repetitions"] = round(float(kwargs["repetitions"]), 1)

            # Ensure weight and repetitions is a positive number:
            if (kwargs["weight"] < 0) or (kwargs["repetitions"] < 0):
                errors.append('Weight and repetitions must be a positive number.')

            # Ensure repetitions is a positive number:
            # if (kwargs["repetitions"] < 0):
            #     errors.append('Weight cannot be a negative number.')

        except ValueError:
            # If value error, send error:
            errors.append('Weight and repetitions must be a positive number only, containing at most one decimal place.')


        # Check for validation errors:
        # If none, create exercise and return created exercise:
        if len(errors) == 0:
            # Create new validated exercise:
            validated_exercise = {
                "exercise": Exercise(name=kwargs["name"], weight=kwargs["weight"], repetitions=kwargs["repetitions"], workout=kwargs["workout"]),
            }
            # Save new Workout:
            validated_exercise["exercise"].save()
            # Return created Workout:
            return validated_exercise
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

class User(models.Model):
    """Creates instances of `User`."""

    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=22)
    tos_accept = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    level_name = models.CharField(max_length=15, default="Newbie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # Adds additional instance methods to `User`

class Workout(models.Model):
    """Creates instances of `Workout`."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()

class Exercise(models.Model):
    """Creates instances of `Exercise`."""

    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=999, decimal_places=1)
    repetitions = models.DecimalField(max_digits=999, decimal_places=1)
    category = models.CharField(max_length=50, default="Strength Training") # Add more categories in the future: ['Strength Training', 'Endurance Training', 'Balance', 'Flexibility']
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExerciseManager()

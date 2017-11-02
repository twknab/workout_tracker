from django.db import models
import re # regex for email validation
import bcrypt # bcrypt for password encryption/decryption

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
            print("NEW PASSWORD:", kwargs["password"][0])
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
        if len(kwargs["name"][0]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        # Check if name contains letters, numbers and basic characters only:
        '''
        Note: The following regex pattern matches for strings which start or do not start with spaces, whom contain letters, numbers and some basic character sequences, followed by either more spaces or more characters. This prevents empty string submissions.
        '''
        WORKOUT_REGEX = re.compile(r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()\]\[~`]+)*\s*$')

        # Test name against regex object:
        print("THIS IS THE WORKOUT REGEX TEST:")
        print(kwargs["name"][0])
        print(WORKOUT_REGEX.match(kwargs["name"][0]))
        print("$$$$$$$$$$$$$")
        if not WORKOUT_REGEX.match(kwargs["name"][0]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        #------------------#
        #-- DESCRIPTION: --#
        #------------------#
        # Check if description is less than 2 characters:
        if len(kwargs["description"][0]) < 2:
            errors.append('Description is required and must be at least 2 characters long.')

        # Check if description contains letters, numbers and basic characters only:
        # Test description against regex object (we'll just use WORKOUT_REGEX again since the pattern has not changed):
        if not WORKOUT_REGEX.match(kwargs["description"][0]):
            errors.append('Description must contain letters, numbers and basic characters only.')

        # Check for validation errors:
        # If none, create workout and load workout page:
        if len(errors) == 0:
            # Create new validated workout:
            validated_workout = {
                "new_workout": Workout(name=kwargs["name"][0], description=kwargs["description"][0]),
            }
            # Save new Workout:
            validated_workout["new_workout"].save()
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


    # def update_profile(self, **kwargs):
    #     """
    #     Updates a User's information.
    #
    #     Parameters:
    #     - `self` - Instance to whom this method belongs.
    #     - `**kwargs` - Dictionary object of updated information from controller.
    #
    #     Validations:
    #     - First Name / Last Name - Required; No fewer than 2 characters; letters only
    #     - Email - Required, Valid Format, Not Taken
    #     """
    #
    #     errors = [] # empty err object
    #
    #     #------------------------#
    #     #-- FIRST / LAST NAME: --#
    #     #------------------------#
    #     # Check if fields are empty:
    #     if len(kwargs["first_name"]) < 2 or len(kwargs["last_name"]) < 2:
    #         errors.append("First and last name required and must be at least 2 characters.")
    #
    #     # Check if first_name or last_name contains letters only:
    #     alphachar_regex = re.compile(r'^[a-zA-Z]*$') # Create regex object
    #     # Test first_name and last_name against regex object:
    #     if not alphachar_regex.match(kwargs["first_name"]) or not alphachar_regex.match(kwargs["last_name"]):
    #         errors.append('First and last name must be letters only.')
    #
    #     #------------#
    #     #-- EMAIL: --#
    #     #------------#
    #     # Ensure that email is at least 5 characters:
    #     if len(kwargs["email"]) < 5:
    #         errors.append("Email is required and must be at least 5 characters.")
    #
    #     # Check if email submitted is different than current email on record:
    #     if User.objects.get(id=kwargs["user_id"]).email != kwargs["email"]:
    #         # Check if email field is empty:
    #         if len(kwargs["email"]) < 5:
    #             errors.append('Email field must be at least 5 characters.')
    #
    #         # Else if email is greater than 5 characters:
    #         else:
    #             # Check if email is in valid format (using regex):
    #             email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
    #             if not email_regex.match(kwargs["email"]):
    #                 errors.append('Email format is invalid.')
    #             else:
    #                 try:
    #                     # If email has not changed, pass, otherwise check if already registered:
    #                     if User.objects.get(id=kwargs["edit_user_id"]).email == kwargs["email"]:
    #                         pass
    #
    #                     else:
    #                         #---------------#
    #                         #-- EXISTING: --#
    #                         #---------------#
    #                         # Check for existing User via email:
    #                         if len(User.objects.filter(email=kwargs["email"])) > 0:
    #                             errors.append('Email address already registered.')
    #                 except KeyError:
    #                     # If email has not changed, pass, otherwise check if already registered:
    #                     if User.objects.get(id=kwargs["user_id"]).email == kwargs["email"]:
    #                         pass
    #                     else:
    #                         #---------------#
    #                         #-- EXISTING: --#
    #                         #---------------#
    #                         # Check for existing User via email:
    #                         if len(User.objects.filter(email=kwargs["email"])) > 0:
    #                             errors.append('Email address already registered.')
    #
    #
    #     # Check for validation errors:
    #     # If none, update information for user:
    #     if len(errors) == 0:
    #         print "User profile data update passed validation..."
    #
    #         # Updating user:
    #         """
    #         The three scenarios:
    #         1. Normal User Updating their profile
    #         2. Admin User Updating their profile
    #         3. Admin User Updating Normal User profile (includes "edit_user_id")
    #         """
    #
    #         # If user is not admin, simply update user profile:
    #         if User.objects.get(id=kwargs["user_id"]).user_level == 0:
    #             User.objects.filter(id=kwargs["user_id"]).update(first_name=kwargs["first_name"], last_name=kwargs["last_name"], email=kwargs["email"])
    #             print "User information updated."
    #             # Return updated user:
    #             return User.objects.get(id=kwargs["user_id"])
    #
    #
    #         # If user is admin, check if this is a self profile update, or updating another user:
    #         if User.objects.get(id=kwargs["user_id"]).user_level == 1:
    #             # If edit_user_id exists, this is an admin edit to another user:
    #             if "edit_user_id" in kwargs:
    #                 print "Admin user update detected..."
    #                 # Update user by `edit_user_id`, including user level:
    #                 User.objects.filter(id=kwargs["edit_user_id"]).update(first_name=kwargs["first_name"], last_name=kwargs["last_name"], email=kwargs["email"], user_level=kwargs["user_level"])
    #                 # Return user whom was edited:
    #                 return User.objects.get(id=kwargs["edit_user_id"])
    #             else:
    #                 # Else if edit_user_id does not exist, this is an admin self-profile change:
    #                 print "Admin profile update detected..."
    #                 # Update user by `user_id`
    #                 User.objects.filter(id=kwargs["user_id"]).update(first_name=kwargs["first_name"], last_name=kwargs["last_name"], email=kwargs["email"])
    #                 return User.objects.get(id=kwargs["user_id"])
    #
    #
    #     else:
    #         # Else, if validation fails, print errors to console and return errors object:
    #         print "Errors validating User registration."
    #         for error in errors:
    #             print "Validation Error: ", error
    #         # Prepare data for controller:
    #         errors = {
    #             "errors": errors,
    #         }
    #         return errors

    # def update_password(self, **kwargs):
    #     """
    #     Updates a User's password.
    #
    #     Parameters:
    #     - `self` - Instance to whom this method belongs.
    #     - `**kwargs` - Dictionary object containing new password from controller.
    #
    #     Validations:
    #     - Password - Required; Min 8 char, Matches Password Confirmation
    #     """
    #
    #     errors = [] # empty errors object
    #
    #     #---------------#
    #     #-- PASSWORD: --#
    #     #---------------#
    #     # Check if password is less than 8 characters:
    #     if len(kwargs["password"]) < 8:
    #         errors.append('Password fields are required and must be at least 8 characters.')
    #     else:
    #         # Check if password matches confirmation password:
    #         if kwargs["password"] != kwargs["confirm_pwd"]:
    #             errors.append('Password and confirmation password must match.')
    #
    #     # Check for validation errors:
    #     # If none, hash password, create user and send new user back:
    #     if len(errors) == 0:
    #
    #         """
    #         Three Scenarios:
    #         1. User updating their own password.
    #         2. Admin updating their own password.
    #         3. Admin updating a normal user's password.
    #         """
    #
    #         # Check if admin is updating another user's password:
    #         if "edit_user_id" in kwargs:
    #             print "Admin password update for normal user detected..."
    #             # Update password for user with ID as `edit_user_id`:
    #             print "Password validated...hashing..."
    #             User.objects.filter(id=kwargs["edit_user_id"]).update(password=bcrypt.hashpw(kwargs["password"].encode(), bcrypt.gensalt(14)))
    #             print "Password hashed..."
    #             # Return created User:
    #             return User.objects.filter(id=kwargs["edit_user_id"])
    #         else:
    #             print "Profile password update detected..."
    #             print "Password validated...hashing..."
    #             User.objects.filter(id=kwargs["user_id"]).update(password=bcrypt.hashpw(kwargs["password"].encode(), bcrypt.gensalt(14)))
    #             print "Password hashed..."
    #             # Return created User:
    #             return User.objects.filter(id=kwargs["user_id"])
    #     else:
    #         # Else, if validation fails, print errors to console and return errors object:
    #         print "Errors validating password update."
    #         for error in errors:
    #             print "Validation Error: ", error
    #         # Prepare data for controller:
    #         errors = {
    #             "errors": errors,
    #         }
    #         return errors

    # def update_profile_description(self, **kwargs):
    #     """
    #     Updates a User's description.
    #
    #     Parameters:
    #     - `self` - Instance to whom this method belongs.
    #     - `**kwargs` - Dictionary object containing new password from controller.
    #
    #     Validations:
    #     - Description - Less than 1000 characters. Not required.
    #     """
    #
    #     errors = [] # empty errors object
    #
    #     #------------------#
    #     #-- DESCRIPTION: --#
    #     #------------------#
    #     # Check if description less than 500 characters:
    #     if len(kwargs["description"]) > 500:
    #         errors.append('Description must be less than 500 characaters.')
    #
    #     # Check for validation errors, if none, update description:
    #     if len(errors) == 0:
    #         print "Description validated..."
    #         User.objects.filter(id=kwargs["user_id"]).update(description=kwargs["description"])
    #         # Return created User:
    #         return User.objects.filter(id=kwargs["user_id"])
    #     else:
    #         # Else, if validation fails, print errors to console and return errors object:
    #         print "Errors validating description."
    #         for error in errors:
    #             print "Validation Error: ", error
    #         # Prepare data for controller:
    #         errors = {
    #             "errors": errors,
    #         }
    #         return errors

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()

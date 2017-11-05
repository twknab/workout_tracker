# About

This application is designed to help in logging workouts.

# Features
- User login and registration.
- Add new workout feature.
- View all workouts feature.
- View individual workouts feature.

# Where I left Off:
Basically the USER ID you're sending to your model from your hidden field, is not being accepted by Django's model association. Refresh yourself on django model associations (one to many), and make sure you're setup correctly.

### Dugout Features (next up):
- Link workouts to User model -- update queries in views.py to get only workouts for USER -- right now they're getting ALL workouts for ALL users
- Add exercise feature.
- Complete workout feature.
- Get search box to work.

### Fix:
- Red slivers on input fields (upper left and right corners)

### Feature Upgrades to Build:
- Add notes to a workout.

- Add `Showing 31 to 40 of 57 records` to `View Workouts` page.

- Add workout stopwatch that records workout time.

- Make clicking on Avatar/Name on menu load User Profile page, where user can view personal details and or edit them (including password).

- Add strong password authentication.

- Make `+ Workout` on navigation open Modal window, rather than a separate view file.

- "Leveling Up" of status AND avatar, depending upon how many completed workouts exist. Presently, "Newbie" is first level. After 5 workouts, change it to "Novice" and so forth -- build a handful of different levels. This is a fun easter-egg feature/cool discovery. (Think of some reward system whereby a user increases in level based upon frequency of workouts, and decreases in level based upon lack of workout frequency)

- "Leveling Down" of status and avatar if X number of days since last workout.

- Add workout categories and other form types for other types of activities and workout records.


**OR**

- User's avatars upgrade along with their status (see downloaded .AI file for a set of avatar images that could be used for various levels)

# About

This application is designed to help in logging workouts.

# Features
- Register new users.
- Login existing users.
- Add a new workout.
- Add exercises to a workout.
- Delete an exercise (for incomplete workouts only).
- Complete a workout.
- View workout.
- Edit a workout.
- Delete a workout.
- View all past workouts.

### Dugout Feature (next up):
- Allow other types of workouts.
- Edit exercise feature.

- Search box capable of searching these fields:
  - workout: `name`, `description`
  - exercise: `name`, `weight`, `repetitions`
  - use a query + a view + django pagination?

### Wishlist / Feature Upgrades:
- Checkbox for "Failure" so user can check if they failed on that set.

- Rest timer (that can be manually set, but allows for rest times between strength training routines)

- Be able to delete Workouts

- Search box.

- Edit Exercise Feature

- Make nice logo homepage image inspired from fav ico.

- Add workout stats for each workout (total volume lifted, total # of reps).

- Add workout stats for the dashboard (total volume lifted, total # of reps).

- Add categories to workout and update forms so other workouts than just strength training may be added. Here's a list: ['Strength Training', 'Endurance Training', 'Balance', 'Flexibility'] or activities like ['Biking', 'Run', 'Walk', 'Hiking']

- Add notes to a workout.

- Add `Showing 31 to 40 of 57 records` to `View Workouts` page.

- Add workout stopwatch that records workout time.

- Make clicking on Avatar/Name on menu load User Profile page, where user can view personal details and or edit them (including password). Allow user to be able to delete their own profile.

- Add strong password authentication.

- Addt'l Security feature: Prune off the password hash from any user object that is passed to the front end (make sure the bcrypt hash is 100% unavailable client-side).

- Make `+ Workout` on navigation open Modal window, rather than a separate view file.

- "Leveling Up" of status AND avatar, depending upon how many completed workouts exist. Presently, "Newbie" is first level. After 5 workouts, change it to "Novice" and so forth -- build a handful of different levels. This is a fun easter-egg feature/cool discovery. (Think of some reward system whereby a user increases in level based upon frequency of workouts, and decreases in level based upon lack of workout frequency).

- "Leveling Down" of status and avatar if X number of days since last workout.

#### Change Log:
- 12/07/17 - Changed view all workouts page to a table.

# About
- [About](#about)
  - [Technologies](#technologies)
  - [Screenshots](#screenshots)
  - [Features](#features)
  - [Known Bugs](#known-bugs)
    - [Dugout Feature (next up)](#dugout-feature-next-up)
    - [Wishlist / Feature Upgrades](#wishlist--feature-upgrades)
      - [Change Log](#change-log)

FitnessTracker is a Python & Django CRUD MVC RESTful application that allows users to track strength training workouts. Users can add exercises and create routines on the fly, logging their activity.

## Technologies

- Python
- Django
- Bootstrap

## Screenshots

*1. Login*
![login](https://user-images.githubusercontent.com/20636750/108618177-c460c480-73d0-11eb-973a-0e502665f8c1.png)

*2. Register New User*
![signup](https://user-images.githubusercontent.com/20636750/108618180-c62a8800-73d0-11eb-8fe0-e3f9aa4ea6d2.png)

*3. Dashboard*
![dashboard](https://user-images.githubusercontent.com/20636750/108618181-c6c31e80-73d0-11eb-9c2e-82e485edf477.png)

*4. Add Workout*
![add-workout](https://user-images.githubusercontent.com/20636750/108618182-c75bb500-73d0-11eb-9724-e0e5dc5eb058.png)

*5. Workout No Exercises*
![workout-no-exercises-added](https://user-images.githubusercontent.com/20636750/108618183-c75bb500-73d0-11eb-9c94-2131160138e8.png)

*6. Edit Workout*
![edit-workout](https://user-images.githubusercontent.com/20636750/108618184-c7f44b80-73d0-11eb-9d8a-99f5b6cc05fa.png)

*7. View Workout*
![workout](https://user-images.githubusercontent.com/20636750/108618185-c7f44b80-73d0-11eb-8f73-36dd795d7768.png)

*8. Workout Completion Summary*
![end-workout-summary](https://user-images.githubusercontent.com/20636750/108618186-c88ce200-73d0-11eb-8786-0f58229588cc.png)

*9. View All Logged Workouts*
![view-all-workouts](https://user-images.githubusercontent.com/20636750/108618187-c88ce200-73d0-11eb-8906-9159b19da426.png)

## Features

- Register new users
- Login existing users
- Add a new workout
- Add exercises to a workout
- Delete an exercise (for incomplete workouts only)
- Complete a workout
- View workout
- Edit a workout
- Delete a workout
- View all past workouts

## Known Bugs

There is a bug where if the password is too long, the salted conversion can go beyond the allowed character count for the object model (e.g, salted password is longer than the text length allowed)

### Dugout Feature (next up)

- Allow other types of workouts.
- Edit exercise feature.

- Search box capable of searching these fields:
  - workout: `name`, `description`
  - exercise: `name`, `weight`, `repetitions`
  - use a query + a view + django pagination?

### Wishlist / Feature Upgrades

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

#### Change Log

- 12/07/17 - Changed view all workouts page to a table.

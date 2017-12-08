/*
This file assists in adding exercises to the DOM when viewing individual workouts.
*/
$( document ).ready(function() {

  $( '#end-workout' ).click(function() {
    return confirm("Are you sure you want to end your workout?");
  });

  $( '#delete-exercise' ).click(function() {
    return confirm("Are you sure you want to delete this exercise?");
  });

  $( '#delete-workout' ).click(function() {
    return confirm("Are you sure you want to delete this workout? This cannot be undone.");
  });

});

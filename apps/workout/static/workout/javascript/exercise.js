/*
This file assists in adding exercises to the DOM when viewing individual workouts.
*/
$( document ).ready(function() {

  $( '#end-workout' ).click(function() {
    console.log("CLICKED")
    return confirm("Are you sure you want to end your workout?");
  });

});

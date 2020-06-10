document.addEventListener('DOMContentLoaded', () => {

  var signup = document.getElementById('signup');
  var questions = document.getElementById('questions');
  var signup_buttons = document.querySelectorAll(".signup_buttons");

  // Don't show the signup screen until the user has stated she asked for a
  // recommendation (prevent students from doing the form without asking me first)
  // Also allow anyone to browse the questionnaire before going further
  signup.style.display = "none";
  questions.style.display = "none";

  // User indicated by clicking button that she has asked - show signup form
  asked.onclick = function(){
    signup.style.display = "block";
    questions.style.display = "none";
    asked.style.display = "none";
    browse.style.display = "inline"
  }

  // User just wants to see the questionnaire
  browse.onclick = function(){
    signup.style.display = "none";
    questions.style.display = "block";
    browse.style.display = "none";
    asked.style.display = "inline";
  }

  login.onclick = function(){
    document.location.href = "/users/login";
  }

  if (window.innerWidth <= 600){
    signup_buttons.forEach(x => x.classList.add("btn-block"));
  }

});

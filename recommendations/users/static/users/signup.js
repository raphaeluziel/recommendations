document.addEventListener('DOMContentLoaded', () => {

  var signup = document.getElementById('signup');
  questions = document.getElementById('questions');

  signup.style.display = "none";
  questions.style.display = "none";

  asked.onclick = function(){
    signup.style.display = "block";
    questions.style.display = "none";
  }

  browse.onclick = function(){
    signup.style.display = "none";
    questions.style.display = "block";
  }

  login.onclick = function(){
    document.location.href = "/users/login";

  }

});

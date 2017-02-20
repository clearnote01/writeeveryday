var loginForm = document.getElementById('loginScreen')
var signupForm = document.getElementById('signupScreen')
var openLogin = document.getElementById('openLogin')
var openSignup = document.getElementById('openSignup')

openLogin.addEventListener('click', function() {
  signupForm.style.display = "none";
  loginForm.style.display = "block";
});
  
openSignup.addEventListener('click', function() {
  loginForm.style.display = "none";
  signupForm.style.display = "block";
});
  


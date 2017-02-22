var loginFormScreen = document.getElementById('loginScreen')
var loginForm = document.getElementById('login')
var signupForm = document.getElementById('signup')
var signupFormScreen = document.getElementById('signupScreen')
var openLogin = document.getElementById('openLogin')
var openSignup = document.getElementById('openSignup')
var errorMsgBox = document.getElementsByClassName('flash-error')

function clearErrorMsgBox() {
  for ( let i=0; i < errorMsgBox.length; i++) {
    if(errorMsgBox[i]) {
      errorMsgBox[i].innerText = "";
    }
  }
}
openLogin.addEventListener('click', function() {
  signupFormScreen.style.display = "none";
  loginFormScreen.style.display = "block";
  clearErrorMsgBox()
});
  
openSignup.addEventListener('click', function() {
  loginFormScreen.style.display = "none";
  signupFormScreen.style.display = "block";
  clearErrorMsgBox()
});

loginForm.addEventListener('submit', function() {
  console.log('Form is submitted');
});
  
signupForm.addEventListener('submit', function() {
  console.log('Form is submitted');
  // Authenticate form before submission
  pass1 = this.password.innerText;
  pass2 = this.password_C.innerText;
  console.log(pass1, pass2);
  if (pass1 === pass2) {
    return false;
  }
  else {
    console.log('Pass mismatch');
    return false;
  }
}, false);


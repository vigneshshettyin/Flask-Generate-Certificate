var myInput = document.getElementById("psw");
var myinput2 = document.getElementById("psw2");
document.getElementById('registerBtn').disabled = true;
  var letter = document.getElementById("letter");
  var capital = document.getElementById("capital");
  var number = document.getElementById("number");
  var length = document.getElementById("length");
  var passwordmatch = document.getElementById("passwordmatch");
  console.log(passwordmatch)
  // When the user clicks on the password field, show the message box
  myInput.onfocus = function() {
    document.getElementById("message").style.visibility = "visible";
  }
  
  // When the user clicks outside of the password field, hide the message box
  myInput.onblur = function() {
    document.getElementById("message").style.visibility = "hidden";
  }

  

  // for confirm password
  
 // When the user clicks on the password field, show the message box
 myinput2.onfocus = function() {
  document.getElementById("message2").style.visibility = "visible";
}

// When the user clicks outside of the password field, hide the message box
myinput2.onblur = function() {
  document.getElementById("message2").style.visibility = "hidden";
}

  
  // When the user starts to type something inside the password field
  myInput.onkeyup = function() {
    document.getElementById('registerBtn').disabled = true;
    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    if(myInput.value.match(lowerCaseLetters)) {  
      letter.classList.remove("invalid");
      letter.classList.add("valid");
    } else {
      letter.classList.remove("valid");
      letter.classList.add("invalid");
    }
    
    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if(myInput.value.match(upperCaseLetters)) {  
      capital.classList.remove("invalid");
      capital.classList.add("valid");
    } else {
      capital.classList.remove("valid");
      capital.classList.add("invalid");
    }
  
    // Validate numbers
    var numbers = /[0-9]/g;
    if(myInput.value.match(numbers)) {  
      number.classList.remove("invalid");
      number.classList.add("valid");
    } else {
      number.classList.remove("valid");
      number.classList.add("invalid");
    }
    
    // Validate length
    if(myInput.value.length >= 8) {
      length.classList.remove("invalid");
      length.classList.add("valid");
    } else {
      length.classList.remove("valid");
      length.classList.add("invalid");
    }
  }

  myinput2.onkeyup = function() {
    console.log(myInput.value,myinput2.value);
    // validating confirm password
    if (myInput.value == myinput2.value)
    {
        passwordmatch.classList.remove("invalid");
        passwordmatch.classList.add("valid");
        document.getElementById('registerBtn').disabled = false;
    }
    else
    {
        passwordmatch.classList.remove("valid");
        passwordmatch.classList.add("invalid");
    }
  
  }
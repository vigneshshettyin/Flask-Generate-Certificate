const emailField = document.querySelector("#exampleInputEmail");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const loginBtn = document.querySelector("#loginBtn");

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;
  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/validate/email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_valid) {
          loginBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">You are not registered. Please sign up</p>`;
        } else if (data.email_pattern_error) {
          loginBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">${data.email_pattern_error}</p>`;
        } else {
          loginBtn.removeAttribute("disabled");
        }
      });
  }
});


// for show password
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#exampleInputPassword');
togglePassword.addEventListener('click', function (e) {
  // toggle the type attribute
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);
  // toggle the eye slash icon
  this.classList.toggle('fa-eye-slash');
});

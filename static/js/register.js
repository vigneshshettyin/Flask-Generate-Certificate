const passwordField = document.querySelector("#exampleInputPassword");
const password2Field = document.querySelector("#exampleRepeatPassword");
const emailField = document.querySelector("#exampleInputEmail");
const passwordFeedBackArea = document.querySelector(".passwordFeedBackArea");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const regitserBtn = document.querySelector("#registerBtn");

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
        if (data.email_error) {
          regitserBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">${data.email_error}</p>`;
        } else if (data.email_pattern_error) {
          regitserBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">${data.email_pattern_error}</p>`;
        } else {
          regitserBtn.removeAttribute("disabled");
        }
      });
  }
});

passwordField.addEventListener("keyup", (e) => {
  const passwordVal = e.target.value;

  passwordField.classList.remove("is-invalid");
  passwordFeedBackArea.style.display = "none";

  if (passwordVal.length > 0) {
    fetch("/validate/password", {
      body: JSON.stringify({
        password: passwordVal,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_error) {
          regitserBtn.disabled = true;
          passwordField.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p class="text-center">${data.password_error}</p>`;
        } else {
          regitserBtn.removeAttribute("disabled");
        }
      });
  }
});

password2Field.addEventListener("keyup", (e) => {
  const passwordVal = e.target.value;
  const password1Val = document.getElementById("exampleInputPassword").value;

  password2Field.classList.remove("is-invalid");
  passwordFeedBackArea.style.display = "none";

  if (passwordVal.length > 0) {
    fetch("/match/passwords", {
      body: JSON.stringify({
        password: password1Val,
        password2: passwordVal,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_mismatch) {
          regitserBtn.disabled = true;
          password2Field.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p class="text-center">${data.password_mismatch}</p>`;
        } else {
          regitserBtn.removeAttribute("disabled");
        }
      });
  }
});
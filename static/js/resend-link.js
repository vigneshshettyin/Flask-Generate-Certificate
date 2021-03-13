const emailField = document.querySelector("#exampleInputEmail");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const resendBtn = document.querySelector("#resendBtn");

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
          resendBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">Your account is already active.</p>`;
        } else if (data.email_pattern_error) {
          resendBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">${data.email_pattern_error}</p>`;
        } else if (data.email_valid) {
          resendBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p class="text-center">You are not registered yet.</p>`;
        } else {
          resendBtn.removeAttribute("disabled");
        }
      });
  }
});

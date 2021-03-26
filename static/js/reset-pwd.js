
const passwordField = document.querySelector("#exampleInputPassword");
const password2Field = document.querySelector("#exampleRepeatPassword");
const resetBtn = document.querySelector("#resetBtn");
const passwordFeedBackArea = document.querySelector(".passwordFeedBackArea");

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
          resetBtn.disabled = true;
          passwordField.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p class="text-center">${data.password_error}</p>`;
        } else {
          resetBtn.removeAttribute("disabled");
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
          resetBtn.disabled = true;
          password2Field.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p class="text-center">${data.password_mismatch}</p>`;
        } else {
          resetBtn.removeAttribute("disabled");
        }
      });
  }
});

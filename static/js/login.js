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

function check()
{
  console.log("fun called")
  var notice=document.getElementById("notice");
  var password=document.getElementById("exampleInputPassword");
  var x=document.getElementById("box").checked;
  if(x==true)
  {
    password.type="text";
    notice.innerHTML="hide password";
  }
  else
  {
    password.type="password";
    notice.innerHTML="show password";
  }
}
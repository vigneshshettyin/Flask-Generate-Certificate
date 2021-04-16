$(".payButton").click(function () {
  if (this.id == "basic") {
    $("#plan").val("Basic Plan");
  } else if (this.id == "regular") {
    $("#plan").val("Regular Plan");
  } else if (this.id == "premium") {
    $("#plan").val("Premium Plan");
  }
  $("#modalPayment").modal();
});

$("#cnfPay").click(function () {
  /* when the pay button in the modal is clicked, submit the form */
  if (
    $.trim($("#name").val()) === "" ||
    $.trim($("#email").val()) === "" ||
    $.trim($("#phone").val()) === ""
  ) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "One or more fields are missing.",
    });
    return false;
  }
});

function getFeedback() {
  Swal.fire({
    title: "Feedback",
    html: `<form action="/feedback" method="post" role="form">
    <input type="text" name="name" class="swal2-input" id="name" placeholder="Your Name"/>
    <input type="email" name="email" class="swal2-input" id="email" placeholder="Your Email"/>
    <input type="phone" name="phone" class="swal2-input" id="phone" placeholder="Your Phone Number"/>
    <label for="inlineRadio1">Rating</label> <br>
    <input type="radio" name="rating" id="inlineRadio1" value="1" required>
    <label for="inlineRadio1">1</label> &nbsp;
    <input type="radio" name="rating" id="inlineRadio2" value="2" required>
    <label for="inlineRadio1">2</label> &nbsp;
    <input type="radio" name="rating" id="inlineRadio3" value="3" required>
    <label for="inlineRadio1">3</label> &nbsp;
    <input type="radio" name="rating" id="inlineRadio4" value="4" required>
    <label for="inlineRadio1">4</label> &nbsp;
    <input type="radio" name="rating" id="inlineRadio5" value="5" checked required>
    <label for="inlineRadio1">5</label> &nbsp;
    <textarea class="swal2-input" name="message" id="message" rows="5" style="height:112px;" placeholder="Feedback...."></textarea>
    `,
    confirmButtonText: "Send Feedback",
    focusConfirm: false,
    showLoaderOnConfirm: false,
    customClass: {
      loader: "custom-loader",
    },
    loaderHtml: '<div class="spinner-border text-primary"></div>',
    preConfirm: () => {
      Swal.showLoading();
      const name = Swal.getPopup().querySelector("#name").value;
      const email = Swal.getPopup().querySelector("#email").value;
      const phone = Swal.getPopup().querySelector("#phone").value;
      const rating = Swal.getPopup().querySelector("input[name=rating]:checked")
        .value;
      const message = Swal.getPopup().querySelector("#message").value;
      var pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      var phonepattern=/^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/im;
      if (!name) {
        Swal.showValidationMessage(`Name is missing`);
      } else if (!email) {
        Swal.showValidationMessage(`Email address is missing.`);
      } else if (String(email).search(pattern) == -1) {
        Swal.showValidationMessage(`Enter a valid email address`);
      } else if (!phone) {
        Swal.showValidationMessage(`Phone Number is missing`);
      }else if (String(phone).search(phonepattern) == -1) {
        Swal.showValidationMessage(`Enter a valid 10-digit phone number`);
      }else if (!rating) {
        Swal.showValidationMessage(`Rating is missing`);
      } else if (!message) {
        Swal.showValidationMessage(`Feedback is missing`);
      }
      return {
        email: email,
        name: name,
        phone: phone,
        rating: rating,
        message: message,
      };
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      fetch("/feedback", {
        body: JSON.stringify({
          email: result.value.email,
          name: result.value.name,
          phone: result.value.phone,
          rating: result.value.rating,
          message: result.value.message,
        }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.feedback_success) {
            new Notify({
              title: "Success",
              text: `${data.feedback_success}`,
              status: "success",
            });
          } else {
            new Notify({
              title: "Error",
              text: `${data.feedback_error}`,
              status: "error",
            });
          }
        });
    }
  });
}

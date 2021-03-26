// For adding new group
$("#add_group").click(function (e) {
  Swal.fire({
    title: "Enter Group Details",
    html: `<form action="" method="POST" id="addGrpForm">
          <input type="text" id="name" name="name" class="swal2-input" placeholder="Name">
          <input type="text" id="dept" name="dept" class="swal2-input" placeholder="Department">
        <input type="email" id="email" name="email" class="swal2-input" placeholder="Email address">
        <input type="text" id="phone" name="phone" class="swal2-input" placeholder="Phone">
        </form>
        `,
    confirmButtonText: "Save",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    preConfirm: () => {
      const email = Swal.getPopup().querySelector("#email").value;
      const name = Swal.getPopup().querySelector("#name").value;
      const dept = Swal.getPopup().querySelector("#dept").value;
      const phone = Swal.getPopup().querySelector("#phone").value;
      var pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!name) {
        Swal.showValidationMessage(`Name is missing`);
      } else if (!dept) {
        Swal.showValidationMessage(`Department is missing`);
      } else if (!email) {
        Swal.showValidationMessage(`Email address is missing.`);
      } else if (String(email).search(pattern) == -1) {
        Swal.showValidationMessage(`Enter a valid email address`);
      } else if (!phone) {
        Swal.showValidationMessage(`Phone Number is missing`);
      }
      return {
        email: email,
        name: name,
        dept: dept,
        phone: phone,
      };
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      fetch("/edit/group/0", {
        body: JSON.stringify({
          email: result.value.email,
          name: result.value.name,
          dept: result.value.dept,
          phone: result.value.phone,
        }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.group_duplicate) {
            Swal.fire({
              icon: "error",
              title: "Already Exists",
              text: `This group has already been added.`,
            });
          } else if (data.group_success) {
            Swal.fire({
              icon: "success",
              title: "Added",
              html: `Group added successfully.`,
            });
            window.location.reload();
          } else {
            Swal.fire({
              icon: "error",
              title: "Oops..",
              text: `We've encountered some error while adding. Please try again.`,
            });
          }
        });
    }
  });
});

// For editing a group
function editGrp(postId) {
  fetch(`/edit/group/${postId}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      Swal.fire({
        title: "Update Group Details",
        html: `<form action="" method="POST" id="editGrpForm">
          <input type="text" id="name" name="name" class="swal2-input" value="${data.post.name}" placeholder="Name">
          <input type="text" id="dept" name="dept" class="swal2-input" value="${data.post.subname}" placeholder="Department">
        <input type="email" id="email" name="email" class="swal2-input" value="${data.post.email}" placeholder="Email address">
        <input type="text" id="phone" name="phone" class="swal2-input" value="${data.post.phone}" placeholder="Phone">
        </form>
        `,
        confirmButtonText: "Update",
        focusConfirm: false,
        customClass: {
          confirmButton: "btn btn-primary btn-lg",
        },
        showLoaderOnConfirm: true,
        preConfirm: () => {
          const email = Swal.getPopup().querySelector("#email").value;
          const name = Swal.getPopup().querySelector("#name").value;
          const dept = Swal.getPopup().querySelector("#dept").value;
          const phone = Swal.getPopup().querySelector("#phone").value;
          var pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
          if (!name) {
            Swal.showValidationMessage(`Name is missing`);
          } else if (!dept) {
            Swal.showValidationMessage(`Department is missing`);
          } else if (!email) {
            Swal.showValidationMessage(`Email address is missing.`);
          } else if (String(email).search(pattern) == -1) {
            Swal.showValidationMessage(`Enter a valid email address`);
          } else if (!phone) {
            Swal.showValidationMessage(`Phone Number is missing`);
          }
          return {
            email: email,
            name: name,
            dept: dept,
            phone: phone,
          };
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.value) {
          fetch(`/edit/group/${postId}`, {
            body: JSON.stringify({
              email: result.value.email,
              name: result.value.name,
              dept: result.value.dept,
              phone: result.value.phone,
            }),
            method: "POST",
          })
            .then((res) => res.json())
            .then((data2) => {
              if (data2.group_success) {
                Swal.fire({
                  icon: "success",
                  title: "Updated",
                  html: `Group edited successfully.`,
                });
                window.location.reload();
              } else {
                Swal.fire({
                  icon: "error",
                  title: "Oops..",
                  text: `We've encountered some error while editing. Please try again.`,
                });
              }
            });
        }
      });
    });
}

// For adding Certificate
function addCertificate(grp_id) {
  Swal.fire({
    title: "Enter Certificate Details",
    html: `<form action="" method="POST" id="addGrpForm">
          <input type="text" id="name" name="name" class="swal2-input" placeholder="Name">
          <input type="email" id="email" name="email" class="swal2-input" placeholder="Email address">
        <input type="text" id="course" name="course" class="swal2-input" placeholder="Course">
        </form>
        `,
    confirmButtonText: "Save",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    preConfirm: () => {
      const email = Swal.getPopup().querySelector("#email").value;
      const name = Swal.getPopup().querySelector("#name").value;
      const course = Swal.getPopup().querySelector("#course").value;
      var pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!name) {
        Swal.showValidationMessage(`Name is missing`);
      } else if (!email) {
        Swal.showValidationMessage(`Email address is missing.`);
      } else if (String(email).search(pattern) == -1) {
        Swal.showValidationMessage(`Enter a valid email address`);
      } else if (!course) {
        Swal.showValidationMessage(`Course is missing`);
      }
      return {
        email: email,
        name: name,
        course: course,
      };
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      fetch(`/edit/${grp_id}/certificates/0`, {
        body: JSON.stringify({
          email: result.value.email,
          name: result.value.name,
          course: result.value.course,
        }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          if (data.certificate_duplicate) {
            Swal.fire({
              icon: "error",
              title: "Already Exists",
              text: `This certificate has already been added.`,
            });
          } else if (data.certificate_success) {
            Swal.fire({
              icon: "success",
              title: "Added",
              html: `Certificate added successfully.`,
            });
            window.location.reload();
          } else {
            Swal.fire({
              icon: "error",
              title: "Oops..",
              text: `We've encountered some error while adding. Please try again.`,
            });
          }
        });
    }
  });
}

// For editing Certificate
function editCertificate(grp_id, cert_id) {
  fetch(`/edit/${grp_id}/certificates/${cert_id}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      Swal.fire({
        title: "Enter Certificate Details",
        html: `<form action="" method="POST" id="addGrpForm">
          <input type="text" id="name" name="name" class="swal2-input" value="${data.post.name}" placeholder="Name">
          <input type="email" id="email" name="email" class="swal2-input" value="${data.post.email}" placeholder="Email address">
        <input type="text" id="course" name="course" class="swal2-input" value="${data.post.coursename}" placeholder="Course">
        </form>
        `,
        confirmButtonText: "Save",
        focusConfirm: false,
        customClass: {
          confirmButton: "btn btn-primary btn-lg",
        },
        showLoaderOnConfirm: true,
        preConfirm: () => {
          const email = Swal.getPopup().querySelector("#email").value;
          const name = Swal.getPopup().querySelector("#name").value;
          const course = Swal.getPopup().querySelector("#course").value;
          var pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
          if (!name) {
            Swal.showValidationMessage(`Name is missing`);
          } else if (!email) {
            Swal.showValidationMessage(`Email address is missing.`);
          } else if (String(email).search(pattern) == -1) {
            Swal.showValidationMessage(`Enter a valid email address`);
          } else if (!course) {
            Swal.showValidationMessage(`Course is missing`);
          }
          return {
            email: email,
            name: name,
            course: course,
          };
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.value) {
          fetch(`/edit/${grp_id}/certificates/${cert_id}`, {
            body: JSON.stringify({
              email: result.value.email,
              name: result.value.name,
              course: result.value.course,
            }),
            method: "POST",
          })
            .then((res) => res.json())
            .then((data2) => {
              if (data2.certificate_success) {
                Swal.fire({
                  icon: "success",
                  title: "Updated",
                  html: `Certificate edited successfully.`,
                });
                window.location.reload();
              } else {
                Swal.fire({
                  icon: "error",
                  title: "Oops..",
                  text: `We've encountered some error while editing. Please try again.`,
                });
              }
            });
        }
      });
    });
}

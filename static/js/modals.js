// For adding new group
$("#add_group").click(function (e) {
  Swal.fire({
    title: "Enter Group Details",
    html: `<form action="" method="POST" id="addGrpForm" enctype="multipart/form-data">
          <input type="text" id="name" name="name" class="swal2-input" placeholder="Name">
          <select id="category" name="category" class="swal2-input">
            <option value="saab" disabled selected>Choose a category</option>
          </select>
          <input type="file" name="signature" class="swal2-file" id="signature" accept="image/*">
          <input type="file" name="bg_image" class="swal2-file" id="bg_image" accept="image/*">
          </form>
        `,
    confirmButtonText: "Create",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    willOpen: () => {
      fetch(`/get-all-categories`, {
        method: "GET",
      })
        .then((res) => res.json())
        .then((data) => {
          $.each(data.category, function (key, name) {
            //Use the Option() constructor to create a new HTMLOptionElement.
            var option = new Option(name, name);
            //Convert the HTMLOptionElement into a JQuery object that can be used with the append method.
            $(option).html(name);
            //Append the option to our Select element.
            $("#category").append(option);
          });
        });
    },
    preConfirm: () => {
      const name = Swal.getPopup().querySelector("#name").value;
      const category = Swal.getPopup().querySelector("#category").value;
      const signature = Swal.getPopup().querySelector("#signature").value;
      const bg_image = Swal.getPopup().querySelector("#bg_image").value;
      $("#signature").change(function () {
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
      });
      $("#bg_image").change(function () {
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
      });
      if (!name) {
        Swal.showValidationMessage(`Name is missing`);
      } else if (!category) {
        Swal.showValidationMessage(`Category is missing`);
      } else if (!signature) {
        Swal.showValidationMessage(`Signature is missing.`);
      } else if (!bg_image) {
        Swal.showValidationMessage(`Background Image is missing`);
      }
      return {
        name: name,
        category: category,
      };
    },
    willClose: () => {
          Swal.showLoading();
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      var formData = new FormData();
      var signature = $("#signature")[0].files[0];
      var bg_image = $("#bg_image")[0].files[0];
      formData.append("signature", signature);
      formData.append("bg_image", bg_image);
      formData.append("name", result.value.name);
      formData.append("category", result.value.category);
      $.ajax({
        method: "post",
        url: `/edit/group/0`,
        data: formData,
        processData: false,
        contentType: false,
        success: function (resp) {
          new Notify({
            title: "Success",
            text: `Group has been created successfully!`,
            status: "success",
          });
          window.location.reload();
        },
        error: function (resp) {
          new Notify({
            title: "Error",
            text: `Sorry, we encountered an error while creating the group.`,
            status: "error",
          });
        },
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
          <select id="category" name="category" class="swal2-input">
            <option value="${data.post.category}" disabled selected>${data.post.category}</option>
          </select>
          <input type="file" name="signature" class="swal2-file" id="signature" accept="image/*">
          <input type="file" name="bg_image" class="swal2-file" id="bg_image" accept="image/*">
        </form>
        `,
        confirmButtonText: "Update",
        focusConfirm: false,
        customClass: {
          confirmButton: "btn btn-primary btn-lg",
        },
        showLoaderOnConfirm: true,
        willOpen: () => {
          fetch(`/get-all-categories`, {
            method: "GET",
          })
            .then((res) => res.json())
            .then((cat) => {
              $.each(cat.category, function (key, name) {
                var option = new Option(name, name);
                $(option).html(name);
                $("#category").append(option);
              });
            });
        },
        preConfirm: () => {
          const name = Swal.getPopup().querySelector("#name").value;
          const category = Swal.getPopup().querySelector("#category").value;
          const signature = Swal.getPopup().querySelector("#signature").value;
          const bg_image = Swal.getPopup().querySelector("#bg_image").value;
          $("#signature").change(function () {
            var reader = new FileReader();
            reader.readAsDataURL(this.files[0]);
          });
          $("#bg_image").change(function () {
            var reader = new FileReader();
            reader.readAsDataURL(this.files[0]);
          });
          if (!name) {
            Swal.showValidationMessage(`Name is missing`);
          } else if (!category) {
            Swal.showValidationMessage(`Category is missing`);
          }
          return {
            name: name,
            category: category,
          };
        },
        willClose: () => {
          Swal.showLoading();
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.value) {
          var formData = new FormData();
          var signature = $("#signature")[0].files[0];
          var bg_image = $("#bg_image")[0].files[0];
          formData.append("signature", signature);
          formData.append("bg_image", bg_image);
          formData.append("name", result.value.name);
          formData.append("category", result.value.category);
          $.ajax({
            method: "post",
            url: `/edit/group/${postId}`,
            data: formData,
            processData: false,
            contentType: false,
            success: function (resp) {
              new Notify({
                title: "Success",
                text: `Group has been updated successfully!`,
                status: "success",
              });
              window.location.reload();
            },
            error: function (resp) {
              new Notify({
                title: "Error",
                text: `Sorry, we encountered an error while updating the group.`,
                status: "error",
              });
            },
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

// Upload CSV

function uploadFile(grp_id) {
  Swal.fire({
    title: "Select a CSV file",
    text: "Download the sample CSV file and add your data inside that.",
    footer: `<a class="btn btn-info btn-icon-split" href="/static/assets/sample_csv.csv" download>
                        <span class="icon text-white-50">
                           <i class="fa fa-download" aria-hidden="true"></i>
                        </span>
                        <span class="text">Sample CSV File</span>                                    
                    </a>`,
    showCancelButton: true,
    confirmButtonText: "Upload",
    input: "file",
    willOpen: () => {
      $(".swal2-file").change(function () {
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
      });
      $(".swal2-file").attr("accept", ".csv");
    },
  }).then((file) => {
    if (file.value) {
      var formData = new FormData();
      var f = $(".swal2-file")[0].files[0];
      formData.append("fileToUpload", f);
      $.ajax({
        method: "post",
        url: `/upload/${grp_id}/certificate`,
        data: formData,
        processData: false,
        contentType: false,
        success: function (resp) {
          new Notify({
            title: "Success",
            text: `Your data has been imported successfully!`,
            status: "success",
          });
          window.location.reload();
        },
        error: function () {
          new Notify({
            title: "Error",
            text: `Sorry, we encountered an error while uploading the file.`,
            status: "error",
          });
        },
      });
    }
  });
}

// For adding new category
function addCategory() {
  Swal.fire({
    title: "Enter Category Details",
    html: `<form action="" method="POST" id="addCategoryForm">
          <input type="text" id="name" name="name" class="swal2-input" placeholder="Name">
          <textarea id="content" name="content" class="swal2-input" placeholder="Content"></textarea>
        </form>
        `,
    footer: `Note : Please &nbsp;<strong> do not </strong>&nbsp; mention date in content.`,
    confirmButtonText: "Create",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    preConfirm: () => {
      const name = Swal.getPopup().querySelector("#name").value;
      const content = Swal.getPopup().querySelector("#content").value;
      if (!name) {
        Swal.showValidationMessage(`Name is missing`);
      } else if (!content) {
        Swal.showValidationMessage(`Content is missing.`);
      }
      return {
        name: name,
        content: content,
      };
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      fetch(`/edit/category/0`, {
        body: JSON.stringify({
          name: result.value.name,
          content: result.value.content,
        }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.category_duplicate) {
            Swal.fire({
              icon: "error",
              title: "Already Exists",
              text: `This category has already been added.`,
            });
          } else if (data.category_success) {
            Swal.fire({
              icon: "success",
              title: "Added",
              html: `Category added successfully.`,
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

// For editing a category
function editCategory(postId) {
  fetch(`/edit/category/${postId}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      Swal.fire({
        title: "Update Group Details",
        html: `<form action="" method="POST" id="editCategoryForm">
        <input type="text" id="name" name="name" class="swal2-input" value="${data.post.name}" placeholder="Name">
          <textarea id="content" name="content" class="swal2-input" placeholder="Content">${data.post.content}</textarea>
        </form>
        `,
        confirmButtonText: "Update",
        focusConfirm: false,
        customClass: {
          confirmButton: "btn btn-primary btn-lg",
        },
        showLoaderOnConfirm: true,
        preConfirm: () => {
          const name = Swal.getPopup().querySelector("#name").value;
          const content = Swal.getPopup().querySelector("#content").value;
          if (!name) {
            Swal.showValidationMessage(`Name is missing`);
          } else if (!content) {
            Swal.showValidationMessage(`Content is missing`);
          }
          return {
            name: name,
            content: content,
          };
        },
        willClose: () => {
          Swal.showLoading();
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.value) {
          fetch(`/edit/category/${postId}`, {
            body: JSON.stringify({
              name: result.value.name,
              content: result.value.content,
            }),
            method: "POST",
          })
            .then((res) => res.json())
            .then((data2) => {
              if (data2.category_success) {
                Swal.fire({
                  icon: "success",
                  title: "Updated",
                  html: `Category edited successfully.`,
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

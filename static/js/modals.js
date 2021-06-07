// For adding new group
$("#add_group").click(function (e) {
  Swal.fire({
    title: "Enter Group Details",
    html: `<form action="" method="POST" id="addGrpForm" enctype="multipart/form-data">
          <input type="text" id="name" name="name" class="swal2-input" placeholder="Name">
          <input type="file" name="bg_image" class="swal2-file" id="bg_image" accept="image/png">
          <input type="number" id="certx" name="certx" class="swal2-input" placeholder="Name (x-axis)">
          <input type="number" id="certy" name="certy" class="swal2-input" placeholder="Name (y-axis)">
          <input type="number" id="qrx" name="qrx" class="swal2-input" placeholder="QR Code (x-axis)">
          <input type="number" id="qry" name="qry" class="swal2-input" placeholder="QR Code (y-axis)">
          <input type="number" id="certnox" name="certnox" class="swal2-input" placeholder="Certificate No (x-axis)">
          <input type="number" id="certnoy" name="certnoy" class="swal2-input" placeholder="Certificate No (y-axis)">
          <input type="text" id="prefix" name="prefix" class="swal2-input" placeholder="Certificate ID Prefix">
          <select id="category" name="font_name" class="swal2-input">
          <option value="" disabled selected>Select the font</option>
          </select>
          <input type="number" id="font_size" name="font_size" class="swal2-input" placeholder="Font Size">
          <input type="color" class="form-control form-control-color" id="textColor" value="#000000" title="Choose your text color">
          </form>
        `,
    footer: `Note : Use PNG images only`,
    confirmButtonText: "Create",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    willOpen: () => {
      fetch(`/get-all-fonts`, {
        method: "GET",
      })
        .then((res) => res.json())
        .then((data) => {
          $.each(data.font, function (key, name) {
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
      const bg_image = Swal.getPopup().querySelector("#bg_image").value;
      const certx = Swal.getPopup().querySelector("#certx").value;
      const certy = Swal.getPopup().querySelector("#certy").value;
      const qrx = Swal.getPopup().querySelector("#qrx").value;
      const qry = Swal.getPopup().querySelector("#qry").value;
      const certnox = Swal.getPopup().querySelector("#certnox").value;
      const certnoy = Swal.getPopup().querySelector("#certnoy").value;
      const font_size = Swal.getPopup().querySelector("#font_size").value;
      const category = Swal.getPopup().querySelector("#category").value;
      const textColor = Swal.getPopup().querySelector("#textColor").value;
      const prefix = Swal.getPopup().querySelector("#prefix").value;
      $("#bg_image").change(function () {
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
      });
      if (!name) {
        Swal.showValidationMessage(`Name is missing`);
      } else if (!bg_image) {
        Swal.showValidationMessage(`Background Image is missing`);
      } else if (!certx) {
        Swal.showValidationMessage(`Name (x-axis) is missing`);
      } else if (!certy) {
        Swal.showValidationMessage(`Name (y-axis) is missing`);
      } else if (!qrx) {
        Swal.showValidationMessage(`QR Code (x-axis) is missing`);
      } else if (!qry) {
        Swal.showValidationMessage(`QR Code (y-axis) is missing`);
      } else if (!certnox) {
        Swal.showValidationMessage(`Certificate No (x-axis) is missing`);
      } else if (!certnoy) {
        Swal.showValidationMessage(`Certificate No (y-axis) is missing`);
      } else if (!prefix) {
        Swal.showValidationMessage(`Certificate ID Prefix is missing`);
      } else if (!category) {
        Swal.showValidationMessage(`Font Name is missing`);
      } else if (!font_size) {
        Swal.showValidationMessage(`Font Size is missing`);
      } else if (!textColor) {
        Swal.showValidationMessage(`Text Color is missing`);
      }
      return {
        name: name,
        certx: certx,
        certy: certy,
        qrx: qrx,
        qry: qry,
        certnox: certnox,
        certnoy: certnoy,
        font_size: font_size,
        category: category,
        textColor: textColor,
        prefix: prefix,
      };
    },
    willClose: () => {
      Swal.showLoading();
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      var formData = new FormData();
      var bg_image = $("#bg_image")[0].files[0];
      formData.append("bg_image", bg_image);
      formData.append("certx", result.value.certx);
      formData.append("certy", result.value.certy);
      formData.append("qrx", result.value.qrx);
      formData.append("qry", result.value.qry);
      formData.append("certnox", result.value.certnox);
      formData.append("certnoy", result.value.certnoy);
      formData.append("prefix", result.value.prefix);
      formData.append("name", result.value.name);
      formData.append("font_size", result.value.font_size);
      formData.append("font_name", result.value.category);
      formData.append("textColor", result.value.textColor);
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
          <input type="file" name="bg_image" class="swal2-file" id="bg_image" accept="image/png">
          <input type="number" value="${data.post.certx}" id="certx" name="certx" class="swal2-input" placeholder="Name (x-axis)">
          <input type="number" value="${data.post.certy}" id="certy" name="certy" class="swal2-input" placeholder="Name (y-axis)">
          <input type="number" value="${data.post.qrx}" id="qrx" name="qrx" class="swal2-input" placeholder="QR Code (x-axis)">
          <input type="number" value="${data.post.qry}" id="qry" name="qry" class="swal2-input" placeholder="QR Code (y-axis)">
          <input type="number" value="${data.post.certnox}" id="certnox" name="certnox" class="swal2-input" placeholder="Certificate No (x-axis)">
          <input type="number" value="${data.post.certnoy}" id="certnoy" name="certnoy" class="swal2-input" placeholder="Certificate No (y-axis)">
          <select id="category" name="font_name" class="swal2-input">
          <option value="${data.post.font_name}" disabled selected>${data.post.font_name}</option>
          </select>
          <input type="number" value="${data.post.font_size}" id="font_size" name="font_size" class="swal2-input" placeholder="Font Size">
          <input type="color" class="form-control form-control-color" id="textColor" value="${data.post.textColor}" title="Choose your text color">
        </form>
        `,
        confirmButtonText: "Update",
        focusConfirm: false,
        customClass: {
          confirmButton: "btn btn-primary btn-lg",
        },
        showLoaderOnConfirm: true,
        willOpen: () => {
          fetch(`/get-all-fonts`, {
            method: "GET",
          })
            .then((res) => res.json())
            .then((data) => {
              $.each(data.font, function (key, name) {
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
          const bg_image = Swal.getPopup().querySelector("#bg_image").value;
          const certx = Swal.getPopup().querySelector("#certx").value;
          const certy = Swal.getPopup().querySelector("#certy").value;
          const qrx = Swal.getPopup().querySelector("#qrx").value;
          const qry = Swal.getPopup().querySelector("#qry").value;
          const certnox = Swal.getPopup().querySelector("#certnox").value;
          const certnoy = Swal.getPopup().querySelector("#certnoy").value;
          const font_size = Swal.getPopup().querySelector("#font_size").value;
          const category = Swal.getPopup().querySelector("#category").value;
          const textColor = Swal.getPopup().querySelector("#textColor").value;
          $("#bg_image").change(function () {
            var reader = new FileReader();
            reader.readAsDataURL(this.files[0]);
          });
          if (!name) {
            Swal.showValidationMessage(`Name is missing`);
          } else if (!bg_image) {
            Swal.showValidationMessage(`Background Image is missing`);
          } else if (!certx) {
            Swal.showValidationMessage(`Name (x-axis) is missing`);
          } else if (!certy) {
            Swal.showValidationMessage(`Name (y-axis) is missing`);
          } else if (!qrx) {
            Swal.showValidationMessage(`QR Code (x-axis) is missing`);
          } else if (!qry) {
            Swal.showValidationMessage(`QR Code (y-axis) is missing`);
          } else if (!certnox) {
            Swal.showValidationMessage(`Certificate No (x-axis) is missing`);
          } else if (!certnoy) {
            Swal.showValidationMessage(`Certificate No (y-axis) is missing`);
          } else if (!font_size) {
            Swal.showValidationMessage(`Font Size is missing`);
          } else if (!category) {
            Swal.showValidationMessage(`Font Name is missing`);
          } else if (!textColor) {
            Swal.showValidationMessage(`Text Color is missing`);
          }
          return {
            name: name,
            certx: certx,
            certy: certy,
            qrx: qrx,
            qry: qry,
            certnox: certnox,
            certnoy: certnoy,
            font_size: font_size,
            category: category,
            textColor: textColor,
          };
        },
        willClose: () => {
          Swal.showLoading();
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.value) {
          var formData = new FormData();
          var bg_image = $("#bg_image")[0].files[0];
          formData.append("bg_image", bg_image);
          formData.append("name", result.value.name);
          formData.append("certx", result.value.certx);
          formData.append("certy", result.value.certy);
          formData.append("qrx", result.value.qrx);
          formData.append("qry", result.value.qry);
          formData.append("certnox", result.value.certnox);
          formData.append("certnoy", result.value.certnoy);
          formData.append("font_size", result.value.font_size);
          formData.append("font_name", result.value.category);
          formData.append("textColor", result.value.textColor);
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

// for generating API
function generateAPI() {
  Swal.fire({
    title: "Select Group",
    html: `<form action="" method="POST" id="generateAPI">
          <select id="group" name="group" class="swal2-input">
            <option value="" disabled selected>Choose a group</option>
          </select>
        </form>
        `,
    confirmButtonText: "Generate",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    willOpen: () => {
      fetch(`/get-all-groups`, {
        method: "GET",
      })
        .then((res) => res.json())
        .then((data) => {
          $.each(data.group, function (key, name) {
            //Use the Option() constructor to create a new HTMLOptionElement.
            var option = new Option(name[1], name[0]);
            //Convert the HTMLOptionElement into a JQuery object that can be used with the append method.
            $(option).html(name[1]);
            //Append the option to our Select element.
            $("#group").append(option);
          });
        });
    },
    preConfirm: () => {
      const group = Swal.getPopup().querySelector("#group").value;
      if (!group) {
        Swal.showValidationMessage(`Group is missing`);
      }
      return {
        group: group,
      };
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    fetch(`/api-key/generate/${result.value.group}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.key_success) {
          window.location.reload();
          new Notify({
            title: "Success",
            text: `${data.key_success}`,
            status: "success",
          });
        } else {
          new Notify({
            title: "Error",
            text: `${data.key_error}`,
            status: "error",
          });
        }
      });
  });
}

// approve api key
function approveAPI(grpId) {
  Swal.fire({
    title: "Set Usage Limit",
    html: `<form action="" method="POST" id="generateAPI">
          <input type="number" id="usage_limit" name="usage_limit" class="swal2-input" placeholder="Usage">
        </form>
        `,
    confirmButtonText: "Approve",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-success btn-lg",
    },
    showLoaderOnConfirm: true,
    preConfirm: () => {
      const usage_limit = Swal.getPopup().querySelector("#usage_limit").value;
      if (!usage_limit) {
        Swal.showValidationMessage(`Usage Limit is missing`);
      }
      return {
        usage_limit: usage_limit,
      };
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    fetch(`/api-key/private/approve/${grpId}`, {
      method: "POST",
      body: JSON.stringify({
        usage_limit: result.value.usage_limit,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.key_approved) {
          window.location.reload();
          new Notify({
            title: "Success",
            text: `${data.key_approved}`,
            status: "success",
          });
        } else {
          new Notify({
            title: "Error",
            text: `${data.key_error}`,
            status: "error",
          });
        }
      });
  });
}

function approvePublicAPI(api_id) {
  fetch(`/api-key/public/approve/${api_id}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.key_approved) {
        window.location.reload();
        new Notify({
          title: "Success",
          text: `${data.key_approved}`,
          status: "success",
        });
      } else {
        new Notify({
          title: "Error",
          text: `${data.key_error}`,
          status: "error",
        });
      }
    });
}

$("#add_font").click(function (e) {
  Swal.fire({
    title: "Enter Font Details",
    html: `<form action="" method="POST" id="addGrpForm" enctype="multipart/form-data">
          <input type="text" id="name" name="name" class="swal2-input" placeholder="Name">
          <input type="text" id="font" name="font" class="swal2-input" placeholder="Font CDN">
          </form>
        `,
    footer: `<p>Note : Get CDN From <a href="https://fonts.google.com/" target="_blank">Google Fonts</a></p>`,
    confirmButtonText: "Create",
    focusConfirm: false,
    customClass: {
      confirmButton: "btn btn-primary btn-lg",
    },
    showLoaderOnConfirm: true,
    preConfirm: () => {
      const name = Swal.getPopup().querySelector("#name").value;
      const font = Swal.getPopup().querySelector("#font").value;
      if (!name) {
        Swal.showValidationMessage(`Font Name is missing`);
      } else if (!font) {
        Swal.showValidationMessage(`Font CDN is missing`);
      }
      return {
        name: name,
        font: font,
      };
    },
    willClose: () => {
      Swal.showLoading();
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.value) {
      var formData = new FormData();
      formData.append("name", result.value.name);
      formData.append("font", result.value.font);
      $.ajax({
        method: "POST",
        url: `/add/fonts`,
        data: formData,
        processData: false,
        contentType: false,
        success: function (resp) {
          new Notify({
            title: "Success",
            text: `Font has been added successfully!`,
            status: "success",
          });
          window.location.reload();
        },
        error: function (resp) {
          new Notify({
            title: "Error",
            text: `Sorry, we encountered an error while creating the new font.`,
            status: "error",
          });
        },
      });
    }
  });
});

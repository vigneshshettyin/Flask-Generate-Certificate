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
  $("#paymentForm").submit();
});

var pass_id = document.getElementById("pass");
var pass_repeat_id = document.getElementById("pass_repeat");
var pass_error_id = document.getElementById("pass_error_msg");
var pass_input;
var pass_repeat_input;
var pass_ids = document.querySelectorAll("#pass, #pass_repeat")
var error_msg_id = document.getElementById("error_msg")
var sign_btn_id = document.getElementById("sign-up_btn")
var cancel_btn_id = document.getElementById("cancel_btn")
var username_msg_id = document.getElementById("user_id_msg")
var email_msg_id = document.getElementById("email_msg")
var user_fm_id = document.getElementsByClassName("signupForm")
var dob_id = document.getElementById("birth_date")
var church_here_link = document.getElementById("church_link")
var church_reg_modal = document.getElementById('church_modal');




var sign_up_callback = (data) => {
  if (data ==="Username already exists"){
    $(username_msg_id).text(data)
  }
  else if (data === "Email already exists"){
    $(email_msg_id).text(data)
  }
  else {
    window.location.href="account_confirm"
  }
};

$(pass_ids).keyup(function(event){
  pass_input = $(pass_id).val();
  pass_repeat_input = $(pass_repeat_id).val();
  //this is for comparing pass with repeat pass
  if (pass_input !== pass_repeat_input) {
    $(pass_error_id).css({'color': 'red'});
    $(pass_error_id).text("password and repeat password don't match");
  }
  else {
    $(pass_error_id).css({'color': 'green'});
    $(pass_error_id).text("password and repeat password match");
  };
});


$(sign_btn_id).on("click", function(event){
  //this is making sure pass is at least 8 characters long
  if (pass_input.length < 8) {
    $(pass_error_id).css({'color': 'red'})
    $(pass_error_id).text("your password needs to be more than 8 characters");
  }
  else if (pass_input !== pass_repeat_input){
    $(pass_error_id).css({'color': 'red'})
    $(pass_error_id).text("please check your information");
  }
  else {
      $.ajax({
        url:"/sign_up",
        type:"POST",
        data: $(user_fm_id).serialize(),
        success: sign_up_callback
      })
  };
});

$(dob_id).datepicker({
  orientation: "bottom auto",
  defaultViewDate: { year: 1980, month: 01, day: 01 },
  autoclose: true
});

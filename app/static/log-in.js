var pass_id = document.getElementById("pass");
var pass_repeat_id = document.getElementById("pass_repeat");
var pass_error_id = document.getElementById("pass_error_msg");
var pass_input;
var pass_repeat_input;
var pass_ids = document.querySelectorAll("#pass, #pass_repeat")
var error_msg_id = document.getElementById("error_msg")
var sign_btn_id = document.getElementById("sign-up_btn")
var cancel_btn_id = document.getElementById("cancel_btn")
var user_fm_id = document.getElementById("user_sign_fm")

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


$(sign_btn_id).click(function(event){
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
    $(user_fm_id).submit()
  };
});

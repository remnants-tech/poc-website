var login_form_class = document.getElementsByClassName("login_form");
var login_btn_id = document.getElementById("login_btn");
var username_id = document.getElementById("username");
var password_id = document.getElementById("pass");
var login_alert = document.getElementById("login_success");

//first disable form submit via enter key and enable enter key for password or username bar
$(login_form_class).keypress(
    (event) => {
     if (event.which == '13') {
        event.preventDefault();
      }
});

$(username_id).keypress(
  (event) => {
    if (event.which == '13') {
       $(login_btn_id).click();
     }
  }
)

$(password_id).keypress(
  (event) => {
    if (event.which == '13') {
       $(login_btn_id).click();
     }
  }
)

//ajax post for authenticating the user

$(login_btn_id).click(function() {
  $.ajax({
    url:"/user_authentication",
    type:"POST",
    data: $(login_form_class).serialize(),
    success: (login_auth_result) => {
      $(login_alert).text("signed in successfully");
      $(".alert").alert()
    }
  })
})

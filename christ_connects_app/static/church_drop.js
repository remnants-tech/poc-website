var church_drop_id = document.getElementById("church_drop");
var state_drop_id = document.getElementById("state_drop");
var modal_fm = document.getElementsByClassName("modal-content");
var modal_reg_btn = document.getElementById("church_reg_submit");
var modal_msg_id = document.getElementById("modal_msg");
var modal_close_btn = document.getElementById("church_reg_close")





var sample,churches_json
var pull_church_callback = (data) => {
  churches_json = JSON.parse(data);
  for (church_pk in churches_json){
    $(church_drop_id).append("<option value="+ church_pk + ">" + churches_json[church_pk] + "</option>");
  };
};
var states_arr= ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
"South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","American Samoa","District of Columbia","Federated States of Micronesia","Guam","Marshall Islands","Northern Mariana Islands","Palau","Puerto Rico","Virgin Islands"]



$.get("/pull_churches",pull_church_callback)

for (state_i = 0; state_i < states_arr.length; state_i++){
  var state = states_arr[state_i];
  $(state_drop_id).append("<option value=" + state + ">" + state + "</option>")
};

$(modal_reg_btn).on("click", function(event){
  $.ajax({
    url:"/user_church_reg",
    type:"POST",
    data: $(modal_fm).serialize(),
    success: (data) => {
      $(modal_msg_id).text(data);
      if (data === "church registered successfully"){
        $(church_drop_id).empty();
        $.get("/pull_churches", pull_church_callback).done( () => {
          $(modal_fm)[0].reset();
          $(modal_msg_id).empty();
          $(modal_close_btn).click();
        });
      };
    }
  })
})

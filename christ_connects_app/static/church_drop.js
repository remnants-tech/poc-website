var church_drop_id = document.getElementById("church_drop");
var sample,churches_json
var pull_church_callback = (data) => {
  churches_json = JSON.parse(data)[0]
  for (church_pk in churches_json){
    $(church_drop_id).append("<option value="+ church_pk + ">" + churches_json[church_pk] + "</option>");
  };
};

$.get("/pull_churches",pull_church_callback)
//save

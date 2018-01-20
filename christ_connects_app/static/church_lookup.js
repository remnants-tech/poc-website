var search_name_input_id = document.getElementById("search_name_input");
var search_name_fm = document.getElementById("search_name_fm");
var search_name_input_btn = document.getElementById("search_input_btn");
var church_search_results_id = document.getElementById("church_search_results");
var state_drop_id = document.getElementById("state_dropdown_bar");
var state_drop_ul_id = document.getElementById("state_drop_ul");
var add_church_search_results_id = document.getElementById("add_church_search_results");

function change_marker_position(lat,lng,name) {
    var latlng = new google.maps.LatLng(lat, lng);
    marker.setPosition(latlng);
    map.panTo(latlng);
    map.setCenter(latlng);
    map.setZoom(16);
    infowindow.setContent(name)
}

$(search_name_fm).keypress(
    (event) => {
     if (event.which == '13') {
        event.preventDefault();
      }
});

$(search_name_input_id).keypress(
  (event) => {
    if (event.which == '13') {
       $(search_name_input_btn).click();
     }
  }
)

$(search_name_input_btn).click( () => {
  var cur_input_val = $(search_name_fm).serialize();
  $.ajax({
    url:"/search_church_criteria",
    type:"POST",
    data: cur_input_val,
    success: (church_data) => {
      $(church_search_results_id).html('<p class="h2">Search Results </p>');
      church_data = JSON.parse(church_data);
      if (church_data === "no results found") {
        $(add_church_search_results_id).html("<p>Searched " + search_name_input.value  + " but found no results </p>")
      }
      else {
        var church_name = church_data['name'][0];
        var new_lat = church_data['latitude'][0];
        var new_lng = church_data['longitude'][0];
        change_marker_position(new_lat,new_lng,church_data['name'][0])
        infowindow.open(map,marker);
        $(add_church_search_results_id).html("<p>" + church_name + "</p>" +
                                       "<p>Location: " + church_data['street_address'] + ", " + church_data['state'] + "</p>")
      };
    }
  })
})

//setting up state drop down menu

var states_arr= ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
"South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","American Samoa","District of Columbia","Federated States of Micronesia","Guam","Marshall Islands","Northern Mariana Islands","Palau","Puerto Rico","Virgin Islands"]

for (state_i = 0; state_i < states_arr.length; state_i++){
  var state = states_arr[state_i];
  var modified_state_id = state.replace(/ /g, "_");
  $(state_drop_ul_id).append(
    '<li><a id="'+ modified_state_id + '" data-value="' + state + '" onclick= "change_state_drop_name(' + modified_state_id +  ')">'+ state + '</a></li>')
};

//changing the text of "search by state" drop down bar

var change_state_drop_name = (selected_id) => {
  var selected_state = $(selected_id).attr('data-value');
  console.log(selected_state);
  $(state_drop_id).html(selected_state + ' <span class="caret"></span>');
  $.ajax({
    url:"/search_church_criteria",
    type:"POST",
    data: ($(search_by_state).serialize() + "&" + "state=" + selected_state),
    success: (church_data) => {
      $(church_search_results_id).html('<p class="h2">Search Results </p>');
      church_data = JSON.parse(church_data);
      if (church_data === "no results found") {
        $(add_church_search_results_id).html("<p>Could not find any churches in " + selected_state + "</p>")
      }
      else {
        //for every search results
        for (var church_i = 0; church_i < church_data["church_pk"].length; church_i++){
          var church_name = church_data['name'][church_i];
          var church_street = church_data['street_address'][church_i];
          var church_state = church_data['state'][church_i];
          var new_lat = church_data['latitude'][church_i];
          var new_lng = church_data['longitude'][church_i];
          add_new_marker(new_lat,new_lng,church_name,church_i);
          $(add_church_search_results_id).append("<p><b>" + church_name + "</b></p>" +
                                          "<p>Location: " + church_street + ", " + church_state + "</p><hr />")
        }
      };
   }
 })
}

function add_new_marker(lat, lng, church_name, church_i) {
  if (church_i === 0){
    change_marker_position(lat,lng, church_name);
    infowindow.open(map,marker);
    console.log(lat,lng,church_name);
  }
  else {
    var add_latlng = new google.maps.LatLng(lat, lng);
    var add_marker = new google.maps.Marker({
      position: add_latlng,
      map: map
    })
    var new_window = new google.maps.InfoWindow({
      content: '<div id="content">' + church_name + '</div>'
    })
    new_window.open(map,add_marker)
  };
};

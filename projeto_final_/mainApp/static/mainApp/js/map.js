var mymap;
var address;



$(document).ready(function(){
    mymap = L.map('mapid').setView([38.73, -9.14], 13);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoidW5paG91c2VzIiwiYSI6ImNrbGltdHJxcDBlZWEyd25tYmtkc2xuNmIifQ.hX3RupN9qPRjEJ9oHAFMQg'
    }).addTo(mymap);
    //var marker = L.marker([38.73, -9.14]).addTo(mymap);
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        str = $("#address").val();
        apiCall = formatCall(str);
        $.getJSON(apiCall, function(data) {
          console.log(data.features[0].center);
          lat = data.features[0].center[1];
          long = data.features[0].center[0];
          // JSON result in `data` variable
          var marker = L.marker([lat, long]).addTo(mymap);
      })
        return false;
      }
    })
});

function addMarker(e){
  var newMarker = new L.marker(e.latlng).addTo(mymap);
}

function formatCall(address){
  //takes Adress string returns a string with the correct format of a query to the map box geocoding api
  var formatedQuery = "https://api.mapbox.com/geocoding/v5/mapbox.places/";
  var apiToken = "pk.eyJ1IjoidW5paG91c2VzIiwiYSI6ImNrbGltdHJxcDBlZWEyd25tYmtkc2xuNmIifQ.hX3RupN9qPRjEJ9oHAFMQg";
  const splittedAdress = address.split(" ");
  console.log(splittedAdress);

  for (const word of splittedAdress) {
    formatedQuery += word;
    formatedQuery += "%20";

  }
  formatedQuery += ".json?access_token=";
  formatedQuery += apiToken;
  //https://api.mapbox.com/geocoding/v5/mapbox.places/Los%20Angeles.json?access_token=YOUR_MAPBOX_ACCESS_TOKEN
  return formatedQuery
}

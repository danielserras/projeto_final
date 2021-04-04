var mymap;
var address;
var latLong = false;
var radioClicked = false;

let marker = null;


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

    //Button to place marker clicked
    $("#addMarker").click(function (){addMarkerClick()});
    
    //Radio button clicked
    $("#house_type").click(function (){radioClicked = true; validate()});
    $("#studio_type").click(function (){radioClicked = true; validate()});
    $("#apartment_type").click(function (){radioClicked = true; validate()});
    $("#bedroom_type").click(function (){radioClicked = true; validate()});
  });

function validate(){
  if (latLong && radioClicked){
    $("#placeAndSelectWarning").attr("hidden",true);
    $("#addPropertyNext").attr("disabled",false);
  }else{
    console.log("TA MAL")  
  }
}

function addMarkerClick(){
  str = $("#address").val();
  apiCall = formatCall(str, "normal");
  $.getJSON(apiCall, function(data) {
    console.log(data.features[0].center);
    lat = data.features[0].center[1];
    long = data.features[0].center[0];
    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = long;
    mymap.setView([lat, long], 15);
    // JSON result in `data` variable
    if (marker != null){
      mymap.removeLayer(marker);
    }
    marker = L.marker([lat, long], {
      draggable: true
    }).addTo(mymap);
    marker.on('dragend', function (e) {
      document.getElementById('latitude').value = marker.getLatLng().lat;
      document.getElementById('longitude').value = marker.getLatLng().lng;
      console.log(marker.getLatLng().lat)
      console.log(marker.getLatLng().lng)

      apicall2 = formatCall(marker.getLatLng().lng + " " + marker.getLatLng().lat, "reverse")
      console.log(apicall2)
      $.getJSON(apicall2, function(data2) {
        console.log(data2)
        document.getElementById('address').value = data2.features[0].place_name;
      })
    })
  })
  latLong = true
  validate()
}


function addMarker(e){
  var newMarker = new L.marker(e.latlng).addTo(mymap);
}

function formatCall(address, type){
  //takes Adress string returns a string with the correct format of a query to the map box geocoding api
  var formatedQuery = "https://api.mapbox.com/geocoding/v5/mapbox.places/";
  var apiToken = "pk.eyJ1IjoidW5paG91c2VzIiwiYSI6ImNrbGltdHJxcDBlZWEyd25tYmtkc2xuNmIifQ.hX3RupN9qPRjEJ9oHAFMQg";
  const splittedAdress = address.split(" ");
  console.log(splittedAdress);
  if (type == "normal"){
    for (const word of splittedAdress) {
      formatedQuery += word;
      formatedQuery += "%20";

    }
    formatedQuery = formatedQuery.slice(0, -3);

  }
  else{
    for (const word of splittedAdress) {
      formatedQuery += word;
      formatedQuery += ",";
    }
    formatedQuery = formatedQuery.slice(0, -1);
   
  }
  formatedQuery += ".json?access_token=";
  formatedQuery += apiToken;
  //https://api.mapbox.com/geocoding/v5/mapbox.places/Los%20Angeles.json?access_token=YOUR_MAPBOX_ACCESS_TOKEN
  return formatedQuery
}
//"https://api.mapbox.com/geocoding/v5/mapbox.places/-73.989,40.733.json?access_token=pk.eyJ1IjoidW5paG91c2VzIiwiYSI6ImNrbGltdHJxcDBlZWEyd25tYmtkc2xuNmIifQ.hX3RupN9qPRjEJ9oHAFMQg"
var mymap;
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
});

function addMarker(e){
    var newMarker = new L.marker(e.latlng).addTo(mymap);
}



$(document).ready(function(){
    var l = $('.PassedLats').length;
    var resultLats = [];
    var resultLongs = [];
    for (i = 0; i < l; i++) { 
        resultLats.push($('.PassedLats').eq(i).val());
        resultLongs.push($('.PassedLongs').eq(i).val());
    }
    
    //print the array or use it for your further logic
    console.log(resultLats);
    console.log(resultLongs);
    for (i = 0; i < l; i++) {
        marker = L.marker([resultLats[i], resultLongs[i]], {
            draggable: false
          }).addTo(mymap);
    }


});


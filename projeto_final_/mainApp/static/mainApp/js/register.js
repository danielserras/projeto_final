//minimum age to register is 18yo
function max18yo(d, m, y, date_object) {
    if(d<10){
            d='0'+d
        } 
        if(m<10){
            m='0'+m
        } 

    y = y - 18
    date_object = y+'-'+m+'-'+d;
    document.getElementById("datefield").setAttribute("max", date_object);
}





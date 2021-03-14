var colIndex=0;
var slideIndex=0;
var max 
var min = 0;
$(document).ready(function(){
    var isMouseOverCol = false; 
    var x, y; 
    max = $('#rangeLength').text();
    var scrollCol = $('#sideCol');

    scrollCol.mouseenter(function() {
        x = window.pageXOffset; 
        y = window.pageYOffset; 

        isMouseOverCol = true;
    });

    document.getElementById('sideCol').addEventListener("wheel", function(e) {  
        noWindowScroll(x,y);
        e.preventDefault();
        colIndex = scrollThroughCol (e.deltaY, max, min, colIndex);
    });
});

function noWindowScroll(x,y) { 
    window.scrollTo(x, y); 
}

function scrollThroughCol (direction, max, min, colIndex) {
    //If scrolled down and not at the column bottom
    if(direction > 0 && (colIndex+3)<max){
        $('#col_image_'+colIndex).attr("hidden",true)
        $('#col_image_'+(colIndex+3)).attr("hidden",false)
        colIndex += 1
    }
    //if scrolled up and not at the column top
    else if(direction < 0 && colIndex>min){
        colIndex -= 1
        $('#col_image_'+colIndex).attr("hidden",false)
        $('#col_image_'+(colIndex+3)).attr("hidden",true)
    }
    return colIndex
}

function previous(){
     if(slideIndex > min){
        $('#listingSlides').animate({'margin-left':'+=600px'}, 600)
        slideIndex -= 1
    }
}

function next(){
    if(slideIndex < max-1){
        $('#listingSlides').animate({'margin-left':'-=600px'}, 600)
        slideIndex += 1
    }
}

function slideToImage(id){
    px = 600*(id-slideIndex)
    slideIndex = id
    $('#listingSlides').animate({'margin-left':'-='+px+'px'}, 600)
}
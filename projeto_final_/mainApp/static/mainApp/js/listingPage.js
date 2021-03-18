var colIndex=0;
var slideIndex=0;
var max 
const min = 0;
$(document).ready(function(){
    var isMouseOverCol = false; 
    var x, y; 
    max = $('#rangeLength').text();
    const scrollCol = $('#sideCol');

    scrollReachedBorder()

    scrollCol.mouseenter(function() {
        x = window.pageXOffset; 
        y = window.pageYOffset; 

        isMouseOverCol = true;
    });

    document.getElementById('sideCol').addEventListener("wheel", function(e) {  
        noWindowScroll(x,y);
        e.preventDefault();
        colIndex = scrollThroughCol (e.deltaY);
    });
});

function noWindowScroll(x,y) { 
    window.scrollTo(x, y); 
}

function previousInColumn(){
    scrollThroughCol(-100)
}

function nextInColumn(){
    scrollThroughCol(100)
}

function scrollReachedBorder(){
    if(colIndex==0){
        $('#col_image_btn_up').css('opacity', 0);
    }
    if(max - colIndex < 4){
        $('#col_image_btn_down').css('opacity', 0);
    }
    if(colIndex!=max-3 && colIndex!=0){
        $('#col_image_btn_up').css('opacity', 1);
        $('#col_image_btn_down').css('opacity', 1);
    }
}

function scrollThroughCol (direction) {
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
    scrollReachedBorder()
    return colIndex
}

function previous(){
    slideToImage(slideIndex-1)
}

function next(){
    slideToImage(slideIndex+1)
}

function slideToImage(id){
    let direction = 0
    //Loops the slide
    if(id == min-1){
       id=max-1
    }
    else if(id == max){
        id=min
    }
    //Changes slide depending on the direction
    $('#order_bullet_'+slideIndex).html('<i class="fa fa-circle-o" aria-hidden="true"></i>')
    $('#order_bullet_'+id).html('<i class="fa fa-circle" aria-hidden="true"></i>')
    $('#slidesFigure').animate({'left':'-='+(id-slideIndex)*100+'%'}, 600)
    slideIndex = id
}
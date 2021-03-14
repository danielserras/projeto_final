$(document).ready(function(){
    console.log('controlo')

    var isMouseOverCol = false; 
    var x, y; 
    var i=0;
    var min = 0;
    var max = $('#rangeLength').text();
    var scrollCol = $('#sideCol'); 

    scrollCol.mouseenter(function() {
        x = window.pageXOffset; 
        y = window.pageYOffset; 

        isMouseOverCol = true;
    });

    document.getElementById('sideCol').addEventListener("wheel", function(e) {  
        noWindowScroll(x,y)
        e.preventDefault();
    
        console.log(i, i+3)
        console.log(e)

        if(e.deltaY > 0 && (i+3)<max){
            $('#col_image_'+i).attr("hidden",true)
            $('#col_image_'+(i+3)).attr("hidden",false)
            i += 1
        }
        else if(e.deltaY < 0 && i>=min){
            $('#col_image_'+i).attr("hidden",false)
            $('#col_image_'+(i+3)).attr("hidden",true)
            i -= 1
        }
    });
});

function noWindowScroll(x,y) { 
    window.scrollTo(x, y); 
}
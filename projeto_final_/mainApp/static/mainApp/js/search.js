$(document).ready(function() {

    function list_redirect(container){
        var container_img = container[1];
        var img_url = container_img.src.slice(22);
        var patt = /[1-9]/;
        var id_location = img_url.search(patt);
        var listing_id = 0;
        console.log(img_url.slice(24));
        for (var c=id_location; c<img_url.length; c++){
            
            if (isNaN(img_url.slice(c,c+1))){
                listing_id = img_url.slice(id_location, c);
                break;
            }
        }

        window.location.href = "listing/"+listing_id;

    }
    $(".imageDiv").click(function(){
        list_redirect($(this).find("img"));
    })
    //Show/Hide advanced search at button press
    document.querySelector('.advancedSearchFormButton').addEventListener('click', function() {
        console.log($("#advancedSearchDiv").css('display'));
        if ($("#advancedSearchDiv").css('display') === 'none') {
            console.log('hello');
            $("#advancedSearchDiv").css('display', 'block');
            console.log($("#advancedSearchDiv").css('display'));
        } else {
            $("#advancedSearchDiv").css('display', 'none');
        }

        this.classList.toggle('rotated');
    });
    //Range bar for rent. Search page
    const ShiftLeftValues = { '2': '0,1', '3': '-0.2', '4': '-0.5', '5': '-0.8', '7': '-1.8' };
    var v = [550, 1200];
    var numTooClose = 150;
    var r = 20;
    if ($(window).width() < 960) {
        var numTooClose = 200;
    }
    if ($(window).width() < 480) {
        var numTooClose = 350;
    }
    $("#slider").slider({
        range: true,
        min: 0,
        max: 2000,
        values: v,
        slide: function(event, ui) {
            if ((ui.values[1] - ui.values[0]) < numTooClose) {
                $('#minPrice').val(ui.values[0])
                $('#maxPrice').val(ui.values[1])
                $("#labelMin").css('display', 'none');
                $("#labelMax").css('display', 'none');
                $("#labelMinToMax").css('display', 'block');
                $("#labelMinToMax").css('left', ((ui.values[0] + ui.values[1]) / (r * 2)) - 4.5 + "%").text(ui.values[0] + '€ até ' + ui.values[1] + '€');
            } else {
                $('#minPrice').val(ui.values[0])
                $('#maxPrice').val(ui.values[1])
                $("#labelMinToMax").css('display', 'none');
                $("#labelMin").css('margin-left', ShiftLeftValues[$("#labelMin").text().length] + 'em').css('display', 'block');
                $("#labelMax").css('margin-left', ShiftLeftValues[$("#labelMax").text().length] + 'em').css('display', 'block');
                $("#labelMin").css('left', (ui.values[0] / r) + "%").text(ui.values[0] + '€');
                if (ui.values[1] == 2000) {
                    $("#labelMax").css('left', (ui.values[1] / r) + "%").text(ui.values[1] + '€ +');
                } else {
                    $("#labelMax").css('left', (ui.values[1] / r) + "%").text(ui.values[1] + '€');
                }
            }
        },
        create: function(event, ui) {
            $('#minPrice').val(v[0])
            $('#maxPrice').val(v[1])
            $("#labelMin").css('left', v[0] / r + "%").text(v[0] + '€').css('margin-left', '-0.5em');
            $("#labelMax").css('left', v[1] / r + "%").text(v[1] + '€').css('margin-left', '-0.8em');
        }
    });
});
$(document).ready(function() {
    //agreement
    $("#agreementAcceptCheckbox").click(function() {
        if ($(this).prop("checked") == true) {
            $("#agreementAccept").prop("disabled", false);
        } else if ($(this).prop("checked") == false) {
            $("#agreementAccept").prop("disabled", true);
        }
    });
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
                $("#labelMin").css('display', 'none');
                $("#labelMax").css('display', 'none');
                $("#labelMinToMax").css('display', 'block');
                $("#labelMinToMax").css('left', ((ui.values[0] + ui.values[1]) / (r * 2)) - 4.5 + "%").text(ui.values[0] + '€ até ' + ui.values[1] + '€');
            } else if (ui.values[1] == 2000) {
                $("#labelMin").css('display', 'block');
                $("#labelMax").css('display', 'block');
                $("#labelMinToMax").css('display', 'none');
                $("#labelMin").css('left', (ui.values[0] / r) + "%").text(ui.values[0] + '€');
                $("#labelMax").css('left', (ui.values[1] / r) + "%").text(ui.values[1] + '€ +');
            } else {
                $("#labelMin").css('display', 'block');
                $("#labelMax").css('display', 'block');
                $("#labelMinToMax").css('display', 'none');
                $("#labelMin").css('left', (ui.values[0] / r) + "%").text(ui.values[0] + '€');
                $("#labelMax").css('left', (ui.values[1] / r) + "%").text(ui.values[1] + '€');
            }
        },
        create: function(event, ui) {
            $("#labelMin").css('left', v[0] / r + "%").text(v[0] + '€');
            $("#labelMax").css('left', v[1] / r + "%").text(v[1] + '€');
            $("#labelMinToMax").css('left', ((ui.values[0] + ui.values[1]) / (r * 2)) - 4 + "%").text(ui.values[0] + '€ até ' + ui.values[1] + '€');
            $("#labelMinToMax").css('display', 'none');
        }
    });
});
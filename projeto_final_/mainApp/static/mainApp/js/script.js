$(document).ready(function() {
    //agreement
    $("#agreementAccept").click(function() {
        if ($(this).prop("checked") == true) {
            $("#agreementSubmit").prop("disabled", false);
        } else if ($(this).prop("checked") == false) {
            $("#agreementSubmit").prop("disabled", true);
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

    var v = [550, 1500];
    $("#slider").slider({
        range: true,
        min: 0,
        max: 2500,
        values: v,
        slide: function(event, ui) {
            if ((ui.values[1] - ui.values[0]) < 150) {
                $("#labelMin").css('display', 'none');
                $("#labelMax").css('display', 'none');
                $("#labelMinToMax").css('display', 'block');
                $("#labelMinToMax").css('left', ((ui.values[0] + ui.values[1]) / 50) - 4 + "%").text(ui.values[0] + '€ até ' + ui.values[1] + '€');
            } else {
                $("#labelMin").css('display', 'block');
                $("#labelMax").css('display', 'block');
                $("#labelMinToMax").css('display', 'none');
                $("#labelMin").css('left', ui.values[0] / 25 + "%").text(ui.values[0] + '€');
                $("#labelMax").css('left', ui.values[1] / 25 + "%").text(ui.values[1] + '€');
            }
        },
        create: function(event, ui) {
            $("#labelMin").css('left', v[0] / 25 + "%").text(v[0] + '€');
            $("#labelMax").css('left', v[1] / 25 + "%").text(v[1] + '€');
            $("#labelMinToMax").css('left', ((ui.values[0] + ui.values[1]) / 50) - 4 + "%").text(ui.values[0] + '€ até ' + ui.values[1] + '€');
            $("#labelMinToMax").css('display', 'none');
        }
    });
});
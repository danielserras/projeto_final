$(document).ready(function(){
    /* addListing */
    var pageListing = 1;
    var bedroomsNum = 1;
    var bathroomsNum = 1;
    var livingroomsNum = 0;
    var kitchensNum = 1;
    /* var imgSlots = 0;

    $(".addImg").click(function(){
        imgSlots++;
        addimgSlot(imgSlots);
    }) */

    /* $('.num_divisions').hide();
    $('.studio_type, .bedroom_type').click(function(){
        $('.num_divisions').hide();
        $('#bedroomsNum').attr('value', 1);
        $('#bathroomsNum').attr('value', 1);
        $('#kitchensNum').attr('value', 1);
        $('#livingroomsNum').attr('value', 0);
    })

    $('.apartment_type, .residency_type, .house_type').click(function(){
        $('.num_divisions').show();
    }) */

    /* if ($(".studio_type").prop('checked')){
        $("#roomsLabel").hide();
        $("#bedroomsNum").hide();
        $("#bedroomsNum").val("1");
    }
    
    if ($(".bedroom_type").prop('checked')){
        $("#roomsLabel").hide();
        $("#bedroomsNum").hide();
        $("#bedroomsNum").val("1");
    } */

    $('.studio_type, .bedroom_type').click(function(){
        $("#roomsLabel").hide();
        $("#bedroomsNum").hide();
        $("#bedroomsNum").val("1");
    })

    $('.house_type, .apartment_type').click(function(){
        $("#roomsLabel").show();
        $("#bedroomsNum").show();
        $("#bedroomsNum").val("");
    })

    if (!$(".multiple_form").is(":hidden")){

        $(".listing_form").show();
        $(".multiple_form_next").click(function(){
            var whole = $('.whole');
            var separate = $('.separate');
            
            if (separate.prop('checked')){
                /* $(".multiple_form").attr("method", "POST");
                $(".multiple_form_next").attr("type", "submit");
                $(".multiple_form").submit(); */
                $('<input>').attr({type: 'hidden',name: 'separate', id: 'sep'}).appendTo('.listing_form');
                $("#sep").val("1");
            }
            $(".listing_form").show();
            $(".multiple_form").remove();
        
    })
    }

    if(window.location.href.includes("propertyEditing")){
        addMarkerClick();
    }

})


/* function addimgSlot(slots) {

    let imgFormContainer = $(".imgF");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[0];
    let imgFormNum = slots-1;

    let newForm = imgFormContainer.children()[4].cloneNode(true);

    imgFormNum++;
    newForm.setAttribute('id', 'id_form-'+imgFormNum.toString()+'-images');
    newForm.setAttribute('name', `form-${imgFormNum.toString()}-images`);
    imgFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = imgFormNum+1;
} */


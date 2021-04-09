$(document).ready(function(){
    /* addListing */
    var pageListing = 1;
    var bedroomsNum = 1;
    var bathroomsNum = 1;
    var livingroomsNum = 0;
    var kitchensNum = 1;
    var imgSlots = 0;

    $(".addImg").click(function(){
        imgSlots++;
        addimgSlot(imgSlots);
    })

    $('.num_divisions').hide();
    $('.studio_type, .bedroom_type').click(function(){
        $('.num_divisions').hide();
        $('#bedroomsNum').attr('value', 1);
        $('#bathroomsNum').attr('value', 1);
        $('#kitchensNum').attr('value', 1);
        $('#livingroomsNum').attr('value', 0);
    })

    $('.apartment_type, .residency_type, .house_type').click(function(){
        $('.num_divisions').show();
    })

    if (!$(".multiple_form").is(":hidden")){

        $(".listing_form").hide();
        $(".multiple_form_next").click(function(){
            var whole = $('.whole');
            var separate = $('.separate');
            
            if (separate.prop('checked')){
                /* $(".multiple_form").attr("method", "POST");
                $(".multiple_form_next").attr("type", "submit");
                $(".multiple_form").submit(); */
                $('<input>').attr({type: 'hidden',name: 'separate', value: '1'}).appendTo('.listing_form');
            }
            $(".listing_form").show();
            $(".multiple_form").remove();
        
    })
    }
    

    /* $(".separate").click(function(){
        window.location.href = "/mainApp/profile/propertiesManagement"
    })
 */
    $("#backPageListing").hide();
    $("#submitListing").hide();
    $("*[class*='pageListing-']").hide();
    $(".pageListing-"+pageListing).show();

    $("#submitListing").click(function(){
        $("#propertyForm").submit();
        setTimeout(function(){
            $("#bedroomForm").submit();
            $("#bathroomForm").submit();
            $("#kitchenForm").submit();
            $("#listingForm").submit();
            if(livingroomsNum > 0){
                $("#livingroomForm").submit();
            }
        }, 1000);
    })
    $("#nextPageListing").click(function(){
        $(".pageListing-"+pageListing).hide();
        pageListing ++;
        $(".pageListing-"+pageListing).show();
        $("#backPageListing").show();
        $("#nextPageListing").show();
        $("#submitListing").hide();
        if(pageListing == 3){
            console.log('entrou2')
            //addBedroomsHtml(bedroomsNum);
            for (let i = 1; i < bedroomsNum; i++){
                addFormBedroom();
            }
            
        }
        if(pageListing == 4){
            //addBathroomsHtml(bathroomsNum);
            for (let j = 1; j < bathroomsNum; j++){
                addFormBathroom();
            }
        }
        if(pageListing == 5){
            //addKitchensHtml(kitchensNum);
            //console.log(kitchensNum)
            for (let k = 1; k < kitchensNum; k++){
                addFormKitchen();
            }
        }
        if(pageListing == 6){
            if(livingroomsNum > 0){
                //addLivingroomsHtml(livingroomsNum,"#pageListing-6");
                for (let k = 1; k < livingroomsNum; k++){
                    addFormLiving();
                }
            }
            else{
                //addAgreementInfoHtml("#pageListing-6");
                $(".pageListing-7").show();
                $(".pageListing-6").html("")
                $("#nextPageListing").hide();
                $("#submitListing").show();
            }
        }
        if(pageListing == 7){
            //addAgreementInfoHtml("#pageListing-7");
            $("#nextPageListing").hide();
            $("#submitListing").show();
        }

    })
    $("#backPageListing").click(function(){
        $("#nextPageListing").show();
        $(".pageListing-7").hide();
        $(".pageListing-"+pageListing).hide();
        pageListing --;
        $(".pageListing-"+pageListing).show();
        $("#submitListing").hide();
        if(pageListing == 1){
            $("#backPageListing").hide();
        }
        if(pageListing == 3){
            //addBedroomsHtml(bedroomsNum);
        }
        if(pageListing == 4){
            //addBathroomsHtml(bathroomsNum);
        }
        if(pageListing == 5){
            //addKitchensHtml(kitchensNum);
        }
        if(pageListing == 6){
            if(livingroomsNum > 0){
                //addLivingroomsHtml(livingroomsNum, "#pageListing-6");
            }
            else{
                //addAgreementInfoHtml("#pageListing-6");
                $("nextPageListing").hide();
                $("#submitListing").show();
            }
        }
        if(pageListing == 7){
            addAgreementInfoHtml("#pageListing-7");
        }
    })

    $("#bedroomsNum").change(function(){
        bedroomsNum = $(this).val();
    })

    $("#bathroomsNum").change(function(){
        bathroomsNum = $(this).val();
    })

    $("#livingroomsNum").change(function(){
        livingroomsNum = $(this).val();
        if(livingroomsNum == 0){
            $("#pagelisting-6").html('');
        }        
    })

    $("#kitchensNum").change(function(){
        kitchensNum = $(this).val();
    })

    $(".container").on("click", ".bedroomHideShow",function(){
        $(this).parent().next().toggle()
    })

    $(".container").on("click", ".bathroomHideShow",function(){
        $(this).parent().next().toggle()
    })

    $(".container").on("click", ".kitchenHideShow",function(){
        $(this).parent().next().toggle()
    })
    $(".container").on("click", ".livingroomHideShow",function(){
        $(this).parent().next().toggle()
    })

})



function addFormBedroom() {
    //e.preventDefault()
    let bedroomForm = $(".bedroomF");
    let bedroomFormContainer = $(".pageListing-3");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[0];
    let bedroomFormNum = bedroomForm.length-1;

    let newForm = bedroomForm[0].cloneNode(true);//Clone the bedroom form
    let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

    bedroomFormNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${bedroomFormNum}-`) //Update the new form to have the correct form number
    bedroomFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = bedroomFormNum+1; //Increment the number of total forms in the management form
    console.log(bedroomFormNum+1);
    console.log($('[id=id_form-TOTAL_FORMS]'));
}

function addFormBathroom() {
    //e.preventDefault()
    let bathroomForm = $(".bathroomF");
    let bathroomFormContainer = $(".pageListing-4");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[1];
    let bathroomFormNum = bathroomForm.length-1
    
    let newForm = bathroomForm[0].cloneNode(true);//Clone the bathroom form
    let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

    bathroomFormNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${bathroomFormNum}-`) //Update the new form to have the correct form number
    bathroomFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = bathroomFormNum+1 //Increment the number of total forms in the management form
}

function addFormKitchen() {
    //e.preventDefault()
    let kitchenForm = $(".kitchenF");
    let kitchenFormContainer = $(".pageListing-5");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[2];
    let kitchenFormNum = kitchenForm.length-1

    let newForm = kitchenForm[0].cloneNode(true);//Clone the kitchen form
    let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

    kitchenFormNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${kitchenFormNum}-`) //Update the new form to have the correct form number
    kitchenFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = kitchenFormNum+1 //Increment the number of total forms in the management form

}

function addFormLiving() {
    //e.preventDefault()
    let livingroomForm = $(".livingroomF");
    let livingroomFormContainer = $(".pageListing-5");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[3];
    let livingroomFormNum = livingroomForm.length-1

    let newForm = livingroomForm[0].cloneNode(true);//Clone the livingroom form
    let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

    livingroomFormNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${livingroomFormNum}-`) //Update the new form to have the correct form number
    livingroomFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = livingroomFormNum+1 //Increment the number of total forms in the management form
    
}

function addimgSlot(slots) {

    let imgFormContainer = $(".imgF");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[0];
    let imgFormNum = slots-1;

    let newForm = imgFormContainer.children()[4].cloneNode(true);

    imgFormNum++;
    newForm.setAttribute('id', 'id_form-'+imgFormNum.toString()+'-images');
    newForm.setAttribute('name', `form-${imgFormNum.toString()}-images`);
    imgFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = imgFormNum+1;
}


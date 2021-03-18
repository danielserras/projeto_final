$(document).ready(function () {
    var bedForm = $(".bedroomF");
    var addButton = $("#addBedroom");
    var totalForms = $("[id=id_form-TOTAL_FORMS]")[0];

    var formNum = bedForm.length-1

    addButton.click(function (e) { 
        e.preventDefault();
        let newForm = bedForm.children()[5].cloneNode(true);
        let formRegex = RegExp(`form-(\\d){1}-`,'g');
        let formRegex2 = RegExp(`value="(\\d)"{1}`,'g');
        let formRegex3 = RegExp(`Quarto (\\d){1}`,'g');
        let bedroomNum = parseInt(totalForms.getAttribute("value")) + 1 ;

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replaceAll("checked","")
        newForm.innerHTML = newForm.innerHTML.replace(formRegex2, `value="0"`);
        newForm.innerHTML = newForm.innerHTML.replace(formRegex3, `Quarto ${bedroomNum}`);

        $("#buttonsDiv").before(newForm)
        
        totalForms.setAttribute('value', `${formNum+1}`)
        
    });

    var removeButton = $(".removeBedroom");

    /* removeButton.click(function(){
        console.log("SIMMMM")
    }) */
});
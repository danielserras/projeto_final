$(document).ready(function () {
    var kitchenForm = $(".kitchenF");
    var addButton = $("#addKitchen");
    var totalForms = $("[id=id_form-TOTAL_FORMS]")[0];

    var formNum = kitchenForm.length-1

    addButton.click(function (e) { 
        e.preventDefault();
        let propertyId = window.location.href.split("/")[7]
        let newForm = kitchenForm.children()[1].cloneNode(true);
        let formRegex = RegExp(`form-(\\d+){1}-`,'g');
        let formRegex2 = RegExp(`value="(\\d+)"{1}`,'g');
        let formRegex3 = RegExp(`Cozinha (\\d+){1}`,'g');
        let formRegex4 = RegExp(`deleteKitchen/(\\d+){1}/(\\d+){1}`, 'g');
        let kitchenNum = parseInt(totalForms.getAttribute("value")) + 1 ;

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replaceAll("checked","")
        newForm.innerHTML = newForm.innerHTML.replace(formRegex2, `value="0"`);
        newForm.innerHTML = newForm.innerHTML.replace(formRegex3, `Cozinha ${kitchenNum}`);
        newForm.innerHTML = newForm.innerHTML.replace("disabled","");
        newForm.innerHTML = newForm.innerHTML.replace(formRegex4, `deleteKitchen/${propertyId}/`);
        newForm.innerHTML = newForm.innerHTML.replace("Tem que ter no mínimo uma cozinha", "");
        $("#buttonsDiv").before(newForm)
        
        totalForms.setAttribute('value', `${formNum+1}`)
        
    });

});
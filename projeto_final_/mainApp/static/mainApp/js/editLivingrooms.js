$(document).ready(function () {
    var livingroomForm = $(".livingroomF");
    var addButton = $("#addLivingroom");
    var totalForms = $("[id=id_form-TOTAL_FORMS]")[0];

    var formNum = livingroomForm.length-1

    addButton.click(function (e) { 
        e.preventDefault();
        let propertyId = window.location.href.split("/")[7]
        let newForm = livingroomForm.children()[1].cloneNode(true);
        let formRegex = RegExp(`form-(\\d+){1}-`,'g');
        let formRegex2 = RegExp(`value="(\\d+)"{1}`,'g');
        let formRegex3 = RegExp(`Sala (\\d+){1}`,'g');
        let formRegex4 = RegExp(`deleteLivingroom/(\\d+){1}/(\\d+){1}`, 'g');
        let bathroomNum = parseInt(totalForms.getAttribute("value")) + 1 ;

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replaceAll("checked","")
        newForm.innerHTML = newForm.innerHTML.replace(formRegex2, `value="0"`);
        newForm.innerHTML = newForm.innerHTML.replace(formRegex3, `Sala ${bathroomNum}`);
        newForm.innerHTML = newForm.innerHTML.replace("disabled","");
        newForm.innerHTML = newForm.innerHTML.replace(formRegex4, `deleteLivingroom/${propertyId}/`);
        $("#buttonsDiv").before(newForm)
        
        totalForms.setAttribute('value', `${formNum+1}`)
        
    });

});
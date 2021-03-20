$(document).ready(function () {
    var bathFrom = $(".bathroomF");
    var addButton = $("#addBathroom");
    var totalForms = $("[id=id_form-TOTAL_FORMS]")[0];

    var formNum = bathFrom.length-1

    addButton.click(function (e) { 
        e.preventDefault();
        let newForm = bathFrom.children()[1].cloneNode(true);
        console.log(bathFrom.children())
        let formRegex = RegExp(`form-(\\d){1}-`,'g');
        let formRegex2 = RegExp(`value="(\\d)"{1}`,'g');
        let formRegex3 = RegExp(`Casa de Banho (\\d){1}`,'g');
        let bathroomNum = parseInt(totalForms.getAttribute("value")) + 1 ;

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replaceAll("checked","")
        newForm.innerHTML = newForm.innerHTML.replace(formRegex2, `value="0"`);
        newForm.innerHTML = newForm.innerHTML.replace(formRegex3, `Casa de Banho ${bathroomNum}`);
        newForm.innerHTML = newForm.innerHTML.replace("disabled","");

        $("#buttonsDiv").before(newForm)
        
        totalForms.setAttribute('value', `${formNum+1}`)
        
    });

});
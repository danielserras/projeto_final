$(document).ready(function () {
    var bedForm = $(".bedroomF");
    var addButton = $("#addBedroom");
    var totalForms = $("[id=id_form-TOTAL_FORMS]")[0];

    var formNum = bedForm.length-1

    addButton.click(function (e) { 
        e.preventDefault();
        let propertyId = window.location.href.split("/")[7]
        let newForm = bedForm.children()[5].cloneNode(true);
        let formRegex = RegExp(`form-(\\d+){1}-`,'g');
        let formRegex2 = RegExp(`value="(\\d+)"{1}`,'g');
        let formRegex3 = RegExp(`Quarto (\\d+){1}`,'g');
        let formRegex4 = RegExp(`deleteBedroom/(\\d+){1}/(\\d+){1}`, 'g');
        let bedroomNum = parseInt(totalForms.getAttribute("value")) + 1 ;

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replaceAll("checked","")
        newForm.innerHTML = newForm.innerHTML.replace(formRegex2, `value="0"`);
        newForm.innerHTML = newForm.innerHTML.replace(formRegex3, `Quarto ${bedroomNum}`);
        newForm.innerHTML = newForm.innerHTML.replace("disabled","");
        newForm.innerHTML = newForm.innerHTML.replace(formRegex4, `deleteBedroom/${propertyId}/`);
        newForm.innerHTML = newForm.innerHTML.replace("Não é possível remover quartos que estejam anunciados", "");
        newForm.innerHTML = newForm.innerHTML.replace("Tem que ter no mínimo um quarto", "");
        $("#buttonsDiv").before(newForm)
       
        totalForms.setAttribute('value', `${formNum+1}`)
        
    });

});
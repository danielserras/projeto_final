$(document).ready(function () {
    var imgSlots = 0;
    $(".addImg").click(function(){
        console.log("ENTREI1")
        imgSlots++;
        addimgSlot(imgSlots);
    })
});

function addimgSlot(slots) {

    /* let imgFormContainer = $(".imgF");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[0];
    let imgFormNum = slots-1;
    let newForm = imgFormContainer.children().cloneNode(true);
    console.log(newForm)

    imgFormNum++;
    newForm.setAttribute('id', 'id_form-'+imgFormNum.toString()+'-images');
    newForm.setAttribute('name', `form-${imgFormNum.toString()}-images`);
    imgFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = imgFormNum+1; */
    let imgFormContainer = $(".imgF");
    let totalForms = $('[id=id_form-TOTAL_FORMS]')[0];
    let imgFormNum = slots-1;

    let newForm = imgFormContainer.children()[5].cloneNode(true);

    imgFormNum++;
    newForm.setAttribute('id', 'id_form-'+imgFormNum.toString()+'-images');
    newForm.setAttribute('name', `form-${imgFormNum.toString()}-images`);
    newForm.value='';
    imgFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = imgFormNum+1;
}
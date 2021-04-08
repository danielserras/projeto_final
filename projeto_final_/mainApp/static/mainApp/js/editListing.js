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
    let newForm = imgFormContainer.children()[4].cloneNode(true);

    imgFormNum++;
    newForm.childNodes[1].innerHTML = '';
    newForm.childNodes[3].childNodes[1].setAttribute('id', 'id_form-'+imgFormNum.toString()+'-images');
    newForm.childNodes[3].childNodes[1].setAttribute('name', `form-${imgFormNum.toString()}-images`);
    newForm.childNodes[3].childNodes[1].value='';
    imgFormContainer.append(newForm) //Insert the new form at the end of the list of forms

    totalForms.value = imgFormNum+1;
}

function upload_img(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            //input.before('<div class="col-sm-4"><img id="img_id" class="img-thumbnail" src="'+e.target.result+'" alt="your image" /></div>" />');
            let image = document.createElement("img")
            image.setAttribute("class", "img-thumbnail")
            image.src = e.target.result
            console.log(input.parentElement.parentElement.childNodes[1])
            input.parentElement.parentElement.childNodes[1].innerHTML='';
            input.parentElement.parentElement.childNodes[1].append(image);
        }

        reader.readAsDataURL(input.files[0]);
        //$(".addImg").click();
    }
}
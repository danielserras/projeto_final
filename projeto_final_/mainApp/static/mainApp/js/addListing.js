$(document).ready(function(){
    /* addListing */
    var pageListing = 1;
    var bedroomsNum = 0;
    var bathroomsNum = 1;
    var livingroomsNum = 0;
    var kitchensNum = 0;

    $("#backPageListing").hide();
    $("*[class*='pageListing-']").hide();
    $(".pageListing-"+pageListing).show();

    $("#nextPageListing").click(function(){
        $(".pageListing-"+pageListing).hide();
        pageListing ++;
        $(".pageListing-"+pageListing).show();
        $("#backPageListing").show();
        if(pageListing == 3){
            addBedroomsHtml(bedroomsNum);
        }
        if(pageListing == 4){
            addBathroomsHtml(bathroomsNum);
        }

    })
    $("#backPageListing").click(function(){
        $(".pageListing-"+pageListing).hide();
        pageListing --;
        $(".pageListing-"+pageListing).show();
        if(pageListing == 1){
            $("#backPageListing").hide();
        }
        if(pageListing == 3){
            addBedroomsHtml(bedroomsNum);
        }
        if(pageListing == 4){
            addBathroomsHtml(bathroomsNum);
        }
    })

    $("#bedroomsNum").change(function(){
        bedroomsNum = $(this).val();
    })

    $("#bathroomsNum").change(function(){
        bathroomsNum = $(this).val();
        console.log("Bathrooms: " + bathroomsNum)
    })

    $("#livingroomsNum").change(function(){
        livingroomsNum = $(this).val();
        console.log("Livingrooms: " + livingroomsNum)
    })

    $("#kitchensNum").change(function(){
        kitchensNum = $(this).val();
        console.log("Kitchens: " + kitchensNum)
    })

    $("#bedroomsInfo").on("click", ".bedroomHideShow",function(){
        console.log("CLICOU")
        $(this).parent().next().toggle()
    })

})

function addBedroomsHtml(n){
    $("#bedroomsInfo").html("")
    for (let i = 0; i < n; i++) {
        $("#bedroomsInfo").append('<div class="row mt-2 mb-2 justify-content-md-center">\
                                    <button class="btn bg-transparent col-sm-7 bedroomHideShow">Quarto 1</button>\
                                </div>\
                                <div class="row justify-content-md-center mb-2">\
                                    <div class="col-sm-7">\
                                        <div class="row">\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="heater" id="">\
                                                <label class="checkbox-inlines" for="heater">Aquecedor</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="airCondition" id="">\
                                                <label for="airCondition">Ar Condicionado</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="chair" id="">\
                                                <label for="chair">Cadeira</label>\
                                            </div>\
                                        </div>\
                                        <div class="row">\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="privateBathroom" id="">\
                                                <label for="privateBathroom">Casa de Banho privada</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="chestOfDrawers" id="">\
                                                <label for="chestOfDrawers">Cómoda</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="wardrope" id="">\
                                                <label for="wardrope">Guarda Roupa</label>\
                                            </div>\
                                        </div>\
                                        <div class="row">\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="window" id="">\
                                                <label for="window">Janela</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="desk" id="">\
                                                <label for="desk">Secretária</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="sofa" id="">\
                                                <label for="sofa">Sofá</label>\
                                            </div>\
                                        </div>\
                                        <div class="row">\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="sofaBed" id="">\
                                                <label for="sofaBed">Sofá-cama</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="tv" id="">\
                                                <label for="tv">Tv</label>\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <input type="checkbox" name="balcony" id="">\
                                                <label for="balcony">Varanda</label>\
                                            </div>\
                                        </div>\
                                        <div class="row">\
                                            <div class="col-sm-4">\
                                                <label for="doubleBeds">Camas de Casal</label>\
                                                <input type="number" name="doubleBeds" id="">\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <label for="singleBeds">Camas de Solteiro</label>\
                                                <input type="number" name="singleBeds" id="">\
                                            </div>\
                                            <div class="col-sm-4">\
                                                <label for="maximumOccupation">Ocupação Máxima </label>\
                                                <input type="number" name="maximumOccupation" id="">\
                                            </div>\
                                        </div>\
                                    </div>\
                                </div>');
    }
}

function addBathroomsHtml(n){
    $("#bathroomsInfo").html("");
    for(let i = 0; i < n; i++){
        $("#bathroomsInfo").append('<div class="row mt-2 mb-2 justify-content-md-center">\
                                        <button class="btn bg-transparent col-sm-7 bathroomHideShow">Casa de Banho</button>\
                                    </div>\
                                    <div class="row justify-content-md-center mb-2" id="bedroom-1">\
                                        <div class="col-sm-7">\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="heater" id="">\
                                                    <label class="checkbox-inlines" for="heater">Banheira</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="airCondition" id="">\
                                                    <label for="airCondition">Chuveiro</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="chair" id="">\
                                                    <label for="chair">Janela</label>\
                                                </div>\
                                            </div>\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="privateBathroom" id="">\
                                                    <label for="privateBathroom">Lavatório</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="chestOfDrawers" id="">\
                                                    <label for="chestOfDrawers">Sanita</label>\
                                                </div>\
                                            </div>\
                                        </div>\
                                    </div>')
    }
}
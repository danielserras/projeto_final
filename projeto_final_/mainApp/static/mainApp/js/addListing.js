$(document).ready(function(){
    /* addListing */
    var pageListing = 1;
    var bedroomsNum = 1;
    var bathroomsNum = 1;
    var livingroomsNum = 0;
    var kitchensNum = 1;

    $("#backPageListing").hide();
    $("#submitListing").hide();
    $("*[class*='pageListing-']").hide();
    $(".pageListing-"+pageListing).show();

    $("#nextPageListing").click(function(){
        $(".pageListing-"+pageListing).hide();
        pageListing ++;
        $(".pageListing-"+pageListing).show();
        $("#backPageListing").show();
        $("#nextPageListing").show();
        if(pageListing == 3){
            addBedroomsHtml(bedroomsNum);
        }
        if(pageListing == 4){
            addBathroomsHtml(bathroomsNum);
        }
        if(pageListing == 5){
            addKitchensHtml(kitchensNum);
        }
        if(pageListing == 6){
            if(livingroomsNum > 0){
                addLivingroomsHtml(livingroomsNum,"#pageListing-6");
            }
            else{
                addAgreementInfoHtml("#pageListing-6");
                $("#nextPageListing").hide();
                $("#submitListing").show();
            }
        }
        if(pageListing == 7){
            addAgreementInfoHtml("#pageListing-7");
            $("#nextPageListing").hide();
            $("#submitListing").show();
        }

    })
    $("#backPageListing").click(function(){
        $("#nextPageListing").show();
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
        if(pageListing == 5){
            addKitchensHtml(kitchensNum);
        }
        if(pageListing == 6){
            if(livingroomsNum > 0){
                addLivingroomsHtml(livingroomsNum, "#pageListing-6");
            }
            else{
                addAgreementInfoHtml("#pageListing-6");
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
            $(element).html('');
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

function addBedroomsHtml(n){
    $("#pageListing-3").html("")
    for (let i = 0; i < n; i++) {
        $("#pageListing-3").append('<div class="row mt-2 mb-2 justify-content-md-center">\
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
    $("#pageListing-4").html("");
    for(let i = 0; i < n; i++){
        $("#pageListing-4").append('<div class="row mt-2 mb-2 justify-content-md-center">\
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

function addKitchensHtml(n){
    $("#pageListing-5").html("");
    for(let i = 0; i < n; i++){
        $("#pageListing-5").append('<div class="row mt-2 mb-2 justify-content-md-center">\
                                        <button class="btn bg-transparent col-sm-7 kitchenHideShow">Cozinha</button>\
                                    </div>\
                                    <div class="row justify-content-md-center mb-2">\
                                        <div class="col-sm-7">\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="chairs" id="">\
                                                    <label class="checkbox-inlines" for="chairs">Cadeiras</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="freezer" id="">\
                                                    <label for="freezer">Congelador</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="cooker" id="">\
                                                    <label for="cooker">Fogão</label>\
                                                </div>\
                                            </div>\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="oven" id="">\
                                                    <label for="oven">Forno</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="fridge" id="">\
                                                    <label for="fridge">Frigorífico</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="window" id="">\
                                                    <label for="waindow">Janela</label>\
                                                </div>\
                                            </div>\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="diswasher" id="">\
                                                    <label for="dishwasher">Máquina de Lavar Loiça</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="washingMachine" id="">\
                                                    <label for="washingMachine">Máquina de Lavar Roupa</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="dryer" id="">\
                                                    <label for="dryer">Máquina de Secar Roupa</label>\
                                                </div>\
                                            </div>\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="table" id="">\
                                                    <label for="table">Mesa</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="microwave" id="">\
                                                    <label for="microwave">Microondas</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="pansAndPots" id="">\
                                                    <label for="pansAndPots">Panelas e Frigideiras</label>\
                                                </div>\
                                            </div>\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="dishesAndCutlery" id="">\
                                                    <label for="dishesAndCutlery">Pratos e Talheres</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="balcony" id="">\
                                                    <label for="balcony">Varanda</label>\
                                                </div>\
                                            </div>\
                                        </div>\
                                    </div>');
    }
}

function addLivingroomsHtml(n, element){
    $(element).html("");
    for(let i = 0; i < n; i++){
        $(element).append('<div class="row mt-2 mb-2 justify-content-md-center">\
                                        <button class="btn bg-transparent col-sm-7 livingroomHideShow">Sala</button>\
                                    </div>\
                                    <div class="row justify-content-md-center mb-2">\
                                        <div class="col-sm-7">\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="chairs" id="">\
                                                    <label class="checkbox-inlines" for="chairs">Cadeiras</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="window" id="">\
                                                    <label for="window">Janela</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="table" id="">\
                                                    <label for="table">Mesa</label>\
                                                </div>\
                                            </div>\
                                            <div class="row">\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="sofa" id="">\
                                                    <label for="sofa">Sofá</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="sofaBed" id="">\
                                                    <label for="sofaBed">Sofá-Cama</label>\
                                                </div>\
                                                <div class="col-sm-4">\
                                                    <input type="checkbox" name="balcony" id="">\
                                                    <label for="balcony">Varanda</label>\
                                                </div>\
                                            </div>\
                                        </div>\
                                    </div>')
    }
}

function addAgreementInfoHtml(element){
    $(element).html('');
    $(element).append('<div class="row mt-2 mb-2 justify-content-md-center">\
                        <div class="col-sm-7">\
                            <h3>Outras informações</h3>\
                        </div>\
                    </div>\
                    <div class="row justify-content-md-center mb-2">\
                        <div class="col-sm-7">\
                            <div class="row">\
                                <div class="col-sm-12">\
                                    <label for="title">Título:</label>\
                                    <input type="text" name="Title" >\
                                </div>\
                            </div>\
                            <div class="row">\
                                <div class="col-sm-12">\
                                    <label for="description">Descrição:</label>\
                                    <textarea name="description"  rows="6" class="w-100"></textarea>\
                                </div>\
                            </div>\
                            <div class="row">\
                                <div class="col-sm-6">\
                                    <label for="availabilityStarts">Disponível de:</label>\
                                    <input type="date" name="availabilityStarts" >\
                                </div>\
                                <div class="col-sm-6">\
                                    <label for="availabilityEnds">até:</label>\
                                    <input type="date" name="availabilityEndss" >\
                                </div>\
                            </div>\
                            <div class="row">\
                                <div class="col-sm-6">\
                                    <label for="rentAmount">Renda:</label>\
                                    <input type="number" name="rentAmount"  min="0">\
                                </div>\
                                <div class="col-sm-6">\
                                    <label for="securityDeposit">Caução:</label>\
                                    <input type="number" name="securityDeposit"  min="0">\
                                </div>\
                            </div>\
                            <div class="row">\
                                <div class="col-sm-6">\
                                    <label for="cleaningServices">Frequência dos Serviçoes de limpeza:</label>\
                                    <input type="text" name="cleaningServices" >\
                                </div>\
                                <div class="col-sm-6">\
                                    <label for="maxCapacity">Ocupação máxima:</label>\
                                    <input type="number" name="maxCapacity"  min="1">\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                    \
                    <div class="row mt-2 mb-2 justify-content-md-center">\
                        <div class="col-sm-7">\
                            <h3>Regras</h3>\
                        </div>\
                    </div>\
                    <div class="row justify-content-md-center mb-2">\
                        <div class="col-sm-7">\
                            <div class="row">\
                                <div class="col-sm-4">\
                                    <input type="checkbox" name="pets" >\
                                    <label for="pets">Animais de Estimação</label>\
                                </div>\
                                <div class="col-sm-4">\
                                    <input type="checkbox" name="smoke" >\
                                    <label for="smoke">Fumar</label>\
                                </div>\
                                <div class="col-sm-4">\
                                    <input type="checkbox" name="overnightVisits" >\
                                    <label for="overnightVisits">Visitas podem pernoitar ocasionalmente</label>\
                                </div>\
                            </div>\
                            <div class="row">\
                                <div class="col-sm-4">\
                                    <label for="allowedGender">Género Permitido</label>\
                                    <select name="allowedGender" >\
                                        <option value="Ambos">Ambos</option>\
                                        <option value="onlyWomens">Apenas Mulheres</option>\
                                        <option value="onlyMens">Apenas Homens</option>\
                                    </select>\
                                </div>\
                            </div>\
                            <div class="row">\
                                <div class="col-sm-4">\
                                    <label for="securityDeposit">Caução</label>\
                                    <input type="number" name="securityDeposit" >\
                                </div>\
                                <div class="col-sm-4">\
                                    <label for="occupacity">Lotação máxima</label>\
                                    <input type="number" name="securityDeposit" >\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                    \
                    <div class="row mt-2 mb-2 justify-content-md-center">\
                        <div class="col-sm-7">\
                            <h3>Despesas Incluídas</h3>\
                        </div>\
                    </div>\
                    <div class="row justify-content-md-center mb-2">\
                        <div class="col-sm-7">\
                            <div class="row">\
                                <div class="col-sm-3">\
                                    <input type="checkbox" name="water" >\
                                    <label for="water">Água</label>\
                                </div>\
                                <div class="col-sm-3">\
                                    <input type="checkbox" name="eletrecity" >\
                                    <label for="eletrecity">Eletrecidade</label>\
                                </div>\
                                <div class="col-sm-3">\
                                    <input type="checkbox" name="internet" >\
                                    <label for="internet">Internet</label>\
                                </div>\
                                <div class="col-sm-3">\
                                    <input type="checkbox" name="gas" >\
                                    <label for="gas">Gás</label>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                    \
                    <div class="row mt-2 mb-2 justify-content-md-center">\
                        <div class="col-sm-7">\
                            <h3>Exterior</h3>\
                        </div>\
                    </div>\
                    <div class="row justify-content-md-center mb-2">\
                        <div class="col-sm-7">\
                            <div class="row">\
                                <div class="col-sm-4">\
                                    <input type="checkbox" name="streetParking" >\
                                    <label for="streetParking">Estacionamento</label>\
                                </div>\
                                <div class="col-sm-4">\
                                    <input type="checkbox" name="garage" >\
                                    <label for="garage">Garagem</label>\
                                </div>\
                                <div class="col-sm-4">\
                                    <input type="checkbox" name="garden" >\
                                    <label for="garden">Jardim</label>\
                                </div>\
                            </div>\
                        </div>\
                    </div>')

}
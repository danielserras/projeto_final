$(document).ready(function(){
    /* addListing */
    var pageListing = 1;
    var bedroomsNum = 0;
    var bathroomsNum = 1;
    var livingroomsNum = 0;
    var kitchensNum = 0;

    $("*[class*='pageListing-']").hide();
    $(".pageListing-"+pageListing).show();

    $("#nextPageListing").click(function(){
        $(".pageListing-"+pageListing).hide();
        pageListing ++;
        $(".pageListing-"+pageListing).show();
        $("#backPageListing").show();

    })
    $("#backPageListing").click(function(){
        $(".pageListing-"+pageListing).hide();
        pageListing --;
        $(".pageListing-"+pageListing).show();
        if(pageListing == 1){
            $("#backPageListing").hide();
        }
    })

    $("#bedroomsNum").change(function(){
        bedroomsNum = $(this).val();
        console.log("Bedrooms: " + bedroomsNum);
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
})
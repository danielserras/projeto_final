$(document).ready(function () {
    $(".star").hover(
        function() {
            num = $(this).attr('id').split("-")[1]
            for (let i = num[0]+0; i <= $(this).attr('id').split("-")[1]; i++) {
                $("#star-"+i).find('path').attr("fill-opacity","1")
            }
        },
        function() {
            num = $(this).attr('id').split("-")[1]
            for (let i = num[0]+0; i <= $(this).attr('id').split("-")[1]; i++) {
                $("#star-"+i).find('path').attr("fill-opacity","0.3")
            }
        }
    )
    $(".star").click(
        function() {
            num = $(this).attr('id').split("-")[1]
            for (let i = num[0]+0; i <= num[0]+5; i++) {
                $("#star-"+i).find('path').removeClass("clicked-path");
                $("#star-"+i).find('path').attr("fill-opacity","0.3")
            }
            for (let i = num[0]+0; i <= $(this).attr('id').split("-")[1]; i++) {
                $("#star-"+i).find('path').addClass("clicked-path");
                $("#starsInput-" + i.toString().charAt(0)).val(Number(i.toString().charAt(1)))
                console.log($("#starsInput-" + i.toString().charAt(0)).val())
            }
        }
    );
    $("#submit_review").on("click", function(){
        let valid = true;
        $('[required]').each(function() {
            if ($(this).is(':invalid') || !$(this).val()) valid = false;
        })
        if (!valid){
            $("#reviewWarningRow").attr("hidden", false);
        } 
    })
});
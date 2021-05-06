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
});
const fiveStepsMeasuresArray = [-1.5, 22, 45, 72, 99]
const sixStepsMeasuresArray = [-1.5, 18, 35, 57, 78, 99]
var measuresArray;
var stepDistancing = 0

$(document).ready(function(){
    
    const numSteps = $("#numberOfSteps").html();
    const stepLabels = getStepLabels();
    const completedSteps = $("#numberOfCompletedSteps").html();
    var calcDistance = (100/(numSteps-1))*(completedSteps-1);
    
    if(numSteps == 5){
        measuresArray = fiveStepsMeasuresArray;
    } else{
        measuresArray = sixStepsMeasuresArray;
    };
    if(completedSteps == 1){
        $("#stepBarDiv").append("<div class='completedStep' style='left:"+ stepDistancing +"%;'></div>");
        stepDistancing += 100/(numSteps-1);
    }
    for (let i = 0; i < measuresArray.length; i++) {
        $("#stepBarDiv").append("<p class='stepLabel' style='left:"+ measuresArray[i]+"%;'>"+stepLabels[i]+"</p>");
    }
    for (let i = 0; i < completedSteps-1; i++) {
        $("#stepBarDiv").append("<div class='completedStep' style='left:"+ stepDistancing +"%;'></div>");
        stepDistancing += 100/(numSteps-1);
    }

    $("#stepBarDiv").append("<div class='stepLine'></div>");
    $(".stepLine").width((100/(numSteps-1)*(completedSteps-2)+"%"));

    setTimeout(function(){ 
        $(".stepLine").animate({width: calcDistance+"%"}, 1000);
    }, 100);
    setTimeout(function(){ 
        $("#stepBarDiv").append("<div class='completedStep' style='left:"+ calcDistance +"%;'></div>");
    }, 1120);

    for (let i = 0; i < numSteps - completedSteps; i++) {
        $("#stepBarDiv").append("<div class='emptyStep' style='left:"+ stepDistancing +"%;'></div>");
        stepDistancing += 100/(numSteps-1);
    }
    
});

function getStepLabels(){
    let labelsHTML = $("#labelsList").html();
    let stepLabels = labelsHTML.split(",");
    return stepLabels
}
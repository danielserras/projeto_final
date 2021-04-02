const fiveStepsMeasuresArray = [-1.5, 22, 45, 72, 99]
const sixStepsMeasuresArray = [-1.5, 18, 35, 57, 78, 99]
var measuresArray;
var stepDistancing = 0

$(document).ready(function(){
    
    const numSteps = $("#numberOfSteps").html();
    const stepLabels = getStepLabels();
    const completedSteps = $("#numberOfCompletedSteps").html();
    
    if(numSteps == 5){
        measuresArray = fiveStepsMeasuresArray;
    } else{
        measuresArray = sixStepsMeasuresArray;
    };
    for (let i = 0; i < measuresArray.length; i++) {
        $("#stepBarDiv").append("<p class='stepLabel' style='left:"+ measuresArray[i]+"%;'>"+stepLabels[i]+"</p>");
    }
    for (let i = 0; i < completedSteps; i++) {
        $("#stepBarDiv").append("<div class='completedStep' style='left:"+ stepDistancing +"%;'></div>");
        stepDistancing += 100/(numSteps-1);
    }
    console.log(stepDistancing - (100/(numSteps-1)));
    $("#stepBarDiv").append("<div class='stepLine' style='width:"+ (stepDistancing - (100/(numSteps-1))) +"%;'></div>");
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
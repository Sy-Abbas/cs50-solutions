function tigger(event)
{
    var buttons = document.getElementsByClassName("mulC");
    for (var  x= 0; x<buttons.length;x++)
    {
        buttons[x].style.backgroundColor = "";
    }
    var trigger = event.srcElement;
    if (trigger.innerHTML === "Hydrogen Sulphide")
    {
        document.getElementById("error").innerHTML = "Correct";
        trigger.style.backgroundColor = "#00FF00";
        document.getElementById("error").style.color = "#00FF00";
    } 
    else
    {
        document.getElementById("error").innerHTML = "Wrong";
        trigger.style.backgroundColor = "#FF0000";
        document.getElementById("error").style.color = "#FF0000";
    }
}
function tigger2(event)
{
    var buttons = document.getElementsByClassName("mulC");
    for (var  x= 0; x<buttons.length;x++)
    {
        buttons[x].style.backgroundColor = "";
    }
    var trigger = event.srcElement;
    if (trigger.innerHTML === "Bromine")
    {
        document.getElementById("error2").innerHTML = "Correct";
        trigger.style.backgroundColor = "#00FF00";
        document.getElementById("error2").style.color = "#00FF00";
    } 
    else
    {
        document.getElementById("error2").innerHTML = "Wrong";
        trigger.style.backgroundColor = "#FF0000";
        document.getElementById("error2").style.color = "#FF0000";
    }
}

function enter(event){
    if (event.key === "Enter"){
        freeResponse();
    }
}
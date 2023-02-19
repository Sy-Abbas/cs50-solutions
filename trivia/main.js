function tigger(event)
{
    var buttons = document.getElementsByClassName("mulC");
    for (var  x= 0; x<buttons.length;x++)
    {
        buttons[x].style.backgroundColor = "";
    }
    var trigger = event.srcElement;
    if (trigger.innerHTML === "5")
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
function freeResponse()
{
    var answer = document.getElementById("ans").value.toLowerCase();
    if (answer === "eye" || answer === "eyes")
    {
        document.getElementById("2nderror").innerHTML = "Correct";
        document.getElementById("2nderror").style.color = "#00FF00";
    }
    else
    {
        document.getElementById("2nderror").innerHTML = "Wrong";
        document.getElementById("2nderror").style.color = "#FF0000";
    }
}

function enter(event){
    if (event.key === "Enter"){
        freeResponse();
    }
}
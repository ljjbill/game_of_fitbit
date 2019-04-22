$(document).ready(function(){
    var empt = document.getElementById('calouput').innerHTML;
    if (empt == null || empt == "") {}
    else if (empt == "Error: incorrect input!") {  $("#output2").modal('show');}
    else {  $("#output").modal('show');} 
});
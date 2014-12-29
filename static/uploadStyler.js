var path = "";
var fileName = "";

$(document).ready(function(){
    $("#FileInputButton").on("click",function (e){
        e.preventDefault();
        $("#FileInput").trigger("click");
    });
    $("#FileInput").on("change",function(){
        path = $(this).val();
        path = path.split("\\");
        fileName = path[path.length - 1];
        $("#FileNameDisplay").text(fileName);
    });
});
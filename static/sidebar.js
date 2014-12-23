var sidebarOut = true;
var contentWidth = "83.7%";
var contentResize = true;

$(document).ready(function(){
    $(window).resize(function() {
        $("#SideBar").height(window.innerHeight - $("#Titlebox").height());
        $("#Content").height((window.innerHeight - $("#Titlebox").height()) - (window.innerHeight/100));
        $("#SideToggle").height($("#Titlebox").height());
        $("#SideToggle").width($("#SideToggle").height());
        $("#Titlebox").css({textIndent: $("#SideToggle").width()})
    });
    
    $(window).resize();
    
    $("#SideToggle").click(function(){
        if (sidebarOut){
            $("#SideBar").hide("slide", { direction: "left" }, 500,function(){
                if (contentResize){
                    $("#Content").animate({width: "99%"},500);
                }
                sidebarOut = false;
            });
        }
        else{
            if (contentResize) {
                $("#Content").animate({width: contentWidth},500,function(){
                    $("#SideBar").show("slide", { direction: "left" }, 500);
                });
            }
            else {
                $("#SideBar").show("slide", { direction: "left" }, 500);
            }
            sidebarOut = true;
        }
    }); 
});

function percentage (total, percent){
    return (total / 100) * percent;
}

function checkSidebar() {
    if (sidebarOut) {
        $("#SideBar").show("slide", { direction: "left" }, 500,function(){
            if (contentResize){
                $("#Content").animate({width: contentWidth},500);
            }
        });
    }
    else {
        $("#SideBar").hide("slide", { direction: "left" }, 500,function(){
            if (contentResize){
                $("#Content").animate({width: "99%"},500);
            }
            sidebarOut = false;
        });
    }
}
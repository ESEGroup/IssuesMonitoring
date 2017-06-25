//JS para o toggle entre uma view e outra:

function show_view() {
    $("#view1").toggle(400);
    $("#view2").toggle(400);
}

$(document).ready(function(){
    $("#switch-view-reload").click(function(){
        var anchor = document.getElementById("view2");
        location.hash = "#" + anchor.getAttribute("anchor");
        location.reload();
    });
    $("#switch-back-reload").click(function(){
        location.hash = "";
        location.reload();
    });
    $("#switch-view").click(function(){
        show_view();
    });
    $("#switch-back").click(function(){
        show_view();
    });

    var anchor = document.getElementById("view2");
    if (location.hash === "#" + anchor.getAttribute("anchor")) {
        show_view();
    }
});

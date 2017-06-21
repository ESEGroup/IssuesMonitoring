//JS para o toggle entre uma view e outra:

function show_first_view() {
    $("#view1").toggle(400);
    $("#view2").toggle(400);
}

function show_last_view() {
    $("#view1").toggle(400);
    $("#view2").toggle(400);
}

$(document).ready(function(){
    $("#switch-view").click(function(){
        var anchor = document.getElementById("view2");
        location.hash = "#" + anchor.getAttribute("anchor");
        location.reload();
    });
    $("#switch-back").click(function(){
        location.hash = "";
        location.reload();
    });

    var anchor = document.getElementById("view2");
    if (location.hash === "#" + anchor.getAttribute("anchor")) {
        show_first_view();
    }
});

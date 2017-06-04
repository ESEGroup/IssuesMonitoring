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
        show_first_view();
    });
    $("#switch-back").click(function(){
        show_last_view();
    });
});

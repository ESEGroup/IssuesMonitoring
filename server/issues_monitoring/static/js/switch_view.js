//JS para o toggle entre uma view e outra:

$(document).ready(function(){
    $("#switch-view").click(function(){
        $("#view1").toggle(400);
        $("#view2").toggle(400);
    });
    $("#switch-back").click(function(){
        $("#view1").toggle(400);
        $("#view2").toggle(400);
    });
});

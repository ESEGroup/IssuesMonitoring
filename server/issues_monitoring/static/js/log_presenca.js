//JS para o toggle entre usuarios presentes e log de presenca:

$(document).ready(function(){
    $("#switch-view").click(function(){
        $("#hidden-log").toggle(400);
        $("#membros-presentes").toggle(400);
    });
    $("#switch-back").click(function(){
        $("#hidden-log").toggle(400);
        $("#membros-presentes").toggle(400);
    });
});

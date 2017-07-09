//JS para o toggle entre uma view e outra:

function show_view() {
    //Esconde mensagens de erro/sucesso/aviso:
    $(".js-message").css("display", "none");
    //Troca a view:
    $("#view1").toggle(400);
    $("#view2").toggle(400);
}

$(document).ready(function(){
    $("#switch-view-reload").click(function(){
        var path = location.pathname;
        path = location.pathname.split("?")[0]
        window.history.pushState('', '', path);
        var anchor = document.getElementById("view2");
        location.hash = "#" + anchor.getAttribute("anchor");
        location.reload();
    });
    $("#switch-back-reload").click(function(){
        var path = location.pathname;
        path = location.pathname.split("?")[0]
        window.history.pushState('', '', path);
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

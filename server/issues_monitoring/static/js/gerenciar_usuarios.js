$(function() {
    var del = document.getElementsByClassName("delete-btn");
    console.log(del.length);
    for (var i = 0; i < del.length; ++i) {
        del[i].addEventListener("click", function(ev) {
            var nome = ev.target.getAttribute("data-nome"),
                url = ev.target.getAttribute("data-url");
            if (confirm("Deseja apagar o usuário " + nome + "?")) {
                ajax(url);
            }
        });
    }

    var alt = document.getElementsByClassName("alter-btn")
    console.log(alt.length);
    for(var i = 0; i<alt.length; ++i){
        alt[i].addEventListener("click", function(ev){
            var nome = ev.target.getAttribute("data-nome"),
                url = ev.target.getAttribute("data-url");
            ajax_get(url);
        });
    }
});

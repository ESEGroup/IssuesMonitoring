$(function() {
    var del = document.getElementsByClassName("delete-btn");
    for (var i = 0; i < del.length; ++i) {
        del[i].addEventListener("click", function(ev) {
            var nome = ev.target.getAttribute("data-nome"),
                url = ev.target.getAttribute("data-url");
            if (confirm("Deseja apagar o usuário " + nome + "?")) {
                ajax(url);
            }
        });
    }
});

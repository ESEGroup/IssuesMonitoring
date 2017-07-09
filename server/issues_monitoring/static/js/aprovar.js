$(function(){
    var salvar = document.getElementById("salvar")

    if (salvar != null && typeof(salvar) != "undefined") {
        salvar.addEventListener("click", function(ev) {
            var checkboxes = document.getElementsByClassName("aprovar");
            for (var i = 0; i < checkboxes.length; ++i) {
                var url = checkboxes[i].getAttribute("data-url"),
                    checked = checkboxes[i].checked;
                options = {url: url, method: "POST", data: {"aprovar": checked}}

                if (i+1 === checkboxes.length) {
                    options["error"] = function() {
                        var path = location.pathname;
                        path = location.pathname.split("?")[0] + "?e=Falha ao atualizar informações!";
                        window.history.pushState('', '', path);
                        location.reload();
                    };
                    options["success"] = function() {
                        var path = location.pathname;
                        path = location.pathname.split("?")[0] + "?c=Informações salvas com sucesso!";
                        window.history.pushState('', '', path);
                        location.reload();
                    };
                }

                $.ajax(options);
            }
        });
    }
});

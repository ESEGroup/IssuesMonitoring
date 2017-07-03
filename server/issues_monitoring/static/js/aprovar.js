$(function(){
    var salvar = document.getElementById("salvar")

    if (salvar != null && typeof(salvar) != "undefined") {
        salvar.addEventListener("click", function(ev) {
            var checkboxes = document.getElementsByClassName("aprovar");
            for (var i = 0; i < checkboxes.length; ++i) {
                $.ajax({
                    url: checkboxes[i].getAttribute("data-url"),
                    method: "POST",
                    data: {"aprovar": checkboxes[i].checked}
                });
            }
            var path = location.pathname;
            path = location.pathname.split("?")[0]
            window.history.pushState('', '', path);
            location.reload();
        });
    }
});

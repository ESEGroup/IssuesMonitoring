$(function(){
    var salvar = document.getElementById("salvar")
        
    if salvar != null and typeof(salvar) != "undefined" {
        salvar.addEventListener("click", function(ev) {
            var checkboxes = document.getElementsByClassName("aprovar");
            for (var i = 0; i < checkboxes.length; ++i) {
                $.ajax({
                    url: checkboxes[i].getAttribute("data-url"),
                    method: "POST",
                    data: {"aprovar": checkboxes[i].checked}
                });
            }
        });
    }
});

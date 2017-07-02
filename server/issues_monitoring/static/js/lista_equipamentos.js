$(function() {

    //JS para os sliders de dois handles presentes em cadastrar lab:
    $("#slider-temp").slider({
        range: true,
        min: 0,
        max: 100,
        values: [ 20, 40 ],
        slide: function(ev, ui ) {
            $("#temp-lab").val(ui.values[0] + "ºC a " + ui.values[1] + "ºC");
            $("#temp-min").val(ui.values[0]);
            $("#temp-max").val(ui.values[1]);
        }
    });
    $("#temp-min").val(20);
    $("#temp-max").val(40);
    $("#temp-lab").val($("#slider-temp").slider("values", 0) + "ºC a " + $("#slider-temp").slider("values", 1) + "ºC");

    var del = document.getElementsByClassName("delete-btn");
    for (var i = 0; i < del.length; ++i) {
        del[i].addEventListener("click", function(ev) {
            var mac = ev.target.getAttribute("data-mac"),
                url = ev.target.getAttribute("data-url");
            if (confirm("Deseja apagar o equipamento de endereço " + mac + "?")) {
                ajax(url);
            }
        });
    }

    var alt = document.getElementsByClassName("alter-btn")
    console.log(alt.length);
    for(var i = 0; i<alt.length; ++i){
        alt[i].addEventListener("click", function(ev){
            var mac = ev.target.getAttribute("data-mac"),
                url = ev.target.getAttribute("data-url");
            ajax_get(url);
            
        });
    }

    // JS para os radiobutton
    var comp_radio         = document.getElementById("comp_radio");
    var ardu_radio         = document.getElementById("ardu_radio");
    var div_select_arduino = document.getElementById("div_select_arduino");
    var select_arduino     = document.getElementById("select_arduino");
    var parent_id          = document.getElementById("parent_id");
    ardu_radio.addEventListener("click", function(ev) {
        div_select_arduino.className += " hidden";
        parent_id.value = 0;
    });

    comp_radio.addEventListener("click", function(ev) {
        div_select_arduino.className = div_select_arduino.className.replace(" hidden", "");
    });

    select_arduino.addEventListener("change", function(ev) {
        parent_id.value = ev.target.value;
    });
});

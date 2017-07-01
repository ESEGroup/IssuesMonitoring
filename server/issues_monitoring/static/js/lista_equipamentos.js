//JS para os input radios escondidos dos arduinos:
$(document).ready(function(){
    $('input[type=radio][name=radio-1]').change(function() {
        $(".hidden-radio").slideToggle(300);
        $(".hidden-zona-conforto").slideToggle(300);
    });

    $('input[type=radio][name=radio-arduino]').change(function() {
        $('#parent-id').val( $('input[name=radio-arduino]:checked', "#register-form").val() );
    });
});

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

    // JS para os radiobutton
    var ardu_radio               = document.getElementById("ardu-radio");
    var parent_id                = document.getElementById("parent-id");
    var inner_radio_arduino_list = document.getElementsByClassName("inner-radio");
    ardu_radio.addEventListener("click", function(ev) {
        parent_id.value = 0;
    });

});

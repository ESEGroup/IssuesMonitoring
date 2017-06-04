//JS para os sliders de dois handles presentes em cadastrar lab:

$(function() {
    $("#slider-temp").slider({
        range: true,
        min: 10,
        max: 50,
        values: [$("#temp-min").val(), $("#temp-max").val()],
        slide: function(ev, ui ) {
            $("#temp-lab").val(ui.values[0] + "ºC a " + ui.values[1] + "ºC");
            $("#temp-min").val(ui.values[0]);
            $("#temp-max").val(ui.values[1]);
        }
    });
    $("#temp-lab").val($("#slider-temp").slider("values", 0) + "ºC a " + $("#slider-temp").slider("values", 1) + "ºC");
} );

$(function() {
    $("#slider-umidade").slider({
        range: true,
        min: 0,
        max: 100,
        values: [$("#umid-min").val(), $("#umid-max").val()],
        slide: function( event, ui ) {
            $("#umidade-lab").val(ui.values[0] + "% a " + ui.values[1] + "%");
            $("#umid-min").val(ui.values[0]);
            $("#umid-max").val(ui.values[1]);
        }
    });
    $("#umidade-lab").val($("#slider-umidade").slider("values", 0) + "% a " + $("#slider-umidade").slider("values", 1) + "%");
});

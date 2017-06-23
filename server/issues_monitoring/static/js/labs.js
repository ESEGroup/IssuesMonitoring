//JS para os sliders de handle unico presentes em cadastrar lab:

var rangeSlider = function(){
  var slider = $('.range-slider'),
      range = $('.range-slider__range'),
      value = $('.range-slider__value');
    
  slider.each(function(){

    value.each(function(){
      var value = $(this).prev().attr('value');
      $(this).html(value);
    });

    range.on('input', function(){
      $(this).next(value).html(this.value);
    });
  });
};

$(function() {
    rangeSlider();

    //JS para os sliders de dois handles presentes em cadastrar lab:
    $("#slider-temp").slider({
        range: true,
        min: 10,
        max: 50,
        values: [ 20, 30 ],
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
        values: [ 10, 60 ],
        slide: function( event, ui ) {
            $("#umidade-lab").val(ui.values[0] + "% a " + ui.values[1] + "%");
            $("#umid-min").val(ui.values[0]);
            $("#umid-max").val(ui.values[1]);
        }
    });
    $("#umidade-lab").val($("#slider-umidade").slider("values", 0) + "% a " + $("#slider-umidade").slider("values", 1) + "%");
});


//JS para o RModal (popup):

window.onload = function () {

    //MODAL PARA EXCLUIR LABORATORIO:

    var modalExcluirLab = new RModal(document.getElementById('delete-popup'));

    //Adiciona um event listener aos botoes de excluir laboratorio:

    var evExcluirLabFunc = function (ev) {
        ev.preventDefault();
        modalExcluirLab.open();
    };
    
    $(".delete-btn").click(function (ev) {
        ev.preventDefault();
        modalExcluirLab.open();
    });

    window.modalExcluirLab = modalExcluirLab;
}

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
    $("#temp-min").val(20);
    $("#temp-max").val(30);
    $("#temp-lab").val($("#slider-temp").slider("values", 0) + "ºC a " + $("#slider-temp").slider("values", 1) + "ºC");

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
    $("#umid-min").val(10);
    $("#umid-max").val(60);
    $("#umidade-lab").val($("#slider-umidade").slider("values", 0) + "% a " + $("#slider-umidade").slider("values", 1) + "%");

    var del = document.getElementsByClassName("delete-btn");
    for (var i = 0; i < del.length; ++i) {
        del[i].addEventListener("click", function(ev) {
            var lab_nome = ev.target.getAttribute("data-lab-nome"),
                url = ev.target.getAttribute("data-url");
            if (confirm("Deseja apagar o laboratório " + lab_nome + "?")) {
                ajax(url);
            }
        });
    }
});

//JS para o toggle entre escolher lab e cadastrar lab:

$(document).ready(function(){
    $("#switch-view").click(function(){
        $("#hidden-form").toggle(400);
        $("#escolher-lab").toggle(400);
    });
    $("#switch-back").click(function(){
        $("#hidden-form").toggle(400);
        $("#escolher-lab").toggle(400);
    });
});

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

rangeSlider();

//JS para os sliders de dois handles presentes em cadastrar lab:

$( function() {
    $( "#slider-temp" ).slider({
        range: true,
        min: 10,
        max: 50,
        values: [ 20, 30 ],
        slide: function( event, ui ) {
            $( "#temp-lab" ).val( ui.values[ 0 ] + "ºC a " + ui.values[ 1 ] + "ºC" );
        }
    });
    $( "#temp-lab" ).val($( "#slider-temp" ).slider( "values", 0 ) + "ºC a " + $( "#slider-temp" ).slider( "values", 1 ) + "ºC");
} );

$( function() {
    $( "#slider-umidade" ).slider({
        range: true,
        min: 0,
        max: 100,
        values: [ 20, 30 ],
        slide: function( event, ui ) {
            $( "#umidade-lab" ).val( ui.values[ 0 ] + "% a " + ui.values[ 1 ] + "%" );
        }
    });
    $( "#umidade-lab" ).val($( "#slider-umidade" ).slider( "values", 0 ) + "% a " + $( "#slider-umidade" ).slider( "values", 1 ) + "%");
} );

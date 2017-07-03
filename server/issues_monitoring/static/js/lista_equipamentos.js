//JS para os input radios escondidos dos arduinos:
$(document).ready(function(){

    //Mostra o submenu de cadastro de computador:
    $('input[type=radio][name=radio-1]').change(function() {
        $(".hidden-radio").slideToggle(300);
        $(".hidden-zona-conforto").slideToggle(300);
        //Seta o id escolhid de acordo se for Arduino (0) ou Equipamento (id do equipamento):
        if ( $("#parent-id").val() == "0" ){
            $("#parent-id").val( $("#select-arduino").val() );
        } else {
            $("#parent-id").val("0");
        };
    });

    //Atualiza o parent id caso escolha outra opcao de arduino:
    $('#select-arduino').change(function() {
        $('#parent-id').val( $("#select-arduino").val() );
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

    //Adiciona os on clicks no botao de deletar:
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

    //Adiciona os on clicks no botao de alterar:
    var alt = document.getElementsByClassName("alter-btn")
    for(var i = 0; i<alt.length; ++i){
        alt[i].addEventListener("click", function(ev){
            var mac = ev.target.getAttribute("data-mac"),
                url = ev.target.getAttribute("data-url");
            ajax_get(url);

        });
    }

});

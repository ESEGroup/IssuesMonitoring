//JS para os input radios escondidos de Temperatura e Umidade:
$(document).ready(function(){
    $('input[type=radio][name=chart_type]').change(function() {
        $(".hidden-select").slideToggle(300);
    });
    
    //Tira a mensagem de erro do historico:
    var path = location.pathname;
    path = location.pathname.split("?")[0]
    window.history.pushState('', '', path);
});

//JS para o slider de handle unico:
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

//JS pro restante da pagina:
$(function() {
    //Ativa o slider de handle unico:
    rangeSlider();

    //Declara o objeto do datetimepicker (e faz com que o datepicker atualize os inputs correspondentes quando selecionado):
    var datetimepickerInit = {
        dateFormat: 'yy-m-d',
        timeFormat: "hh:mm tt",
        inline: true,
        onSelect: function(dateText, inst) {
            var date = $(this).datepicker('getDate'),
                day  = date.getDate(),
                month = date.getMonth() + 1,
                year =  date.getFullYear();
                hours = date.getHours();
                minutes = date.getMinutes();
            if ( $(this).attr('id') == 'datepicker-start'){
                $('#start-date').val( day + '/' + month + '/' + year + ' ' + hours + ':' + minutes + ':0');
            } else if ( $(this).attr('id') == 'datepicker-end'){
                $('#end-date').val( day + '/' + month + '/' + year + ' ' + hours + ':' + minutes + ':0');
            }
            $('#daterange').val( $('#start-date').val() + " - " + $('#end-date').val() );
        }
    };

    //Atribui os valores iniciais de hoje e ontem aos datepickers:
    $('#datepicker-start').datetimepicker(datetimepickerInit);
    datetimepickerInit["defaultDate"] = 1;
    $('#datepicker-end').datetimepicker(datetimepickerInit);


    //Inicializa o campo daterange com o intervalo entre hoje e amanha:
    var date = new Date();
    var today_string = date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
    //Adiciona uma unidade do dia:
    date.setDate(date.getDate() + 1);
    var tomorrow_string = date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
    $('#start-date').val(today_string + ' 00:00:00')
    $('#end-date').val(tomorrow_string + ' 00:00:00')
    //Une os dois valores:
    $('#daterange').val( $('#start-date').val() + " - " + $('#end-date').val() );

});

function showModal()
{
    // Get the modal
    var modal = document.getElementById('myModal');

    modal.style.display = "block";

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function drawIssuesChart(mydata, title){

    function drawChart() {
        $(".curve-chart").slideToggle(300);
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'index');
        data.addColumn('number', 'Média');
        data.addColumn({id: 'min', type:'number', role: 'interval'});
        data.addColumn({id: 'max', type:'number', role: 'interval'});

        data.addRows(mydata);

        var options = {
            title:'Gráfico - ' + title,
            height: 600,
            curveType:'function',
            lineWidth: 4,
            series: [{'color': '#D3362D'}],
            intervals: { 'lineWidth':2, 'barWidth': 0.5 },
            legend: 'none'
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve-chart'));

        document.getElementById('curve-chart').setAttribute('style','');
        chart.draw(data, options);
    }

    if (mydata.length > 0) {
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);
    } else {
        document.getElementById('curve-chart').remove();
        document.getElementById('warning-chart').style = "";
    }
}

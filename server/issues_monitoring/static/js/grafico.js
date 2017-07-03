//JS para os input radios escondidos de Temperatura e Umidade:
$(document).ready(function(){
    $('input[type=radio][name=chart_type]').change(function() {
        $(".hidden-select").slideToggle(300);
    });
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


    //Inicializa o campo daterange com o intervalo entre hoje e ontem:
    var date = new Date();
    var today_string = date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
    //Subtrai uma unidade do dia:
    date.setDate(date.getDate() - 1);
    var yesterday_string = date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
    $('#start-date').val(yesterday_string + ' 00:00:00')
    $('#end-date').val(today_string + ' 00:00:00')
    //Une os dois valores:
    $('#daterange').val( $('#start-date').val() + " - " + $('#end-date').val() );
    //Inicializa o date-picker de ontem:
    $("#datepicker-start").datetimepicker({ defaultDate: -1 });



});

function drawIssuesChart(mydata, type){

    function drawChart() {
        $(".curve-chart").slideToggle(300);
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'index');
        data.addColumn('number', 'Média');
        data.addColumn({id: 'min', type:'number', role: 'interval'});
        data.addColumn({id: 'max', type:'number', role: 'interval'});

        data.addRows(mydata);

        var options = {
            title:'Gráfico - ' + type,
            width: 680,
            height: 300,
            curveType:'function',
            lineWidth: 4,
            series: [{'color': '#D3362D'}],
            intervals: { 'lineWidth':2, 'barWidth': 0.5 },
            legend: 'none',
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

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
    
    
    $("#datepicker-start").datetimepicker({
        onSelect: function() { 
            $("#start-date").val( $(this).datepicker({ dateFormat: 'dd-mm-yy' }).val() ); 
        }
    });
    
    $("#datepicker-end").datetimepicker({
        onSelect: function() { 
            $("#end-date").val( $(this).datepicker({ dateFormat: 'dd-mm-yy' }).val() ); 
        }
    });
    
    //Ativa o datepicker:
    $("#datepicker-start").datetimepicker();
    $("#datepicker-end").datetimepicker();

    
/*
    //JS referente ao grafico:
    $('input[type=radio][name=chart_type]').on('change', function(){
        console.log($(this).val());
        if ($(this).val() == "temperatura"){
            $('.equips').remove();
            var equips = JSON.parse('{{equipamentos}}');
            var equips_div = $('<div />').addClass('equips');
            var lab_div = $('<div />');
            var lab_radio = $('<input />')
                                        .attr('type', 'radio')
                                        .attr('name', 'equipamento')
                                        .attr('value', 'laboratorio')
            var lab_span = $('<span />').text("Laboratório");
            $(lab_div).append(lab_radio);
            $(lab_div).append(lab_span);
            $(equips_div).append(lab_div);
            $.each(equips, function(idx,row){
                var equip_div = $('<div />');
                var equip_radio = $('<input />')
                                            .attr('type', 'radio')
                                            .attr('name', 'equipamento')
                                            .attr('value', row)
                var equip_span = $('<span />').text('Equipamento ' + row);
                $(equip_div).append(equip_radio);
                $(equip_div).append(equip_span);
                $(equips_div).append(equip_div);
            });
            $('.graphic_mode').append(equips_div)
        }
        else{
            $('.equips').remove();
        }
    });

  var mydata = JSON.parse('{{temp_data}}' || "[]");

  function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'index');
    data.addColumn('number', 'mean');
    data.addColumn({id: 'min', type:'number', role: 'interval'});
    data.addColumn({id: 'max', type:'number', role: 'interval'});

    data.addRows(mydata);

    var options = {
        title:'Grafico',
        curveType:'function',
        lineWidth: 4,
        series: [{'color': '#D3362D'}],
        intervals: { 'lineWidth':2, 'barWidth': 0.5 },
        legend: 'none',
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve-chart'));

    chart.draw(data, options);
  }

  if (mydata.length > 0) {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
  } else {
      document.getElementById('curve-chart').remove();
      document.getElementById('warning-chart').style = "";
  }
*/
});


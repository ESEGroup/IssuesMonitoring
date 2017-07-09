$(function() {
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

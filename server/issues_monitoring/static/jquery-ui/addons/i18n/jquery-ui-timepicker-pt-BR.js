/* Brazilian Portuguese translation for the jQuery Timepicker Addon */
/* Written by Diogo Damiani (diogodamiani@gmail.com) */
(function ($) {
	$.timepicker.regional['pt-BR'] = {
		timeOnlyTitle: 'Escolha o horário',
		timeText: 'Horário',
		hourText: 'Hora',
		minuteText: 'Minutos',
		secondText: 'Segundos',
		millisecText: 'Milissegundos',
		microsecText: 'Microssegundos',
		timezoneText: 'Fuso horário',
		currentText: 'Agora',
		closeText: 'Fechar',
		timeFormat: 'HH:mm',
		timeSuffix: '',
		amNames: ['a.m.', 'AM', 'A'],
		pmNames: ['p.m.', 'PM', 'P'],
		isRTL: false
	};
	$.timepicker.setDefaults($.timepicker.regional['pt-BR']);
})(jQuery);


/* Brazilian initialisation for the jQuery UI date picker plugin. */
/* Written by Leonildo Costa Silva (leocsilva@gmail.com). */
( function( factory ) {
	if ( typeof define === "function" && define.amd ) {

		// AMD. Register as an anonymous module.
		define( [ "../widgets/datepicker" ], factory );
	} else {

		// Browser globals
		factory( jQuery.datepicker );
	}
}( function( datepicker ) {

datepicker.regional[ "pt-BR" ] = {
	closeText: "Fechar",
	prevText: "&#x3C;Anterior",
	nextText: "Próximo&#x3E;",
	currentText: "Hoje",
	monthNames: [ "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
	"Julho","Agosto","Setembro","Outubro","Novembro","Dezembro" ],
	monthNamesShort: [ "Jan","Fev","Mar","Abr","Mai","Jun",
	"Jul","Ago","Set","Out","Nov","Dez" ],
	dayNames: [
		"Domingo",
		"Segunda-feira",
		"Terça-feira",
		"Quarta-feira",
		"Quinta-feira",
		"Sexta-feira",
		"Sábado"
	],
	dayNamesShort: [ "Dom","Seg","Ter","Qua","Qui","Sex","Sáb" ],
	dayNamesMin: [ "Dom","Seg","Ter","Qua","Qui","Sex","Sáb" ],
	weekHeader: "Sm",
	dateFormat: "dd/mm/yy",
	firstDay: 0,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: "" };
    datepicker.setDefaults( datepicker.regional[ "pt-BR" ] );

    return datepicker.regional[ "pt-BR" ];

} ) );

/* global $, Dashboard */

var dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');

//dashboard.addWidget('knob_widget', 'Knob', {
//	getData: function () {
//		$.extend(this.scope, {
//			title: "Arc",
//			data: {
//				angleArc: 270,
//				fgColor: "lightgreen",
//				angleOffset: 225,
//				displayInput: false,
//				displayPrevious: false,
//				step: 1,
//				min: 0,
//				max: 100,
//				readOnly: true
//			},
//			value: 14,
//			moreInfo: "Mer info."
//		});
//	}
//});

dashboard.addWidget('weather_widget', 'Number', {
	getData: function () {
		var self = this;
		$.get('/weather/', function (data) {
			$.extend(self.scope, {
				title: data.title,
				moreInfo: data.moreInfo,
				updatedAt: data.updatedAt,
				detail: data.detail,
				value: data.value
			});
		});
	}
});

dashboard.addWidget('trello_widget', 'List', {
	getData: function () {
		var self = this;
		$.get('/trello/', function (data) {
			console.log(data);
			$.extend(self.scope, {
				title: data.title,
				moreInfo: data.moreInfo,
				updatedAt: data.updatedAt,
				data: data.data
			});
		});
	}
});

dashboard.addWidget('forecast_widget', 'Graph', {
	getData: function () {
		var self = this;
		$.get('/forecast/', function (data) {
			$.extend(self.scope, {
				title: data.title,
				moreInfo: data.moreInfo,
				data: data.data,
				value: data.value
			})
		});
	}
});
function hazardsSelectedChart(params){

    this.identifier = params.id;
    this.title = params.title;
    this.categories = params.categories;
    this.series = params.series;
    this.colors = params.colors;


    this.createChart = function (){
        var self = this;
        $(function () {

            Highcharts.chart(self.identifier, {

                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Hazards selected in this assessment'
                },
                credits: {
                    enabled: false
                },
                exporting: {
                    enabled: false
                },
                plotOptions: {
                    pie: {
                        shadow: false,
                        center: ['50%', '50%']
                    }
                },
                tooltip: {
                    valueSuffix: '%'
                },
                series: [{
                    name: 'Hazard Groups',
                    data: browserData,
                    size: '60%',
                    dataLabels: {
                        formatter: function () {
                            return this.y > 5 ? this.point.name : null;
                        },
                        color: '#ffffff',
                        distance: -30
                    }
                }, {
                    name: 'Hazard Types',
                    data: versionsData,
                    size: '80%',
                    innerSize: '60%',
                    dataLabels: {
                        formatter: function () {
                            // display only if larger than 1
                            return this.y > 1 ? '<b>' + this.point.name + '</b> ' : null;
                        }
                    }
                }]
            });
        });


    }
}

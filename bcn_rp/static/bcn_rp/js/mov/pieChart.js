function CompletionChart(params){

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
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },

                credits: {
                    enabled: false
                },

                exporting: {
                    enabled: false
                },

                colors: self.colors,

                title: {
                    text: self.title,
                    x: -80
                },

                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: false
                        },
                        showInLegend: true
                    }
                },

                xAxis: {
                    categories: self.categories,
                },

                yAxis: {
                    title: self.title,
                    min: 0,
                },

               tooltip: {
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y:.2f}</b> ({point.percentage:.2f}%)<br/>',
                    shared: true,
               },

               legend: {
                    align: 'right',
                    verticalAlign: 'top',
                    y: 70,
                    layout: 'vertical'
               },

                series: self.series


            });
        });

    }

}
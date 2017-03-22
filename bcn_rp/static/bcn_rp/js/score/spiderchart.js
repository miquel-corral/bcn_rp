function SpiderChart(params){

    this.identifier = params.id;
    this.title = params.title;
    this.categories = params.categories;
    this.series = params.series;
    this.colors = params.colors;

    if (typeof(this.colors) === 'undefined'){
        this.colors = ['#2f7ed8', '#0d233a', '#8bbc21', '#910000', '#1aadce',
            '#492970', '#f28f43', '#77a1e5', '#c42525', '#a6c96a'];
    }

    this.createChart = function (){
        var self = this;
        $(function () {

            Highcharts.chart(self.identifier, {

                chart: {
                    polar: true,
                    type: 'line'

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

                pane: {
                    size: '80%'
                },

                xAxis: {
                    categories: self.categories,
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },

                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0,
                    max: 10,
                },

                tooltip: {
                    shared: true,
                    pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.2f}</b><br/>'
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
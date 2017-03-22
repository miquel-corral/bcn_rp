function CompletionData(data){

    this.data = data;


    this.getCategories = function(){
         var self = this;
         var categories = [];

         self.data.forEach(function(assessment) {
             categories.push('Degree of Completion');
         });
         return categories;
    }

    this.getSerie = function(title){
        var self = this;
        var series = [];
        var serie = { name: 'Questions',
                      colorByPoint: true,
                      data: [],
                      pointPlacement: 'on'};

        self.data.forEach(function(assessment) {
            serie.data.push({name: 'Responded', y:parseFloat(assessment['completion'])});
            serie.data.push({name: 'Not responded', y:parseFloat(100-parseFloat(assessment['completion']))});
         });

        series.push(serie);

        return series;
    }

    this.getMoVSerie = function(){
        var self = this;
        return self.getSerie('MoV');
    }






}
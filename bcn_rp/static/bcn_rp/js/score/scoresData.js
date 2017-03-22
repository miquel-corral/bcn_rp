function ScoresData(data){

    this.data = data;


    this.getCategories = function(){
         var self = this;
         var categories = [];

         self.data.forEach(function(assessmentelement) {
             categories.push(assessmentelement.element.name);
         });
         return categories;
    }

    this.getSerie = function(title, field){
        var self = this;
        var series = [];
        var serie = { name: title,
                        data: [],
                        pointPlacement: 'on'};

         self.data.forEach(function(assessmentelement) {
             serie.data.push(parseFloat(assessmentelement[field]));
         });

        series.push(serie);
        return series;
    }

    this.getScoreSerie = function(){
        var self = this;
        return self.getSerie('Score','score');
    }






}
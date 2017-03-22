function MoVData(data){

    this.data = data;


    this.getCategories = function(){
         var self = this;
         var categories = [];

         self.data.forEach(function(assessment) {
             categories.push('MoV Type');
         });
         return categories;
    }

    this.getSerie = function(title){
        var self = this;
        var series = [];
        var serie = { name: title,
                        data: [],
                        pointPlacement: 'on'};

        self.data.forEach(function(assessment) {
            series.push({ name: 'Media', data:[parseFloat(assessment['mov_media'])], pointPlacement: 'on'});
            series.push({ name: 'Official Document', data:[parseFloat(assessment['mov_official_document'])], pointPlacement: 'on'});
            series.push({ name: 'Public Knowledge', data:[parseFloat(assessment['mov_public_knowledge'])], pointPlacement: 'on'});
         });

        return series;
    }

    this.getMoVSerie = function(){
        var self = this;
        return self.getSerie('MoV');
    }






}
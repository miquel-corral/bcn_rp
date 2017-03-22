function HazardInterdepsData(data){

    this.rawData = data;
    this.dependencyData;
    this.codes = []; // codes needed to manage relationships

    this.getDependencyData = function(){
        var self = this;

        dependencyData = {
            packageNames : self.getPackageNames(),
            matrix : self.getMatrix()
        }

        return dependencyData;
    }

    this.getPackageNames = function(){
        var self = this;

        var packageNames = [];

        self.rawData.forEach(function(assessmenthazardtype) {
             packageNames.push(assessmenthazardtype.hazard_type.name);
             self.codes.push(assessmenthazardtype.hazard_type.code);
        });

        return packageNames;
    }

    this.getMatrix = function(){
        var self = this;

        var matrix = self.initMatrix();

        self.setConsecuences2(matrix, self.rawData);
        self.setCauses2(matrix, self.rawData);

        return matrix;

    }

    this.initMatrix = function(){
        var self = this;
        var length = self.rawData.length;

        var matrix = [];
        for(var i=0; i<length; i++) {
            matrix[i] = [];
            for(var j=0; j<length; j++) {
                matrix[i][j] = 0;
            }
        }

        return matrix
    }


    this.setConsecuences2 = function(matrix, data){
        var self = this;
        var index = 0;
        data.forEach(function(assessmenthazardtype) {
             index = self.codes.indexOf(assessmenthazardtype.hazard_type.code)
             self.setAssesmentHazardTypeConsecuences2(matrix[index],assessmenthazardtype.ht_consequence);
        });
    }

    this.setAssesmentHazardTypeConsecuences2 = function(row, ht_consequences){
        var self = this;

        if( ht_consequences && ht_consequences.length > 0){
            ht_consequences.forEach(function(cons) {
               position = self.codes.indexOf(cons.a_h_type_code);
               row[position]=1;
            });
        }


    }






     this.setCauses2 = function(matrix, data){
        var self = this;
        var index = 0;
        data.forEach(function(assessmenthazardtype) {
            index = self.codes.indexOf(assessmenthazardtype.hazard_type.code)

             console.log("causes.hazard_type: " + assessmenthazardtype.hazard_type.code + ", index: " + index)

            self.setAssesmentHazardTypeCauses2(matrix, index, assessmenthazardtype.ht_cause);
             //self.setAssesmentHazardTypeCauses2(matrix, index++, assessmenthazardtype.ht_cause);

        });
    }

    this.setAssesmentHazardTypeCauses2 = function(matrix, i, ht_cause){
           var self = this;

            if (ht_cause && ht_cause.length > 0){
                ht_cause.forEach(function(cause){

                   position = self.codes.indexOf(cause.a_h_type_code);


                   console.log("cause: " + cause.a_h_type_code + ", position: " + position);

                   matrix[position][i]=1;





                })

            }


    }


    /*
    this.setCauses = function(matrix, data){
        var self = this;
        var index = 0;
        data.forEach(function(assessmenthazardtype) {
             self.setAssesmentHazardTypeCauses(matrix, index++, assessmenthazardtype.ht_cause);
        });
    }

    this.setAssesmentHazardTypeCauses = function(matrix, index, ht_cause){
           var self = this;

            ht_cause.forEach(function(cause) {

               console.log(cause);
               console.log(typeof(cause));

               if (typeof(cause) === 'undefined'){
                  matrix[parseInt(cause.id)-1][index] = 1;
               }

            });

    }
    */

}
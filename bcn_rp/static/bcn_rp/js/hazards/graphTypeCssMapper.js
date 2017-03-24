function TypeCssMapper(cssNames){

    this.cssNames = cssNames;

    this.mapType = function (type){
        var self = this;
        if ( self.cssNames[type] === "undefined" ){
           return  self.defaultMapping();
        }
        else{
           return self.cssNames[type];
        }

    };

    this.defaultMapping = function (){
        return  "link basic";
    }
}
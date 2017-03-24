function Legend(types, svg, typeCssMapper, legendRectSize, legendSpacing){

    this.typeCssMapper = typeCssMapper;
    this.types = types;
    this.svg = svg;
    this.legendRectSize = legendRectSize;
    this.legendSpacing = legendSpacing;

    this.cssScale;
    this.legend;



    this.createLegend = function (){
        var self = this;
        self.types = self.processTypeData(self.types);
        self.cssScale = self.createCssScale(self.types);
        self.legend = self.appendLegendObject(self.svg, self.cssScale);
        self.addLegendRectangle(self.legend,self.cssScale);
        self.addLegendText(self.legend);
    }


    this.getTypeNames = function (types){
        var self = this;
        return Object.keys(types).map(function(key) {
            return types[key].name;
        })
    };

    this.getTypeColors = function (types){
        var self = this;
        return Object.keys(types).map(function(key) {
            return types[key].color;
        })
    };

    this.getTypeCss = function (types){
        var self = this;
        return Object.keys(types).map(function(key) {
            return types[key].css;
        })
    };

    this.createCssScale = function (types){
        var self = this;
        var type_names = self.getTypeNames(types);
        var type_css = self.getTypeCss(types);
        var cssScale = d3.scale.ordinal()
            .domain(type_names)
            .range(type_css);
        return cssScale;
    };

    this.appendLegendObject = function(svg, cssScale){
         var self = this;
         var legend = svg
            .append("g")
            .selectAll("g")
            .data(cssScale.domain())
            .enter()
            .append('g')
              .attr('class', 'legend')
              .attr('transform', function(d, i) {
                var height = self.legendRectSize;
                var x = 0;
                var y = i * height;
                return 'translate(' + x + ',' + y + ')';
            });

            return legend;
     };

     this.addLegendRectangle = function( legend , cssScale){
         var self = this;
          legend.append('rect')
            .attr('width', self.legendRectSize)
            .attr('height', self.legendRectSize)
            .attr("class", cssScale);

     };

     this.addLegendText = function( legend ){
        var self = this;
          legend.append('text')
                .attr('x', self.legendRectSize + self.legendSpacing)
                .attr('y', self.legendRectSize - self.legendSpacing)
                .attr("class","legend")
                .text(function(d) { return d; });
    };


    this.processTypeData = function(types){
        var self = this;
        types.forEach(function(type) {
             type.css = self.typeCssMapper.mapType(type.id);
        });

        return types;
     }

};
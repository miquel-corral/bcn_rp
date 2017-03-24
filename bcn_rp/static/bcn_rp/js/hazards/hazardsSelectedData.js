function HazardSelectedData(ah_types_data, hg_data){

    // row data
    this.ah_types_data = ah_types_data;
    this.hg_data = hg_data;

    var colors = Highcharts.getOptions().colors;
    var categories = this.getCategories();

    this.getCategories = function(){
        var self = this;
        var categories = [];

        self.hg_data.forEach(function(hg){
            categories.push(hg.name);
        })

        return categories;
    }


    var data = this.getData();

    this.getData = function(){
        var self = this;

        var data = [];

        self.ah_types_data.forEach(function(ah_type){


        })

    }



        data = [{% for key, value in hazard_selected.items %}{
                y:{% for k, v in value.items %}{{v}}{%if not forloop.last%}+{% endif %}{% endfor %},
                color: colors[{{forloop.counter|add:'-1'}}],
                drilldown: {
                    name: '{{key}}',
                    categories: [{% for k, v in value.items %}'{{k}}'{% if not forloop.last %},{% endif %}{% endfor %}],
                    data:[{% for k, v in value.items %}{{v}}{% if not forloop.last %},{% endif %}{% endfor %}],
                    color: colors[{{forloop.counter|add:'-1'}}]
                }}{% if not forloop.last %},{% endif %}{% endfor %}],
        browserData = [],
        versionsData = [],
        i,
        j,
        dataLen = data.length,
        drillDataLen,
        brightness;


    // Build the data arrays
    for (i = 0; i < dataLen; i += 1) {

        // add browser data
        browserData.push({
            name: categories[i],
            y: data[i].y,
            color: data[i].color
        });

        // add version data
        drillDataLen = data[i].drilldown.data.length;
        for (j = 0; j < drillDataLen; j += 1) {
            brightness = 0.2 - (j / drillDataLen) / 5;
            versionsData.push({
                name: data[i].drilldown.categories[j],
                y: data[i].drilldown.data[j],
                color: Highcharts.Color(data[i].color).brighten(brightness).get()
            });
        }
    }





}



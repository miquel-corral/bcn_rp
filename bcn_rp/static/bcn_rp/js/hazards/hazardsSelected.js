var ah_type_Data;
var hg_Data;

function getData(id){

    // get assessment hazard types
    d3.json("/assessment_hazard_list/?id=" + id , function(error, data) {
        if (error) return console.error('Error loading graph data', error)
        ah_type_Data = data
    });

    // get selected hazard groups
    d3.json("/hazard_group_list/?a_id=" + id , function(error, data) {
        if (error) return console.error('Error loading graph data', error)
        hg_Data =  data
    });

    createGraph();
}


function createGraph(){

     var colorsScore = ['#f45b5b'];
     var colorPalette='Set2';
     var colorPick=6;
     var params = {
        id : 'score',
        title : 'Score',
        categories : scoreData.getCategories(),
        series : scoreData.getScoreSerie(),
        //colors : colorsScore
        colors: colorbrewer[colorPalette][colorPick].slice(),
     };

     return createChart(params);
}


function createChart(params){
     var chart = new SpiderChart(params);
     chart.createChart();
     return chart;
}


function getURLParameter(sParam){
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split('&');
  for (var i = 0; i < sURLVariables.length; i++)
  {
      var sParameterName = sURLVariables[i].split('=');
      if (sParameterName[0] == sParam)
      {
          return sParameterName[1];
      }
  }

}

function createGraph(hazardSelectedData){

    var chart = d3.chart.dependencyWheel()
      .width(900)
      .margin(250)
      .padding(.10);

    d3.select('#chart')
     .datum(hazardInterdepsData.getDependencyData())
     .call(chart);

}


var id = getURLParameter("id");


getData(id);
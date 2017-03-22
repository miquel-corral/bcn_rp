var movData;
var completionData;

function getData(){

    if (typeof(id) === 'undefined'){
        $.getJSON( "/assessment" , function( data ) {

            if (data.length > 0){
                movData = new MoVData(data);
                createMoVChart();
                completionData = new CompletionData(data);
                createCompletionChart();
            }else{
                console.log("No assessment data.");
            }
        })
    }
}


function createMoVChart(){
    var colorPalette='Set2';
    var colorPick=6;
    var params = {
        id : 'mov',
        title : 'Degree of Certainty',
        categories : movData.getCategories(),
        series : movData.getMoVSerie(),
        colors: colorbrewer[colorPalette][colorPick].slice(),
    };
    return createMoVChartData(params);
}


function createMoVChartData(params){
     var chart = new MoVChart(params);
     chart.createChart();
     return chart;
}


// TODO: separate js for completion
function createCompletionChart(){
    var colorPalette='Set2';
    var colorPick=6;
    var params = {
        id : 'completion',
        title : 'Degree of Completion',
        categories : completionData.getCategories(),
        series : completionData.getSerie(),
        colors: colorbrewer[colorPalette][colorPick].slice(),
    };
    return createCompletionChartData(params);
}


function createCompletionChartData(params){
     var chart = new CompletionChart(params);
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

var id = getURLParameter("id");


getData();






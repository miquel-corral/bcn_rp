
var scoreData;

function getData(id){

    console.log('getData!');

    if (typeof(id) === 'undefined'){
        getParentCharts();
    }else{
        getChildCharts(id);
    }
 }


function getChildCharts(id){

     $.getJSON( "/child_assessmentelement_list?id=" + id , function( data ) {

            if (data.length > 0){
                scoreData = new ScoresData(data);
                createCharts();
            }
            else{
                getLeafChart(id);
            }


    })

}

function getLeafChart(id){

    $.getJSON( "/assessmentelement_list?id=" + id , function( data ) {
           if (data.length = 1 ){
               createLeafChart(data[0]);
           }
    })

}



function getParentCharts(){
    $.getJSON( "/parent_assessmentelement_list", function( data ) {
            scoreData = new ScoresData(data);
            createCharts();
    })
}

 function createCharts(){

    createScoreChart();
    //createOrganizationalChart();
    //createFunctionalChart();
    //createPhysicalChart();

}


function createScoreChart(){

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



function createLeafChart(ae){

     var colorLeafSeries = ['#91e8e1'];

     var params = {
         id : 'leaf',
         title : 'Score ' + ae.score,
         categories : ['Organizational','Functional','Physical'],
         series : [{ name: ae.element.name + 'Scores',
                      data: [parseInt(ae.organizational_score), parseInt(ae.functional_score), parseInt(ae.physical_score)],
                      pointPlacement: 'on'}],
         colors : colorLeafSeries
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

var id = getURLParameter("id");


getData(id);

console.log('Hello!');




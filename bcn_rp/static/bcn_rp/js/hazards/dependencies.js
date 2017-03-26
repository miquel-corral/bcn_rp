var graph;
var legend;

// Define map css style names for link types
var cssNames = {"1":"link blue","2":"link dash","3":"link opacity"};

// Create mapper, implements mapping between types and css styles
var typeCssMapper = new TypeCssMapper(cssNames);


var id = getURLParameter("assessmentElementId");

getGraphData(id);


function getWidth(){
    return document.getElementById("depen").offsetWidth;
}

function getHeight(){
    return Math.ceil(getWidth()*0.6);
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

function getGraphData(id){

    if(typeof(id)==='undefined'){
        url="/hazard_impacts_list/";
    }else{
        url="/hazard_impacts_list?assessmentElementId=" + id + "&level=1";
    }

    d3.json(url, function(error, graphData) {
        if (error) return console.error('Error loading graph data', error)
        // Build graph
        graph = new Graph(graphData, id, typeCssMapper, "small", getHeight(), getWidth());
        graph.createGraph();
        getTypeData();
    });
 }

 function getTypeData(){

     if(typeof(id)==='undefined'){
        url="/hazard_impact_type_list/1?level=1";
    }else{
        url="/hazard_impact_type_list/1?assessmentElementId=" + id + "&level=1";
    }


    d3.json("/hazard_impact_type_list", function(error, dataTypes) {
        if (error) return console.error('Error loading type data', error)
         // Build legend
         legend = new Legend(dataTypes, graph.svg, typeCssMapper, 20, 10);
         legend.createLegend();

    });
 }






function getData(id){

    d3.json("/hazard_dependencies_list/?id=" + id , function(error, data) {
        if (error) return console.error('Error loading graph data', error)
        var hazardInterdepsData = new HazardInterdepsData(data);
        createGraph(hazardInterdepsData);
    });

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

function createGraph(hazardInterdepsData){

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
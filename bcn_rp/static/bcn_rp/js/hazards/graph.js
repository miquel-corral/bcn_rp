/*
    graphData : Data from links
    sourceId = id used as source
    typeCssMapper = class that implements the mapping between type and css
    nodeSize = [small,medium,big]
    height  = container height
    width  = width height
*/

function Graph(graphData, sourceId, typeCssMapper, nodeSize, height, width){

  this.graphData = graphData;
  this.sourceId = sourceId;
  this.typeCssMapper = typeCssMapper;
  this.nodeSize = nodeSize;
  this.height = height;
  this.width = width;


  this.links;
  this.nodes;
  this.svg;
  this.path;
  this.node;

  this.nodeSizesData = {"small":{nodeRadius: 10, refX : 17.75, refY: -1.1},
                 "medium":{nodeRadius: 30, refX : 32.75, refY: -1.55},
                 "big": {nodeRadius: 60, refX : 54.5, refY: -4.65}};


  this.createGraph = function(){
        var self = this;

        self.links = self.computeLinks(self.graphData);
        self.nodes = self.computeNodes(self.links);
        self.createLinkedGraph(self.links, self.nodes);
   }

  this.computeLinks = function(links){

        links.forEach(function(link) {
             link.source = link.source;
             link.source_name = link.source_name;
             link.target = link.target;
             link.target_name = link.target_name;
             link.value = 1;
             link.isSource = false;
             if (link.source == self.sourceId){
                link.isSource = true;
             }

        });

        return links;
    }

   this.computeNodes = function(links){

        var nodes = {};

        // Compute the distinct nodes from the links.
        links.forEach(function(link) {
            link.source = nodes[link.source] ||
                (nodes[link.source] = {name: link.source_name, isSource: link.isSource});
            link.target = nodes[link.target] ||
                (nodes[link.target] = {name: link.target_name});
            link.value = +link.value;

        });
        return nodes;
    }


    this.createLinkedGraph = function(links, nodes){
            var self = this;

            force = self.createLayout(links,nodes);

            self.svg = self.createSvg();

            self.defineArrow(self.svg);

            self.path = self.createPaths(self.svg);

            self.node = self.createNodes(self.svg,force);

    }


    this.createLayout = function(links, nodes){
        var self = this;
        var force = d3.layout.force()
            .nodes(d3.values(nodes))
            .links(links)
            .size([self.width, self.height])
            .linkDistance(self.width/3)
            .charge(-300)
            .on("tick", function(d){self.tick(d,self);})
            .start();

        force.drag()
                .on("dragstart", self.dragstart);

        return force;
    }

    this.createSvg = function(){
        var self = this;
        var svg = d3.select("#depen").append("svg")
            .attr("width", self.width)
            .attr("height", self.height);
        return svg;
    }


    this.defineArrow = function(svg){
        var self = this;
        svg.append("svg:defs").selectAll("marker")
            .data(["end"])      // Different link/path types can be defined here
          .enter().append("svg:marker")    // This section adds in the arrows
            .attr("id", String)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", self.nodeSizesData[nodeSize].refX)
            .attr("refY", self.nodeSizesData[nodeSize].refY)
            .attr("markerWidth", 9)
            .attr("markerHeight", 9)
            .attr("orient", "auto")
          .append("svg:path")
            .attr("d", "M0,-5L10,0L0,5")


    }

    this.createPaths = function(svg){
        var self = this;
     var path = svg.append("svg:g").selectAll("path")
        .data(self.links)
      .enter().append("svg:path")
      .attr("class", function (d){ return self.typeCssMapper.mapType(d.impact_type);})
       .attr("marker-end", "url(#end)");


    return path;
}


    this.createNodes = function(svg, force){
        var self = this;
        var path = svg.selectAll(".node")
            .data(force.nodes())
          .enter().append("g")
            .attr("class", "node")
            .on("dblclick", self.dblclick)
            .call(force.drag);

            self.addCircleNode(path);

            self.addTextNode(path);

        return path;

    }

    this.addCircleNode = function(nodes){
        var self = this;
        nodes.append("circle")
            .attr("r", self.nodeSizesData[nodeSize].nodeRadius)
            .attr("class", function(node){
                if (node.isSource){
                    return "origin";
                }else{
                   return "";
                }})
    }

    this.addTextNode = function(node){
        var self = this;
        node.append("text")
            .attr("x", 12)
            .attr("dy", ".35em")
            .text(function(d) { return d.name; });
    }


    this.dblclick = function(d) {
      d3.select(this).classed("fixed", d.fixed = false);
    }

    this.dragstart = function(d) {
      d3.select(this).classed("fixed", d.fixed = true);
    }


   this.tick = function( tick, self ) {

        self.path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        });

        self.node
            .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")"; });
    }


}




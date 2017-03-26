function StakeholdersData(graphData, typeData){

    this.graphData = graphData;
    this.typeData = typeData;

    this.nodes;
    this.links;
    this.dependencyTypes;




    this.processTypeData = function(){
        var self = this;

        self.dependencyTypes = {};

        self.typeData.forEach(function(type){
            self.dependencyTypes[type.id] = type.name;
        });

    }

    this.processGraphData = function(){
        var self = this;
        self.nodes = self.computeNodes(self.graphData);
        self.links = self.computeLinks(self.graphData);
    }

    this.computeNodes = function(graphData){

        var nodes = {};
            // Compute the distinct nodes from the links.
            graphData.forEach(function(link) {

                if ( typeof nodes[link.ae_origin.element.id] === "undefined"){
                    nodes[link.ae_origin.element.id] ||
                        (nodes[link.ae_origin.element.id] = { type: link.ae_origin.element.name, id: link.ae_origin.element.id,parent: null, name: link.ae_origin.element.name});
                        addStakeholdersNodes(link.ae_origin, link.ae_origin.stakeholders, nodes, graphData);
                }

                if ( typeof nodes[link.ae_dependent.element.id]  === "undefined"){
                    nodes[link.ae_dependent.element.id] ||
                      (nodes[link.ae_dependent.element.id] = { type: link.ae_dependent.element.name, id: link.ae_dependent.element.id,parent: null, name: link.ae_dependent.element.name});

                    addStakeholdersNodes(link.ae_dependent, link.ae_dependent.stakeholders, nodes, graphData);
                }

            });

        var keys = Object.keys(nodes);

        var values = keys.map(function(v) { return nodes[v]; })

        return values;

    }

    this.computeLinks = function(graphData){

        graphData.forEach(function(link) {
                if (typeof link.isStakeholderLink === "undefined" || link.isStakeholderLink == false){
                     link.source = link.ae_origin.element.id;
                     link.target = link.ae_dependent.element.id;
                     link.value = link.dependency_type;
                }
            });
        return graphData;

    }

    function getChildren(graphData, sourceId){

         var children = [];

         graphData.forEach(function(link) {
                if  (typeof link.ae_origin != "undefined" && sourceId == link.ae_origin.element.id){
                    var child =  {id : link.ae_dependent.element.id, type:link.dependency_type};
                    children.push(child);
                }

            });

        return children;

    }


    function addStakeholdersNodes(assestmentelement, stakeholders, nodes, graphData){


            stakeholders.forEach(function(stakeholder) {
                var stakeholderId = assestmentelement.element.name + stakeholder.name;

                if (typeof nodes[stakeholderId]  === "undefined"){

                    var children = getChildren(graphData, assestmentelement.element.id);

                    if (children.length > 0){

                        nodes[stakeholderId] = { type: assestmentelement.element.name, id: stakeholderId, parent: assestmentelement.element.id, name: stakeholder.name, ae_id : assestmentelement.id};


                        children.forEach(function(child){
                             graphData.push({source: stakeholderId,  target: child.id, value: child.type, isStakeholderLink: true});
                         });
                    }
                }
            });






    }


    this.processTypeData();
    this.processGraphData();



}
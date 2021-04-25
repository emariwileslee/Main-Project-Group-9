
var people_ids = {}
var id_index = 0

$(document).ready(renderGraph());


function findSubNetwork(selected, edgeArray){
    var selectedsNetwork = []
    for (var i = 0; i < edgeArray.length; i++){
        if (edgeArray[i].from == selected){
            selectedsNetwork.push(edgeArray[i].to)
        } else if (edgeArray[i].to == selected){
            if(!selectedsNetwork.includes(edgeArray[i].from)){
                selectedsNetwork.push(edgeArray[i].from)
            }
        }
    }
    return selectedsNetwork;
}

function addToPeopleIdDict(name, nodeArray){
    if (people_ids[name] == undefined){
        people_ids[name] = id_index
        nodeArray.push({id: id_index, label: name, group: id_index % 5})
        id_index += 1 

    } 
    return people_ids[name]
}
function renderGraph(){
    //var ready  = await checkIfLoaded()
    readFile(data)
}

function checkIfLoaded(){
   
    return new Promise(resolve => {
     while(true){
        if (data != -1) {
            resolve(true);
        }
    }
  });
}

function readFile(relationships) {


    var nodeArray = []
    var edgeArray = []

    var PersonsFollowers = []
    //12 used to be 9 for follow-demo.csv.. HAVE TO CHANGE AGAIN IF HEADERS CHANGE ( eventually make it so it just parses until the ":")
    for (var i = 0; i < relationships.length; i++){
        followedName = relationships[i][0]
        followerName = relationships[i][1]

        
        followed = addToPeopleIdDict(followedName, nodeArray)
        follower = addToPeopleIdDict(followerName, nodeArray)

        

        edgeArray.push({from: followed, to: follower})

        if(PersonsFollowers[followed] != undefined){

            PersonsFollowers[followed].push(followerName)
        } else {
            PersonsFollowers[followed] = []
            PersonsFollowers[followed].push(followerName)
        }
    }
    
    var origNodes = new vis.DataSet(nodeArray)
    var nodes  = new vis.DataSet(nodeArray)
    
    // create an array with edges
    var origEdges = new vis.DataSet(edgeArray);
    var edges = new vis.DataSet(edgeArray);
    
    // create a network
    var container = document.getElementById('mynetwork');
    console.log("Container: ")
    console.log(container)
    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        physics: {
            enabled: false,
            solver: "repulsion",
            repulsion: {
                nodeDistance: 400 // Put more distance between the nodes.
            },
        },
        edges: {
            arrows: {
                to:{
                    enabled: true,
                    scaleFactor: .25
                }
            },
            length: 400
        }
    };



    // initialize your network!
    var network = new vis.Network(container, data, options);
    network.stabilize();

    network.on('click',function(properties) {
        var nodeId = properties.nodes[0];

        if(PersonsFollowers[nodeId] != undefined){
            
            for(var i =0 ; i < PersonsFollowers[nodeId].length ; i++){
                //console.log(PersonsFollowers[nodeId][i])
            }
        }
        
    })
    var lastDoubleClicked = -1;
    network.on('doubleClick', function(properties){ 

  //Double click to get subnetwork. 
        var nodeId = properties.nodes[0];
        
        if(PersonsFollowers[nodeId] != undefined){
            if(lastDoubleClicked != nodeId){
                var selectedsNetwork = findSubNetwork(nodeId, edgeArray)
                for(var i = 0; i < nodeArray.length; i++){
                    if (!selectedsNetwork.includes(i) && i != nodeId){
                        try {
                          nodes.remove({ id: i });
                        } catch (err) {
                          alert(err);
                        }
                    }
                }
                lastDoubleClicked = nodeId
            } else{
                
                
                data = {
                    nodes: origNodes,
                    edges: origEdges
                };
                network = new vis.Network(container, data, options);
                network.redraw()
            }
        }

    });
    



//Context Menu right click logic  

  // Trigger action when the contexmenu is about to be shown
    $(document).bind("contextmenu", function (event) {
        
        // Avoid the real one
        event.preventDefault();
        
        // Show contextmenu
        $(".custom-menu").finish().toggle(100).
        
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
    });


    // If the document is clicked somewhere
    $(document).bind("mousedown", function (e) {
        
        // If the clicked element is not the menu
        if (!$(e.target).parents(".custom-menu").length > 0) {
            
            // Hide it
            $(".custom-menu").hide(100);
        }
    });


    // If the menu element is clicked
    $(".custom-menu li").click(function(){
        
        // This is the triggered action name
        switch($(this).attr("data-action")) {
            
            // A case for each action. Your actions here
            case "first": alert("first"); break;
            case "second": alert("second"); break;
            case "third": alert("third"); break;
        }
      
        // Hide it AFTER the action was triggered
        $(".custom-menu").hide(100);
      });


  reader.onerror = function() {
    console.log(reader.error);
  };

}



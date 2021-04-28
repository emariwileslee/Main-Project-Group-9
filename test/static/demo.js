
var people_ids = {}
var id_index = 0
var lastRightClicked = -1;

var nodeArray = []
var edgeArray = []
var PersonsFollowers = []

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

function addToPeopleIdDict(nodeArray, newNode){
    if (people_ids[newNode.nodeName] == undefined){
        people_ids[newNode.nodeName] = id_index
        //size is controlled by value
        nodeArray.push({id: id_index, label: newNode.nodeName, group: id_index % 5, value: id_index + 3, data : newNode})
        id_index += 1 

    } 
    return people_ids[newNode.nodeName]
}
function renderGraph(){
    //var ready  = await checkIfLoaded()
    readFile(data)
}

function readFile(data) {
    
    var nodeArray = []
    var edgeArray = []
    var PersonsFollowers = []

    //12 used to be 9 for follow-demo.csv.. HAVE TO CHANGE AGAIN IF HEADERS CHANGE ( eventually make it so it just parses until the ":")
    for (var i = 0; i < data.length; i++){
        var newNode = {
            parentNodeName : data[i].parent_node,
            nodeName : data[i].username,
            connectionType : data[i].connection_type,
            bio : data[i].bio,
            totalLikes : data[i].total_likes,
            totalFollowers : data[i].total_followers,
            totalFollowing : data[i].total_following,
            profileImgUrl : data[i].profile_img_url,
            rootPostUrl : data[i].root_post_url
        }
        


        follower = addToPeopleIdDict(nodeArray, newNode)
        followed  = people_ids[newNode.parentNodeName]
        
        if (newNode.connectionType != 'ROOT'){
            edgeArray.push({from: followed, to: follower})
        }
        
        if(PersonsFollowers[followed] != undefined){

            PersonsFollowers[followed].push(newNode.nodeName)
        } else {
            PersonsFollowers[followed] = []
            PersonsFollowers[followed].push(newNode.nodeName)
        }
    }

    var origNodes = new vis.DataSet(nodeArray)
    var nodes  = new vis.DataSet(nodeArray)
    
    // create an array with edges
    var origEdges = new vis.DataSet(edgeArray);
    var edges = new vis.DataSet(edgeArray);
    
    // create a network
    var container = document.getElementById('mynetwork');
    
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
        nodes : {
            shape : 'hexagon',
            heightConstraint : {
                minimum : 50,
            },
            scaling : {
                label : false,
                min : 1, 
                max: 18

               
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
    network.on("oncontext", function (properties) 
    {
        lastRightClicked = network.getNodeAt(properties.pointer.DOM);
        
        console.log(lastRightClicked)
        properties.event.preventDefault();
        if(lastRightClicked != undefined)
        {
            
            $(".custom-menu").prepend(makeProfileSummary(lastRightClicked))
            $(".custom-menu").finish().toggle(100);
            $(".custom-menu").css({
                top: properties.event.pageY + "px",
                left: properties.event.pageX + "px"
            });
        }
            
    });


    // If the document is clicked somewhere
    $(document).bind("mousedown", function (e) {
        
        // If the clicked element is not the menu
        if (!$(e.target).parents(".custom-menu").length > 0) {
            
            // Hide it
            $(".custom-menu").hide();
            $("#profsum").remove();
        }
    });


    // If the menu element is clicked
    $(".custom-menu li").click(function(){
        
        // This is the triggered action name
        switch($(this).attr("data-action")) {
            
            // A case for each action. Your actions here
            case "first": alert("first"); break;
            case "seeNetwork": alert("second"); break;
            case "showProfiles": showProfiles(); break;
        }
      
        // Hide it AFTER the action was triggered
        $(".custom-menu").hide(100);
      });
      function makeProfileSummary(nodeId){
            var profSummary = "<li id='profsum'>"
            profSummary += "<p> Total Followers: " + nodeArray[nodeId].data.totalFollowers + "</p>"
            profSummary += "<p> Total Following: " + nodeArray[nodeId].data.totalFollowing + "</p>"


            profSummary += "</li>"
            return profSummary;
      }
      function showProfiles(){
        
        var name = nodeArray[lastRightClicked].label
        openInNewTab('https://www.instagram.com/'+ name);
      }
      function openInNewTab(href) {
            Object.assign(document.createElement('a'), {
            target: '_blank',
            href: href,
        }).click();
       }
}

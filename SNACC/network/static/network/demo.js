
var people_ids = {}
var id_index = 0
var lastRightClicked = -1;

var nodeArray = []
var edgeArray = []
var PersonsFollowers = []

$(document).ready(renderGraph(accounts, connections));

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

function renderGraph(accounts, connections ) 
{
    
    
    var nodeArray = []
    var edgeArray = []
    var PersonsFollowers = []
    //load accounts/nodes 
    for (var i = 0; i < accounts.length; i++){
        var newNode = {
            id : accounts[i].id,
            username : accounts[i].username,
            connectionType : accounts[i].connection_type,
            bio : accounts[i].bio,
            average_likes : accounts[i].average_likes,
            totalFollowers : accounts[i].total_followers,
            totalFollowing : accounts[i].total_following
        }
        nodeArray.push({id: newNode.id, label: newNode.username, group: id_index % 5, value: newNode.totalFollowers, data : newNode})
    }
    //load connections/edges 

    for (var i = 0; i < connections.length; i++){
        follower = connections[i].fro;
        followed  = connections[i].to;
        
        
        edgeArray.push({from: followed, to: follower})
        
        if(PersonsFollowers[followed] != undefined){

            PersonsFollowers[followed].push(follower)
        } else {
            PersonsFollowers[followed] = []
            PersonsFollowers[followed].push(follower);
        }
    }
        



    console.log(edgeArray)





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
            
            scaling : {
               
                min : 20, 
                max: 100,
                customScalingFunction: function (min,max,total,value) {
                    if (max === min) {
                        return 0.5;
                    }
                    else {
                        let scale = 1 / (max - min);
                        
                        return Math.max(0,((value)*scale));
                    }
                }

               
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
    network.on('doubleClick', function(properties)
    { 

    //Double click behavior. 
        var nodeId = properties.nodes[0];
        if(PersonsFollowers[nodeId] != undefined){
            //do whatever you want here. and not like when your girl tells you "do whatever you want" but you know damn well she's gonna get upset if you do the thing in question. You really can do whatever you want here I promise I won't get mad
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
            case "showPost": showPost(); break;
            case "showProfiles": showProfiles(); break;
        }
      
        // Hide it AFTER the action was triggered
        $(".custom-menu").hide(100);
      });
     
      function makeProfileSummary(nodeId){
            var node = nodeArray[nodeId].data
            var profSummary = "<li id='profsum'>"
            profSummary += "<h1>" + node.username + "</h1>"
            profSummary += "<p>Biography: " + node.bio + "</p>"
            profSummary += "<p id = 'average_likes'>Average Likes: " + node.average_likes  + "</p>"
            profSummary += "<h3>Followers</h3>"
            profSummary += "<p> Total Followers: " + node.totalFollowers + "</p>"
            profSummary += "<p> Related to Trend: 53% </p>"
            profSummary += "<h3>Following</h3>"
            profSummary += "<p> Total Following: " + node.totalFollowing + "</p>"
            profSummary += "<p> Related To Trend: 24% </p>"

            profSummary += "</li>"
            return profSummary;
      }
      function showPost(){
            openInNewTab(nodeArray[lastRightClicked].data.rootPostUrl);
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

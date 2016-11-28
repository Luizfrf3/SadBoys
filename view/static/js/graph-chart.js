var nodes = new vis.DataSet();
var edges = new vis.DataSet();
var dataSet;
var mode = "friends"

var container = document.getElementById('sadboysgraph');
var nodeContent = document.getElementById('nodeContent');

/* get the data */
var data = {
  nodes: nodes,
  edges: edges
};

/* Define the visualization options of the graph */
var options = {
  autoResize: true,
  nodes: {
    shape: 'dot',
    scaling: {
      min: 5,
      max: 20,
      label: {
        min: 8,
        max: 15,
        drawThreshold: 10,
        maxVisible: 15
      }
    },
    size: 10,
    font: {
      size: 10,
      color: '#000000'
    },
    borderWidth: 0.6
  },
  edges: {
    width: 0.15,
    smooth: {
      type: 'cubicBezier',
      roundness: 0.5,
      enabled: true
    }
  },
  interaction: {
    multiselect: false,
    navigationButtons: true,
    selectable: true,
    selectConnectedEdges: true,
    tooltipDelay: 100,
    zoomView: true,
    hideEdgesOnDrag: true
  },
  physics: {
    stabilization: {
        enabled: true,
        iterations: 80,
        updateInterval: 10,
        onlyDynamicEdges: true,
        fit: true
    },
    barnesHut: {
      gravitationalConstant: -100,
      springConstant: 0.001,
      springLength: 150
    }
  }
};

/* Create the graph (the graph element now is network) */
network = new vis.Network(container, data, options);

network.on('selectNode', function (params) {
  console.log()
  if (params.nodes.length > 0) {
    // get the data from selected node
    data = nodes.get(params.nodes[0]);
  }

  attributes = data['attributes']
  console.log(attributes)
  create_element(attributes)
  user_img(attributes['img_url'])
})

network.on('deselectNode', function (params) {
  nodeContent.innerHTML = 'Nenhum nó selecionado';
})

network.on('doubleClick', function (params) {
  if(nodes.get(params.nodes[0])['size'] == 16){
    if(mode == "friends"){
      mode = "tweets"
      loadJSON("/graph/data/tweets/"+params['nodes'], getNodesAndEdges, function(err) {
        console.log('Error on loading json: ' + err);
      });
    }else{
      mode = "friends"
      loadJSON("/graph/data/follows/"+params['nodes'], getNodesAndEdges, function(err) {
        console.log('Error on loading json: ' + err);
      });
    }
  }else{
    loadJSON("/graph/data/follows/"+params['nodes'], getNodesAndEdges, function(err) {
      console.log('Error on loading json: ' + err);
    });
  }

  /*
  attributes = data['attributes']
  console.log(attributes)

  */
})


/* This function gets the json from the adress and call the function with it */
loadJSON("/graph/data/initial", getNodesAndEdges, function(err) {
  console.log('Error on loading json: ' + err);
});

/* This function fills the Dataset. */
function getNodesAndEdges(JSONfile) {
  if (JSONfile.nodes === undefined) {
    JSONfile = {};
  }else {
    dataSet = JSONfile;
  }

  nodes.clear();
  edges.clear();

  /* Get the json and parse it in the visjs format */
  var parsed = vis.network.gephiParser.parseGephi(JSONfile);

  // Add the parsed data to the DataSets.
  nodes.add(parsed.nodes);
  edges.add(parsed.edges);

  // Fits the data in the div - zoom to fit
  network.fit();
}


function loadJSON(path, success, error) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        success(JSON.parse(xhr.responseText));
      }
      else {
        error(xhr);
      }
    }
  };
  xhr.open('GET', path, true);
  xhr.send();
}

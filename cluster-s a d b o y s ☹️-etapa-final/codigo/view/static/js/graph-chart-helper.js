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
      size: 32,
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
      springConstant: 0.002,
      springLength: 150
    }
  }
};

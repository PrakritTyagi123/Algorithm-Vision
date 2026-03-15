/* ═══════════════════════════════════════════════════
   AlgoVision — graphUI.js
   UI Controller for Graph & Pathfinding Algorithms
   ═══════════════════════════════════════════════════ */

const GraphUI = (() => {
  let graphViz = null;
  let gridRenderer = null;
  let currentGraph = null;
  let currentGrid = null;
  let steps = [];
  let currentStep = 0;
  let mode = 'graph'; // 'graph' or 'grid'
  let _dpInitialized = false;

  function init(graphVisualizer, gridRend) {
    graphViz = graphVisualizer;
    gridRenderer = gridRend;
  }

  /**
   * Generate and display a new random graph
   */
  function randomizeGraph(nodeCount = 8, density = 0.4, directed = false) {
    mode = 'graph';
    currentGraph = Helpers.randomGraph(nodeCount, density, directed);
    graphViz.setGraph(currentGraph.nodes, currentGraph.edges, directed);
    gridRenderer.hide();
    resetPlayback();
    return currentGraph;
  }

  /**
   * Generate and display a new random grid
   */
  function randomizeGrid(rows = 20, cols = 30, wallRatio = 0.25) {
    mode = 'grid';
    const data = Helpers.randomGrid(rows, cols, wallRatio);
    currentGrid = data;
    gridRenderer.initGrid(data.grid, data.start, data.end);
    gridRenderer.onCellClick = (r, c) => {
      gridRenderer.toggleWall(r, c);
    };
    resetPlayback();
    return currentGrid;
  }

  /**
   * Set custom graph
   */
  function setGraph(nodes, edges, directed = false) {
    mode = 'graph';
    currentGraph = { nodes, edges };
    graphViz.setGraph(nodes, edges, directed);
    gridRenderer.hide();
    resetPlayback();
  }

  /**
   * Fetch steps from backend
   */
  async function loadSteps(category, algorithm) {
    try {
      let data;
      if (mode === 'grid' || category === 'pathfinding') {
        data = await API.getPathfindingSteps(algorithm, currentGrid.grid, currentGrid.start, currentGrid.end);
      } else if (category === 'geometry') {
        const points = currentGraph ? currentGraph.nodes.map(n => [n.x, n.y]) : null;
        data = await API.getGeometrySteps(algorithm, points, null);
      } else {
        const endNode = currentGraph ? currentGraph.nodes.length - 1 : 0;
        data = await API.getGraphSteps(algorithm, currentGraph.nodes, currentGraph.edges, 0, endNode);
      }
      steps = data.steps || data;
      currentStep = 0;
      return steps;
    } catch (err) {
      console.error('Failed to load graph steps:', err);
      // Fallback: generate BFS/DFS client-side
      steps = _generateClientSteps(algorithm);
      currentStep = 0;
      return steps;
    }
  }

  /**
   * Advance to next step
   */
  function nextStep() {
    if (currentStep >= steps.length) return false;

    const step = steps[currentStep];

    if (step.table) {
      // Floyd-Warshall, Johnson table data → use dpViz
      if (currentStep === 0 || !_dpInitialized) {
        const s = step;
        if (typeof dpViz !== 'undefined' && dpViz.initTable) {
          dpViz.initTable(s.table.length, s.table[0]?.length || 1,
            s.row_headers || null, s.col_headers || null);
          _dpInitialized = true;
        }
      }
      if (typeof dpViz !== 'undefined') dpViz.applyStep(step);
    } else if (mode === 'grid') {
      _applyGridStep(step);
    } else {
      graphViz.applyStep(step);
    }

    currentStep++;
    return currentStep < steps.length;
  }

  function goToStep(index) {
    // For graph visualization, replay from start to index
    if (mode === 'graph') {
      graphViz.reset();
    } else {
      gridRenderer.resetStates();
    }

    currentStep = 0;
    const target = Helpers.clamp(index, 0, steps.length);
    while (currentStep < target) {
      const step = steps[currentStep];
      if (mode === 'grid') {
        _applyGridStep(step);
      } else {
        graphViz.applyStep(step);
      }
      currentStep++;
    }
  }

  function _applyGridStep(step) {
    if (step.visited) {
      step.visited.forEach(([r, c]) => {
        if (!(r === currentGrid.start[0] && c === currentGrid.start[1]) &&
            !(r === currentGrid.end[0] && c === currentGrid.end[1])) {
          gridRenderer.setCellState(r, c, 'visited');
        }
      });
    }

    if (step.frontier) {
      step.frontier.forEach(([r, c]) => {
        if (!(r === currentGrid.start[0] && c === currentGrid.start[1]) &&
            !(r === currentGrid.end[0] && c === currentGrid.end[1])) {
          gridRenderer.setCellState(r, c, 'frontier');
        }
      });
    }

    if (step.current) {
      const [r, c] = step.current;
      if (!(r === currentGrid.start[0] && c === currentGrid.start[1]) &&
          !(r === currentGrid.end[0] && c === currentGrid.end[1])) {
        gridRenderer.setCellState(r, c, 'current');
      }
    }

    if (step.path) {
      step.path.forEach(([r, c]) => {
        if (!(r === currentGrid.start[0] && c === currentGrid.start[1]) &&
            !(r === currentGrid.end[0] && c === currentGrid.end[1])) {
          gridRenderer.setCellState(r, c, 'path');
        }
      });
    }
  }

  function resetPlayback() {
    steps = [];
    currentStep = 0;
    _dpInitialized = false;
    if (mode === 'graph') {
      graphViz.reset();
    } else {
      gridRenderer.resetStates();
    }
  }

  function getProgress() {
    return {
      current: currentStep,
      total: steps.length,
      percent: steps.length ? (currentStep / steps.length) * 100 : 0,
    };
  }

  /**
   * Client-side BFS/DFS fallback
   */
  function _generateClientSteps(algorithm) {
    if (!currentGraph) return [];

    const adj = {};
    currentGraph.nodes.forEach(n => (adj[n.id] = []));
    currentGraph.edges.forEach(e => {
      adj[e.from].push(e.to);
    });

    if (algorithm === 'bfs') return _bfsSteps(adj, 0);
    if (algorithm === 'dfs') return _dfsSteps(adj, 0);
    return _bfsSteps(adj, 0);
  }

  function _bfsSteps(adj, start) {
    const steps = [];
    const visited = new Set();
    const queue = [start];
    visited.add(start);

    while (queue.length) {
      const node = queue.shift();
      steps.push({
        step: steps.length + 1,
        current: node,
        visited: [...visited],
        frontier: [...queue],
        description: `Visiting node ${node}`,
      });

      for (const neighbor of adj[node] || []) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push(neighbor);
          steps.push({
            step: steps.length + 1,
            current: node,
            visited: [...visited],
            frontier: [...queue],
            edge_active: [node, neighbor],
            description: `Discovered node ${neighbor} from ${node}`,
          });
        }
      }
    }

    return steps;
  }

  function _dfsSteps(adj, start) {
    const steps = [];
    const visited = new Set();

    function dfs(node) {
      visited.add(node);
      steps.push({
        step: steps.length + 1,
        current: node,
        visited: [...visited],
        description: `Visiting node ${node}`,
      });

      for (const neighbor of adj[node] || []) {
        if (!visited.has(neighbor)) {
          steps.push({
            step: steps.length + 1,
            current: node,
            visited: [...visited],
            edge_active: [node, neighbor],
            description: `Exploring edge ${node} → ${neighbor}`,
          });
          dfs(neighbor);
        }
      }
    }

    dfs(start);
    return steps;
  }

  return {
    init,
    randomizeGraph,
    randomizeGrid,
    setGraph,
    loadSteps,
    nextStep,
    goToStep,
    resetPlayback,
    getProgress,
    getCurrentStep() { return steps[currentStep - 1] || {}; },
    get steps() { return steps; },
    get mode() { return mode; },
    get currentGraph() { return currentGraph; },
    get currentGrid() { return currentGrid; },
  };
})();

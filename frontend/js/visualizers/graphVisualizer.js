/* ═══════════════════════════════════════════════════
   AlgoVision — graphVisualizer.js
   Orchestrates graph algorithm step playback
   ═══════════════════════════════════════════════════ */

class GraphVisualizer {
  constructor(graphRenderer) {
    this.renderer = graphRenderer;
    this.nodes = [];
    this.edges = [];
    this.directed = false;
  }

  /**
   * Set the graph data
   */
  setGraph(nodes, edges, directed = false) {
    this.nodes = nodes;
    this.edges = edges;
    this.directed = directed;
    this.renderer.setGraph(nodes, edges, directed);
    this.renderer.render();
  }

  /**
   * Apply a step from the backend
   * Step format:
   * {
   *   step: number,
   *   visited: number[],           // node IDs that are visited
   *   current: number,             // currently processing node
   *   frontier: number[],          // nodes in queue/stack
   *   edge_active: [from, to],     // currently traversed edge
   *   path: number[],              // final path nodes
   *   mst_edges: [[from,to],...],  // MST edges (Kruskal/Prim)
   *   distances: { nodeId: dist }, // shortest distances (Dijkstra etc)
   *   description: string
   * }
   */
  applyStep(step) {
    // Reset all states
    this.renderer.resetStates();

    // Mark visited nodes
    if (step.visited) {
      step.visited.forEach(id => this.renderer.setNodeState(id, 'visited'));
    }

    // Mark frontier nodes
    if (step.frontier) {
      step.frontier.forEach(id => this.renderer.setNodeState(id, 'active'));
    }

    // Mark current node
    if (step.current != null) {
      this.renderer.setNodeState(step.current, 'current');
    }

    // Mark start/end
    if (step.start_node != null) {
      this.renderer.setNodeState(step.start_node, 'start');
    }
    if (step.end_node != null) {
      this.renderer.setNodeState(step.end_node, 'end');
    }

    // Mark active edge
    if (step.edge_active) {
      const [from, to] = step.edge_active;
      this.renderer.setEdgeState(from, to, 'active');
    }

    // Mark visited edges
    if (step.edges_visited) {
      step.edges_visited.forEach(([from, to]) => {
        this.renderer.setEdgeState(from, to, 'visited');
      });
    }

    // Mark MST edges
    if (step.mst_edges) {
      step.mst_edges.forEach(([from, to]) => {
        this.renderer.setEdgeState(from, to, 'mst');
      });
    }

    // Mark path
    if (step.path) {
      step.path.forEach(id => this.renderer.setNodeState(id, 'path'));
      // Mark path edges
      for (let i = 0; i < step.path.length - 1; i++) {
        this.renderer.setEdgeState(step.path[i], step.path[i + 1], 'path');
      }
    }

    // Render with updated states
    this.renderer.render();

    // Draw distance labels if present
    if (step.distances) {
      this._drawDistances(step.distances);
    }
  }

  /**
   * Draw distance labels near nodes
   */
  _drawDistances(distances) {
    const ctx = this.renderer.ctx;
    Object.entries(distances).forEach(([nodeId, dist]) => {
      const node = this.renderer.nodes[+nodeId];
      if (!node) return;

      const label = dist === Infinity ? '∞' : String(dist);
      const x = node.dx;
      const y = node.dy - this.renderer.nodeRadius - 12;

      // Background pill
      ctx.fillStyle = Helpers.getCSSVar('--bg-surface') || '#0f1424';
      ctx.strokeStyle = Helpers.getCSSVar('--border') || '#1e2a45';
      ctx.lineWidth = 1;
      const textW = ctx.measureText(label).width + 10;
      this.renderer.roundRect(x - textW / 2, y - 8, textW, 16, 4);
      ctx.fill();
      ctx.stroke();

      this.renderer.drawText(label, x, y, {
        font: '600 10px JetBrains Mono',
        color: Helpers.getCSSVar('--accent-light') || '#60a5fa',
      });
    });
  }

  /**
   * Reset visualization
   */
  reset() {
    this.renderer.resetStates();
    this.renderer.render();
  }
}

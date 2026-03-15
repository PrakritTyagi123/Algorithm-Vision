/* ═══════════════════════════════════════════════════
   AlgoVision — graphRenderer.js
   Graph-specific Canvas Rendering (Nodes + Edges)
   ═══════════════════════════════════════════════════ */

class GraphRenderer extends CanvasRenderer {
  constructor(canvasId = 'main-canvas') {
    super(canvasId);
    this.nodeRadius = 22;
    this.nodes = [];
    this.edges = [];
    this.nodeStates = {};  // nodeId → color/state
    this.edgeStates = {};  // "from-to" → color/state
    this.directed = false;
  }

  /**
   * Set graph data
   */
  setGraph(nodes, edges, directed = false) {
    this.nodes = nodes;
    this.edges = edges;
    this.directed = directed;
    this.nodeStates = {};
    this.edgeStates = {};

    // Scale node positions to fit canvas
    this._scaleToFit();
  }

  /**
   * Scale node positions to fit within canvas bounds
   */
  _scaleToFit() {
    if (!this.nodes.length) return;
    const padding = 60;
    const xs = this.nodes.map(n => n.x);
    const ys = this.nodes.map(n => n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const dataW = maxX - minX || 1;
    const dataH = maxY - minY || 1;
    const scaleX = (this.width - padding * 2) / dataW;
    const scaleY = (this.height - padding * 2) / dataH;
    const scale = Math.min(scaleX, scaleY, 1.5);

    const offsetX = (this.width - dataW * scale) / 2 - minX * scale;
    const offsetY = (this.height - dataH * scale) / 2 - minY * scale;

    this.nodes.forEach(n => {
      n.dx = n.x * scale + offsetX;
      n.dy = n.y * scale + offsetY;
    });
  }

  /**
   * Update a node's visual state
   */
  setNodeState(nodeId, state) {
    this.nodeStates[nodeId] = state;
  }

  /**
   * Update an edge's visual state
   */
  setEdgeState(from, to, state) {
    this.edgeStates[`${from}-${to}`] = state;
    if (!this.directed) {
      this.edgeStates[`${to}-${from}`] = state;
    }
  }

  /**
   * Reset all states
   */
  resetStates() {
    this.nodeStates = {};
    this.edgeStates = {};
  }

  /**
   * Get color for a node state
   */
  _nodeColor(state) {
    const colors = {
      default:  Helpers.getCSSVar('--color-default'),
      active:   Helpers.getCSSVar('--color-active'),
      visited:  Helpers.getCSSVar('--color-visited'),
      current:  Helpers.getCSSVar('--color-current'),
      path:     Helpers.getCSSVar('--color-path'),
      found:    Helpers.getCSSVar('--color-found'),
      start:    Helpers.getCSSVar('--color-start'),
      end:      Helpers.getCSSVar('--color-end'),
    };
    return colors[state] || colors.default;
  }

  /**
   * Get color for an edge state
   */
  _edgeColor(state) {
    const colors = {
      default:  Helpers.getCSSVar('--border-light') || '#2a3655',
      active:   Helpers.getCSSVar('--color-active'),
      visited:  Helpers.getCSSVar('--color-visited'),
      path:     Helpers.getCSSVar('--color-path'),
      mst:      Helpers.getCSSVar('--color-found'),
    };
    return colors[state] || colors.default;
  }

  /**
   * Render the complete graph
   */
  render() {
    this.clear();
    this._scaleToFit();

    // Draw edges first (below nodes)
    this._drawEdges();

    // Draw nodes on top
    this._drawNodes();
  }

  _drawEdges() {
    const ctx = this.ctx;
    const drawnEdges = new Set();

    this.edges.forEach(edge => {
      const key = this.directed ? `${edge.from}-${edge.to}` : [edge.from, edge.to].sort().join('-');
      if (!this.directed && drawnEdges.has(key)) return;
      drawnEdges.add(key);

      const fromNode = this.nodes[edge.from];
      const toNode = this.nodes[edge.to];
      if (!fromNode || !toNode) return;

      const state = this.edgeStates[`${edge.from}-${edge.to}`] || 'default';
      const color = this._edgeColor(state);
      const lineWidth = state === 'default' ? 1.5 : 3;

      if (this.directed) {
        // Shorten arrow to stop at node radius
        const angle = Math.atan2(toNode.dy - fromNode.dy, toNode.dx - fromNode.dx);
        const tx = toNode.dx - (this.nodeRadius + 4) * Math.cos(angle);
        const ty = toNode.dy - (this.nodeRadius + 4) * Math.sin(angle);
        const fx = fromNode.dx + (this.nodeRadius + 2) * Math.cos(angle);
        const fy = fromNode.dy + (this.nodeRadius + 2) * Math.sin(angle);
        this.drawArrow(fx, fy, tx, ty, { color, width: lineWidth });
      } else {
        this.drawLine(fromNode.dx, fromNode.dy, toNode.dx, toNode.dy, { color, width: lineWidth });
      }

      // Draw weight label
      if (edge.weight != null) {
        const mx = (fromNode.dx + toNode.dx) / 2;
        const my = (fromNode.dy + toNode.dy) / 2;
        // Background
        ctx.fillStyle = Helpers.getCSSVar('--bg-surface') || '#0f1424';
        ctx.fillRect(mx - 12, my - 9, 24, 18);
        this.drawText(edge.weight, mx, my, {
          font: '600 11px JetBrains Mono',
          color: state !== 'default' ? color : Helpers.getCSSVar('--text-secondary'),
        });
      }
    });
  }

  _drawNodes() {
    this.nodes.forEach(node => {
      const state = this.nodeStates[node.id] || 'default';
      const color = this._nodeColor(state);
      const isActive = state !== 'default';

      // Glow effect for active nodes
      if (isActive) {
        this.ctx.save();
        this.ctx.shadowColor = color;
        this.ctx.shadowBlur = 16;
        this.drawCircle(node.dx, node.dy, this.nodeRadius, {
          fill: color + '22',
          stroke: color,
          lineWidth: 3,
        });
        this.ctx.restore();
      }

      // Node circle
      this.drawCircle(node.dx, node.dy, this.nodeRadius, {
        fill: isActive ? color : (Helpers.getCSSVar('--bg-surface-3') || '#1a2238'),
        stroke: isActive ? color : (Helpers.getCSSVar('--border-light') || '#2a3655'),
        lineWidth: isActive ? 2.5 : 1.5,
      });

      // Node label
      this.drawText(node.label || node.id, node.dx, node.dy, {
        font: '600 13px JetBrains Mono',
        color: isActive ? '#fff' : Helpers.getCSSVar('--text-primary'),
      });
    });
  }
}

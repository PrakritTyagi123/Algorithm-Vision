/* ═══════════════════════════════════════════════════
   AlgoVision — treeVisualizer.js
   Renders tree data structures (BST, AVL, Trie, etc.)
   ═══════════════════════════════════════════════════ */

class TreeVisualizer {
  constructor(renderer) {
    this.renderer = renderer;
    this.tree = null;       // { value, left, right, x, y }
    this.nodeStates = {};   // value → state
    this.nodeRadius = 20;
    this.levelHeight = 70;
    this.minHSpacing = 40;
  }

  /**
   * Set the tree data and compute layout
   * @param {Object} treeData - nested { value, left, right } or { value, children }
   */
  setTree(treeData) {
    this.tree = treeData;
    this.nodeStates = {};
    if (this.tree) {
      this._computeLayout(this.tree, 0);
      this._centerTree();
    }
    this.render();
  }

  /**
   * Compute x,y positions for each node using a simple recursive layout
   */
  _computeLayout(node, depth) {
    if (!node) return { width: 0 };

    node.depth = depth;
    node.y = 50 + depth * this.levelHeight;

    const leftInfo = this._computeLayout(node.left, depth + 1);
    const rightInfo = this._computeLayout(node.right, depth + 1);

    const totalWidth = Math.max(this.minHSpacing, leftInfo.width + rightInfo.width + this.minHSpacing);

    // Position relative to subtree widths
    if (node.left && node.right) {
      node.left.xOffset = -totalWidth / 4;
      node.right.xOffset = totalWidth / 4;
    } else if (node.left) {
      node.left.xOffset = -this.minHSpacing / 2;
    } else if (node.right) {
      node.right.xOffset = this.minHSpacing / 2;
    }

    return { width: totalWidth };
  }

  /**
   * Convert relative offsets to absolute coordinates centered in canvas
   */
  _centerTree() {
    if (!this.tree) return;
    const cx = this.renderer.width / 2;
    this._setAbsolutePositions(this.tree, cx);
  }

  _setAbsolutePositions(node, parentX) {
    if (!node) return;
    node.x = parentX + (node.xOffset || 0);
    this._setAbsolutePositions(node.left, node.x);
    this._setAbsolutePositions(node.right, node.x);
  }

  /**
   * Apply a visualization step
   * @param {Object} step - {
   *   tree: { nested tree },
   *   highlighted: [values],
   *   visited: [values],
   *   current: value,
   *   path: [values],
   *   description: string
   * }
   */
  applyStep(step) {
    if (step.tree) {
      this.tree = step.tree;
      this._computeLayout(this.tree, 0);
      this._centerTree();
    }

    this.nodeStates = {};

    if (step.visited) {
      step.visited.forEach(v => (this.nodeStates[v] = 'visited'));
    }

    if (step.highlighted) {
      step.highlighted.forEach(v => (this.nodeStates[v] = 'active'));
    }

    if (step.current != null) {
      this.nodeStates[step.current] = 'current';
    }

    if (step.path) {
      step.path.forEach(v => (this.nodeStates[v] = 'path'));
    }

    if (step.inserted != null) {
      this.nodeStates[step.inserted] = 'found';
    }

    if (step.deleted != null) {
      this.nodeStates[step.deleted] = 'swap';
    }

    if (step.rotated) {
      step.rotated.forEach(v => (this.nodeStates[v] = 'compare'));
    }

    this.render();
  }

  /**
   * Render the tree
   */
  render() {
    this.renderer.clear();
    if (!this.tree) return;
    this._drawEdges(this.tree);
    this._drawNodes(this.tree);
  }

  _drawEdges(node) {
    if (!node) return;

    const ctx = this.renderer.ctx;

    if (node.left) {
      const color = this._edgeColor(node, node.left);
      this.renderer.drawLine(node.x, node.y, node.left.x, node.left.y, {
        color,
        width: 1.5,
      });
      this._drawEdges(node.left);
    }

    if (node.right) {
      const color = this._edgeColor(node, node.right);
      this.renderer.drawLine(node.x, node.y, node.right.x, node.right.y, {
        color,
        width: 1.5,
      });
      this._drawEdges(node.right);
    }
  }

  _drawNodes(node) {
    if (!node) return;

    const state = this.nodeStates[node.value] || 'default';
    const color = this._nodeColor(state);
    const isActive = state !== 'default';

    // Glow
    if (isActive) {
      this.renderer.ctx.save();
      this.renderer.ctx.shadowColor = color;
      this.renderer.ctx.shadowBlur = 14;
    }

    this.renderer.drawCircle(node.x, node.y, this.nodeRadius, {
      fill: isActive ? color : (Helpers.getCSSVar('--bg-surface-3') || '#1a2238'),
      stroke: isActive ? color : (Helpers.getCSSVar('--border-light') || '#2a3655'),
      lineWidth: isActive ? 2.5 : 1.5,
    });

    if (isActive) {
      this.renderer.ctx.restore();
    }

    // Value label
    this.renderer.drawText(String(node.value), node.x, node.y, {
      font: '600 12px JetBrains Mono',
      color: isActive ? '#fff' : Helpers.getCSSVar('--text-primary'),
    });

    // Balance factor for AVL
    if (node.bf != null) {
      this.renderer.drawText(`bf:${node.bf}`, node.x, node.y + this.nodeRadius + 12, {
        font: '400 9px JetBrains Mono',
        color: Helpers.getCSSVar('--text-tertiary'),
      });
    }

    // Color indicator for Red-Black tree
    if (node.color) {
      this.renderer.drawCircle(node.x + this.nodeRadius - 4, node.y - this.nodeRadius + 4, 4, {
        fill: node.color === 'red' ? '#ef4444' : '#333',
        stroke: '#fff',
        lineWidth: 1,
      });
    }

    this._drawNodes(node.left);
    this._drawNodes(node.right);
  }

  _nodeColor(state) {
    const map = {
      default:  Helpers.getCSSVar('--color-default'),
      active:   Helpers.getCSSVar('--color-active'),
      visited:  Helpers.getCSSVar('--color-visited'),
      current:  Helpers.getCSSVar('--color-current'),
      path:     Helpers.getCSSVar('--color-path'),
      found:    Helpers.getCSSVar('--color-found'),
      swap:     Helpers.getCSSVar('--color-swap'),
      compare:  Helpers.getCSSVar('--color-compare'),
    };
    return map[state] || map.default;
  }

  _edgeColor(parent, child) {
    const pState = this.nodeStates[parent.value];
    const cState = this.nodeStates[child.value];
    if (pState === 'path' && cState === 'path') {
      return Helpers.getCSSVar('--color-path');
    }
    if (pState === 'current' || cState === 'current') {
      return Helpers.getCSSVar('--color-current');
    }
    return Helpers.getCSSVar('--border-light') || '#2a3655';
  }

  /**
   * Reset
   */
  reset() {
    this.nodeStates = {};
    this.render();
  }
}

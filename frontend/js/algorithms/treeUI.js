/* ═══════════════════════════════════════════════════
   AlgoVision — treeUI.js
   UI Controller for: Tree, DP, Backtracking, String,
   Math, Data Structures
   ═══════════════════════════════════════════════════ */

const TreeUI = (() => {
  let treeViz = null;
  let dpViz = null;
  let canvasRenderer = null;
  let steps = [];
  let currentStep = 0;
  let currentCategory = 'tree';

  // Track which containers are visible
  let _canvasEl = null;
  let _dpContainerEl = null;

  function init(treeVisualizer, dpVisualizer, renderer) {
    treeViz = treeVisualizer;
    dpViz = dpVisualizer;
    canvasRenderer = renderer;
    _canvasEl = document.getElementById('main-canvas');
    _dpContainerEl = document.getElementById('dp-table-container');
  }

  /* ── Show/hide helpers ── */
  function _showCanvas() {
    if (_canvasEl) _canvasEl.style.display = 'block';
    if (_dpContainerEl) _dpContainerEl.style.display = 'none';
    // Force reflow then resize so drawing gets correct dimensions
    if (canvasRenderer) {
      _canvasEl.offsetHeight; // force reflow
      canvasRenderer.resize();
    }
  }
  function _showDP() {
    if (_canvasEl) _canvasEl.style.display = 'none';
    if (_dpContainerEl) _dpContainerEl.style.display = 'flex';
  }
  function _showBoth() {
    if (_canvasEl) _canvasEl.style.display = 'block';
    if (_dpContainerEl) _dpContainerEl.style.display = 'flex';
    if (canvasRenderer) {
      _canvasEl.offsetHeight;
      canvasRenderer.resize();
    }
  }

  /* ── Setup functions ── */

  function randomTree(size = 10) {
    const values = Helpers.randomArray(size, 1, 99);
    const tree = _buildBST(values);
    treeViz.setTree(tree);
    _showCanvas();
    resetPlayback();
    return values;
  }

  function _buildBST(values) {
    let root = null;
    function insert(node, val) {
      if (!node) return { value: val, left: null, right: null };
      if (val < node.value) node.left = insert(node.left, val);
      else if (val > node.value) node.right = insert(node.right, val);
      return node;
    }
    [...new Set(values)].forEach(v => (root = insert(root, v)));
    return root;
  }

  function initBoard(size = 8) {
    currentCategory = 'backtracking';
    _showDP();
    dpViz.initBoard(size);
    resetPlayback();
  }

  /* ── Load steps from backend ── */

  async function loadSteps(category, algorithm, params = {}) {
    currentCategory = category;
    if (!params || typeof params !== 'object') params = {};

    try {
      let data;
      switch (category) {
        case 'tree':
          data = await API.getTreeSteps(algorithm, params.values || Helpers.randomArray(8, 1, 50));
          break;
        case 'dp':
          data = await API.getDPSteps(algorithm, params);
          break;
        case 'backtracking':
          data = await API.getBacktrackingSteps(algorithm, params);
          break;
        case 'string':
          data = await API.getStringSteps(algorithm, params.text || 'ABABDABACDABABCABAB', params.pattern || 'ABABCABAB');
          break;
        case 'math':
          data = await API.getMathSteps(algorithm, params);
          break;
        case 'datastructure':
          data = await API.getDataStructureSteps(algorithm, params.operations || []);
          break;
        default:
          data = [];
      }

      steps = data.steps || data;
      currentStep = 0;

      // ── Auto-detect and init the right visualizer ──
      _autoInitVisualizer(steps, category);

      return steps;
    } catch (err) {
      console.error(`Failed to load ${category} steps:`, err);
      steps = _generateClientSteps(category, algorithm, params);
      currentStep = 0;
      return steps;
    }
  }

  /**
   * Scan steps to determine what visualizer to use, then init it.
   */
  function _autoInitVisualizer(steps, category) {
    if (!steps.length) return;

    // Find first step with renderable data
    const firstTable = steps.find(s => s.table);
    const firstBoard = steps.find(s => s.board);
    const firstTree = steps.find(s => s.tree);
    const firstArray = steps.find(s => s.array);

    if (firstBoard) {
      // Board visualization (n-queens, sudoku, knights, rat-maze, word-search)
      const size = firstBoard.board.length;
      _showDP();
      dpViz.initBoard(size);
    } else if (firstTable) {
      // Table visualization (DP, string, math)
      const s = firstTable;
      const rows = s.table.length;
      const cols = Array.isArray(s.table[0]) ? s.table[0].length : 1;
      _showDP();
      dpViz.initTable(rows, cols, s.row_headers || null, s.col_headers || null);
    } else if (firstTree) {
      // Tree visualization
      _showCanvas();
    } else if (firstArray) {
      // Array visualization (segment tree, fenwick, graph coloring, DS)
      _showCanvas();
    } else {
      // Description-only — show DP container for text display
      _showDP();
      dpViz.show();
    }
  }

  /* ── Step-by-step playback ── */

  function nextStep() {
    if (currentStep >= steps.length) return false;

    const step = steps[currentStep];

    // Smart dispatch based on step data (not category)
    if (step.tree) {
      _showCanvas();
      treeViz.applyStep(step);
    } else if (step.board) {
      _showDP();
      dpViz.applyBoardStep(step);
    } else if (step.table) {
      _showDP();
      const rows = step.table.length;
      const cols = Array.isArray(step.table[0]) ? step.table[0].length : 1;
      if (!dpViz.cells || !dpViz.cells.length || dpViz.rows !== rows || dpViz.cols !== cols) {
        dpViz.initTable(rows, cols, step.row_headers || null, step.col_headers || null);
      }
      dpViz.applyStep(step);
    } else if (step.array) {
      _showCanvas();
      _renderDSArray(step);
    }

    currentStep++;
    return currentStep < steps.length;
  }

  function goToStep(index) {
    currentStep = 0;
    treeViz.reset();
    dpViz.reset();

    // Re-init visualizer
    if (steps.length) _autoInitVisualizer(steps, currentCategory);

    const target = Helpers.clamp(index, 0, steps.length);
    while (currentStep < target) {
      nextStep();
    }
  }

  function resetPlayback() {
    steps = [];
    currentStep = 0;
  }

  function getProgress() {
    return { current: currentStep, total: steps.length };
  }

  function getCurrentStep() {
    return steps[currentStep - 1] || {};
  }

  /* ── DS Array Renderer (canvas) ── */

  function _renderDSArray(step) {
    const ctx = canvasRenderer.ctx;
    canvasRenderer.clear();

    const arr = step.array || [];
    if (!arr.length) return;

    const w = canvasRenderer.width;
    const h = canvasRenderer.height;
    const maxCellW = 60;
    const cellW = Math.min(maxCellW, (w - 80) / arr.length);
    const startX = (w - arr.length * cellW) / 2;
    const y = h / 2 - 25;

    arr.forEach((val, i) => {
      const x = startX + i * cellW;

      // Determine state
      const isActive = step.active && (Array.isArray(step.active) ? step.active.includes(i) : step.active === i);
      const isSwap = step.swap && (Array.isArray(step.swap) ? step.swap.includes(i) : step.swap === i);
      const isCurrent = step.current === i;
      const isSorted = step.sorted && (Array.isArray(step.sorted) ? step.sorted.includes(i) : false);

      let bgColor = '#efefef';
      let textColor = '#000';
      let borderColor = '#ddd';

      if (isCurrent) {
        bgColor = '#e76f51'; textColor = '#fff'; borderColor = '#e76f51';
      } else if (isSwap) {
        bgColor = '#f4a261'; textColor = '#fff'; borderColor = '#f4a261';
      } else if (isActive) {
        bgColor = '#457b9d'; textColor = '#fff'; borderColor = '#457b9d';
      } else if (isSorted) {
        bgColor = '#2a9d8f'; textColor = '#fff'; borderColor = '#2a9d8f';
      }

      // Cell box
      ctx.fillStyle = bgColor;
      canvasRenderer.roundRect(x + 2, y, cellW - 4, 50, 5);
      ctx.fill();
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Value
      canvasRenderer.drawText(String(val), x + cellW / 2, y + 25, {
        font: `600 ${Math.min(14, cellW * 0.4)}px JetBrains Mono`,
        color: textColor,
      });

      // Index below
      canvasRenderer.drawText(String(i), x + cellW / 2, y + 62, {
        font: '400 9px JetBrains Mono',
        color: '#bbb',
      });
    });

    // Pointers
    if (step.pointers) {
      Object.entries(step.pointers).forEach(([name, idx]) => {
        if (idx == null || idx < 0 || idx >= arr.length) return;
        const x = startX + idx * cellW + cellW / 2;
        canvasRenderer.drawText(`↑ ${name}`, x, y + 80, {
          font: '600 10px JetBrains Mono',
          color: '#e76f51',
        });
      });
    }
  }

  /* ── Client-side fallback ── */

  function _generateClientSteps(category, algorithm, params) {
    return [{
      step: 1,
      description: `${algorithm}: connect backend for full visualization (python run.py)`,
    }];
  }

  /* ── Public API ── */
  return {
    init,
    randomTree,
    initBoard,
    loadSteps,
    nextStep,
    goToStep,
    resetPlayback,
    getProgress,
    getCurrentStep,
    get steps() { return steps; },
  };
})();

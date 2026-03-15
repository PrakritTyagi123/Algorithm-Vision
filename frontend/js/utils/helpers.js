/* ═══════════════════════════════════════════════════
   AlgoVision — helpers.js
   Shared utility functions
   ═══════════════════════════════════════════════════ */

const Helpers = (() => {
  /**
   * Generate a random integer array
   * @param {number} size - array length
   * @param {number} min - minimum value (inclusive)
   * @param {number} max - maximum value (inclusive)
   * @returns {number[]}
   */
  function randomArray(size = 30, min = 5, max = 100) {
    return Array.from({ length: size }, () =>
      Math.floor(Math.random() * (max - min + 1)) + min
    );
  }

  /**
   * Generate a nearly-sorted array
   */
  function nearlySortedArray(size = 30, swaps = 3) {
    const arr = Array.from({ length: size }, (_, i) => i + 1);
    for (let s = 0; s < swaps; s++) {
      const i = Math.floor(Math.random() * size);
      const j = Math.floor(Math.random() * size);
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  /**
   * Generate a reversed array
   */
  function reversedArray(size = 30) {
    return Array.from({ length: size }, (_, i) => size - i);
  }

  /**
   * Sleep utility for async animations
   */
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Clamp a value between min and max
   */
  function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
  }

  /**
   * Linearly interpolate between a and b
   */
  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  /**
   * Ease-out cubic
   */
  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  /**
   * Ease-in-out sine
   */
  function easeInOutSine(t) {
    return -(Math.cos(Math.PI * t) - 1) / 2;
  }

  /**
   * Throttle function
   */
  function throttle(fn, limit) {
    let inThrottle = false;
    return function (...args) {
      if (!inThrottle) {
        fn.apply(this, args);
        inThrottle = true;
        setTimeout(() => (inThrottle = false), limit);
      }
    };
  }

  /**
   * Debounce function
   */
  function debounce(fn, wait) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), wait);
    };
  }

  /**
   * Convert speed slider value (1-100) to delay in ms
   * speed=1 → 1000ms, speed=100 → 5ms
   */
  function speedToDelay(speed) {
    const minDelay = 5;
    const maxDelay = 1000;
    // Exponential mapping for better feel
    const t = (speed - 1) / 99;
    return Math.round(maxDelay * Math.pow(minDelay / maxDelay, t));
  }

  /**
   * Get a CSS variable value from the root
   */
  function getCSSVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /**
   * Parse a color string (hex or rgb) to {r, g, b}
   */
  function parseColor(color) {
    if (color.startsWith('#')) {
      const hex = color.slice(1);
      return {
        r: parseInt(hex.substring(0, 2), 16),
        g: parseInt(hex.substring(2, 4), 16),
        b: parseInt(hex.substring(4, 6), 16),
      };
    }
    const match = color.match(/\d+/g);
    if (match) {
      return { r: +match[0], g: +match[1], b: +match[2] };
    }
    return { r: 100, g: 100, b: 100 };
  }

  /**
   * Generate a random graph (adjacency list with weights)
   * @param {number} nodeCount
   * @param {number} edgeDensity - 0 to 1
   * @param {boolean} directed
   * @returns {{ nodes: Array, edges: Array }}
   */
  function randomGraph(nodeCount = 8, edgeDensity = 0.4, directed = false) {
    const nodes = [];
    const edges = [];

    // Place nodes in a circular layout
    const cx = 400, cy = 300, radius = 200;
    for (let i = 0; i < nodeCount; i++) {
      const angle = (2 * Math.PI * i) / nodeCount - Math.PI / 2;
      nodes.push({
        id: i,
        label: String.fromCharCode(65 + i), // A, B, C, ...
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle),
      });
    }

    // Generate edges
    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        if (Math.random() < edgeDensity) {
          const weight = Math.floor(Math.random() * 20) + 1;
          edges.push({ from: i, to: j, weight });
          if (!directed) {
            edges.push({ from: j, to: i, weight });
          }
        }
      }
    }

    // Ensure connectivity
    for (let i = 1; i < nodeCount; i++) {
      const hasEdge = edges.some(
        e => (e.from === i && e.to < i) || (e.to === i && e.from < i)
      );
      if (!hasEdge) {
        const j = Math.floor(Math.random() * i);
        const weight = Math.floor(Math.random() * 20) + 1;
        edges.push({ from: j, to: i, weight });
        if (!directed) {
          edges.push({ from: i, to: j, weight });
        }
      }
    }

    return { nodes, edges };
  }

  /**
   * Generate a random maze grid
   * @param {number} rows
   * @param {number} cols
   * @param {number} wallRatio - 0 to 1
   * @returns {{ grid: number[][], start: [number, number], end: [number, number] }}
   */
  function randomGrid(rows = 20, cols = 30, wallRatio = 0.25) {
    const grid = [];
    for (let r = 0; r < rows; r++) {
      const row = [];
      for (let c = 0; c < cols; c++) {
        row.push(Math.random() < wallRatio ? 1 : 0);
      }
      grid.push(row);
    }
    const start = [1, 1];
    const end = [rows - 2, cols - 2];
    grid[start[0]][start[1]] = 0;
    grid[end[0]][end[1]] = 0;

    // Carve a guaranteed path: go right then down (with slight randomness)
    let r = start[0], c = start[1];
    while (r !== end[0] || c !== end[1]) {
      grid[r][c] = 0;
      // Also clear neighbors for wider path
      if (r > 0) grid[r-1][c] = 0;
      if (r < rows-1) grid[r+1][c] = 0;

      if (c < end[1] && (r === end[0] || Math.random() < 0.6)) {
        c++;
      } else if (r < end[0]) {
        r++;
      } else if (c < end[1]) {
        c++;
      }
    }
    grid[end[0]][end[1]] = 0;

    return { grid, start, end };
  }

  /**
   * Deep clone an object (simple, no circular refs)
   */
  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  /**
   * Format a number with commas
   */
  function formatNumber(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  return {
    randomArray,
    nearlySortedArray,
    reversedArray,
    sleep,
    clamp,
    lerp,
    easeOutCubic,
    easeInOutSine,
    throttle,
    debounce,
    speedToDelay,
    getCSSVar,
    parseColor,
    randomGraph,
    randomGrid,
    deepClone,
    formatNumber,
  };
})();

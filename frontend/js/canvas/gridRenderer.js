/* ═══════════════════════════════════════════════════
   AlgoVision — gridRenderer.js
   Grid-based Canvas Rendering (Pathfinding, Backtracking)
   ═══════════════════════════════════════════════════ */

class GridRenderer {
  constructor(containerId = 'grid-container') {
    this.container = document.getElementById(containerId);
    this.rows = 0;
    this.cols = 0;
    this.grid = [];
    this.cellElements = [];
    this.cellSize = 28;
    this.start = null;
    this.end = null;
    this.onCellClick = null; // callback(row, col)
  }

  /**
   * Show the grid container
   */
  show() {
    this.container.style.display = 'grid';
  }

  /**
   * Hide the grid container
   */
  hide() {
    this.container.style.display = 'none';
  }

  /**
   * Initialize grid from a 2D array
   * @param {number[][]} gridData - 0=open, 1=wall
   * @param {number[]} start - [row, col]
   * @param {number[]} end - [row, col]
   */
  initGrid(gridData, start, end) {
    this.grid = gridData;
    this.rows = gridData.length;
    this.cols = gridData[0].length;
    this.start = start;
    this.end = end;
    this.cellElements = [];

    // Calculate cell size to fit container
    const containerRect = this.container.parentElement.getBoundingClientRect();
    const availW = containerRect.width - 40;
    const availH = containerRect.height - 40;
    this.cellSize = Math.floor(Math.min(availW / this.cols, availH / this.rows));
    this.cellSize = Helpers.clamp(this.cellSize, 12, 40);

    // Set grid CSS
    this.container.style.gridTemplateColumns = `repeat(${this.cols}, ${this.cellSize}px)`;
    this.container.style.gridTemplateRows = `repeat(${this.rows}, ${this.cellSize}px)`;
    this.container.style.justifyContent = 'center';
    this.container.style.alignContent = 'center';
    this.container.style.gap = '1px';

    // Clear and build cells
    this.container.innerHTML = '';

    for (let r = 0; r < this.rows; r++) {
      this.cellElements[r] = [];
      for (let c = 0; c < this.cols; c++) {
        const cell = document.createElement('div');
        cell.className = 'grid-cell';
        cell.dataset.row = r;
        cell.dataset.col = c;

        // Set initial state
        if (r === start[0] && c === start[1]) {
          cell.style.background = Helpers.getCSSVar('--color-start');
          cell.title = 'Start';
        } else if (r === end[0] && c === end[1]) {
          cell.style.background = Helpers.getCSSVar('--color-end');
          cell.title = 'End';
        } else if (gridData[r][c] === 1) {
          cell.style.background = Helpers.getCSSVar('--color-wall');
          cell.title = 'Wall';
        } else {
          cell.style.background = Helpers.getCSSVar('--bg-surface-3');
        }

        // Click handler for toggling walls
        cell.addEventListener('click', () => {
          if (this.onCellClick) {
            this.onCellClick(r, c);
          }
        });

        this.container.appendChild(cell);
        this.cellElements[r][c] = cell;
      }
    }

    this.show();
  }

  /**
   * Set a single cell's state
   */
  setCellState(row, col, state) {
    const cell = this.cellElements[row]?.[col];
    if (!cell) return;

    const colors = {
      open:    Helpers.getCSSVar('--bg-surface-3'),
      wall:    Helpers.getCSSVar('--color-wall'),
      visited: Helpers.getCSSVar('--color-visited'),
      current: Helpers.getCSSVar('--color-current'),
      path:    Helpers.getCSSVar('--color-path'),
      start:   Helpers.getCSSVar('--color-start'),
      end:     Helpers.getCSSVar('--color-end'),
      frontier: Helpers.getCSSVar('--color-compare'),
    };

    cell.style.background = colors[state] || colors.open;

    // Animate visited cells
    if (state === 'visited' || state === 'frontier') {
      cell.style.animation = 'cellVisited 400ms ease-out';
    } else if (state === 'path') {
      cell.style.animation = 'cellPath 300ms ease-out';
    }
  }

  /**
   * Reset all cells to initial state
   */
  resetStates() {
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        if (r === this.start[0] && c === this.start[1]) {
          this.setCellState(r, c, 'start');
        } else if (r === this.end[0] && c === this.end[1]) {
          this.setCellState(r, c, 'end');
        } else if (this.grid[r][c] === 1) {
          this.setCellState(r, c, 'wall');
        } else {
          this.setCellState(r, c, 'open');
        }
        // Remove animation
        const cell = this.cellElements[r]?.[c];
        if (cell) cell.style.animation = '';
      }
    }
  }

  /**
   * Toggle a wall cell
   */
  toggleWall(row, col) {
    if ((row === this.start[0] && col === this.start[1]) ||
        (row === this.end[0] && col === this.end[1])) return;

    this.grid[row][col] = this.grid[row][col] === 1 ? 0 : 1;
    this.setCellState(row, col, this.grid[row][col] === 1 ? 'wall' : 'open');
  }

  /**
   * Destroy grid
   */
  destroy() {
    this.container.innerHTML = '';
    this.hide();
  }
}

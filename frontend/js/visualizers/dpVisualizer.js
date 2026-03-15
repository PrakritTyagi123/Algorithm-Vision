/* ═══════════════════════════════════════════════════
   AlgoVision — dpVisualizer.js
   Renders DP tables, backtracking boards, string alignment
   ═══════════════════════════════════════════════════ */

class DPVisualizer {
  constructor() {
    this.container = document.getElementById('dp-table-container');
    this.table = null;
    this.rows = 0;
    this.cols = 0;
    this.cells = [];  // 2D array of <td> elements
  }

  /**
   * Show the DP table container
   */
  show() {
    this.container.style.display = 'flex';
  }

  /**
   * Hide the DP table container
   */
  hide() {
    this.container.style.display = 'none';
  }

  /**
   * Initialize a DP table
   * @param {number} rows
   * @param {number} cols
   * @param {string[]} rowHeaders - optional row labels
   * @param {string[]} colHeaders - optional column labels
   */
  initTable(rows, cols, rowHeaders = null, colHeaders = null) {
    this.rows = rows;
    this.cols = cols;
    this.cells = [];

    // Build table HTML
    this.container.innerHTML = '';
    this.table = document.createElement('table');
    this.table.className = 'dp-table';

    // Column headers
    if (colHeaders) {
      const thead = document.createElement('thead');
      const tr = document.createElement('tr');
      if (rowHeaders) {
        tr.appendChild(document.createElement('th')); // corner cell
      }
      colHeaders.forEach(h => {
        const th = document.createElement('th');
        th.textContent = h;
        tr.appendChild(th);
      });
      thead.appendChild(tr);
      this.table.appendChild(thead);
    }

    // Body rows
    const tbody = document.createElement('tbody');
    for (let r = 0; r < rows; r++) {
      const tr = document.createElement('tr');
      this.cells[r] = [];

      if (rowHeaders && rowHeaders[r] != null) {
        const th = document.createElement('th');
        th.textContent = rowHeaders[r];
        tr.appendChild(th);
      }

      for (let c = 0; c < cols; c++) {
        const td = document.createElement('td');
        td.textContent = '';
        td.dataset.row = r;
        td.dataset.col = c;
        tr.appendChild(td);
        this.cells[r][c] = td;
      }

      tbody.appendChild(tr);
    }
    this.table.appendChild(tbody);
    this.container.appendChild(this.table);
    this.show();
  }

  /**
   * Apply a DP step
   * @param {Object} step - {
   *   table: number[][],       // full table state
   *   current: [row, col],     // currently filling cell
   *   highlighted: [[r,c],...], // cells being referenced
   *   filled: [[r,c],...],     // already filled cells
   *   description: string
   * }
   */
  applyStep(step) {
    // Update table values
    if (step.table) {
      for (let r = 0; r < this.rows; r++) {
        for (let c = 0; c < this.cols; c++) {
          if (step.table[r] && step.table[r][c] != null) {
            const val = step.table[r][c];
            this.cells[r][c].textContent = val === Infinity ? '∞' : val === -Infinity ? '-∞' : val;
          }
        }
      }
    }

    // Reset all cell classes
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        this.cells[r][c].className = '';
        if (this.cells[r][c].textContent !== '') {
          this.cells[r][c].className = 'dp-filled';
        }
      }
    }

    // Highlight referenced cells
    if (step.highlighted) {
      step.highlighted.forEach(([r, c]) => {
        if (this.cells[r]?.[c]) {
          this.cells[r][c].className = 'dp-highlight';
        }
      });
    }

    // Mark current cell
    if (step.current) {
      const [r, c] = step.current;
      if (this.cells[r]?.[c]) {
        this.cells[r][c].className = 'dp-current';
      }
    }

    // Mark path cells (for traceback)
    if (step.path) {
      step.path.forEach(([r, c]) => {
        if (this.cells[r]?.[c]) {
          this.cells[r][c].className = 'dp-highlight';
        }
      });
    }
  }

  /**
   * Initialize an N×N board (for N-Queens, Sudoku, etc.)
   * @param {number} size
   */
  initBoard(size) {
    this.initTable(size, size);
    // Style as a chess-like board
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        if ((r + c) % 2 === 0) {
          this.cells[r][c].style.background = Helpers.getCSSVar('--bg-surface-2');
        } else {
          this.cells[r][c].style.background = Helpers.getCSSVar('--bg-surface-3');
        }
      }
    }
  }

  /**
   * Apply a board step (N-Queens, Sudoku, Knight's Tour)
   * @param {Object} step - {
   *   board: (string|number)[][],
   *   current: [row, col],
   *   placed: [[r,c],...],
   *   conflict: [[r,c],...],
   *   description: string
   * }
   */
  applyBoardStep(step) {
    const size = this.rows;

    // Reset board colors
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const baseColor = (r + c) % 2 === 0
          ? Helpers.getCSSVar('--bg-surface-2')
          : Helpers.getCSSVar('--bg-surface-3');
        this.cells[r][c].style.background = baseColor;
        this.cells[r][c].style.color = Helpers.getCSSVar('--text-primary');
        this.cells[r][c].style.fontSize = '1.1rem';

        if (step.board && step.board[r]) {
          const val = step.board[r][c];
          this.cells[r][c].textContent = val === 0 || val === '' || val == null ? '' : val;
        }
      }
    }

    // Highlight placed pieces
    if (step.placed) {
      step.placed.forEach(([r, c]) => {
        if (this.cells[r]?.[c]) {
          this.cells[r][c].style.background = Helpers.getCSSVar('--color-sorted');
          this.cells[r][c].style.color = '#fff';
        }
      });
    }

    // Highlight conflicts
    if (step.conflict) {
      step.conflict.forEach(([r, c]) => {
        if (this.cells[r]?.[c]) {
          this.cells[r][c].style.background = Helpers.getCSSVar('--color-swap');
          this.cells[r][c].style.color = '#fff';
        }
      });
    }

    // Highlight current cell
    if (step.current) {
      const [r, c] = step.current;
      if (this.cells[r]?.[c]) {
        this.cells[r][c].style.background = Helpers.getCSSVar('--color-current');
        this.cells[r][c].style.color = '#fff';
        this.cells[r][c].style.boxShadow = '0 0 8px rgba(249, 115, 22, 0.5)';
      }
    }
  }

  /**
   * Reset
   */
  reset() {
    this.container.innerHTML = '';
    this.cells = [];
  }

  /**
   * Destroy
   */
  destroy() {
    this.reset();
    this.hide();
  }
}

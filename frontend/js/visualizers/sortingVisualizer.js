/* ═══════════════════════════════════════════════════
   AlgoVision — sortingVisualizer.js
   Renders sorting AND searching algorithm steps as bars.
   Sorting: compare(red), swap(orange), sorted(teal), active(blue)
   Searching: current(coral), range bracket, dimmed eliminated,
              found(green pulse), pointer labels (low/mid/high)
   ═══════════════════════════════════════════════════ */

class SortingVisualizer {
  constructor(renderer) {
    this.renderer = renderer;
    this.array = [];
    this.barStates = [];
    this.pointers = {};
    this.range = null;       // [lo, hi] active search zone
    this.maxVal = 100;
    this.barGap = 2;
    this.mode = 'sort';      // 'sort' or 'search'
  }

  /* ── Public API ── */

  setArray(arr) {
    this.array = [...arr];
    this.maxVal = Math.max(...arr, 1);
    this.barStates = new Array(arr.length).fill('default');
    this.pointers = {};
    this.range = null;
    this.render();
  }

  setMode(mode) {
    this.mode = mode; // 'sort' or 'search'
  }

  applyStep(step) {
    if (step.array) {
      this.array = [...step.array];
      this.maxVal = Math.max(...this.array, 1);
    }

    const n = this.array.length;
    this.barStates = new Array(n).fill('default');

    // 1. Sorted / checked
    if (step.sorted && Array.isArray(step.sorted)) {
      step.sorted.forEach(i => {
        if (i >= 0 && i < n) {
          this.barStates[i] = this.mode === 'search' ? 'checked' : 'sorted';
        }
      });
    }

    // 2. Compare
    if (step.compare && Array.isArray(step.compare)) {
      step.compare.forEach(i => {
        if (i >= 0 && i < n) this.barStates[i] = 'compare';
      });
    }

    // 3. Swap
    if (step.swap && Array.isArray(step.swap)) {
      step.swap.forEach(i => {
        if (i >= 0 && i < n) this.barStates[i] = 'swap';
      });
    }

    // 4. Active
    if (step.active != null) {
      const indices = Array.isArray(step.active) ? step.active : [step.active];
      indices.forEach(i => {
        if (i >= 0 && i < n) this.barStates[i] = 'active';
      });
    }

    // 5. Found
    if (step.found != null) {
      const indices = Array.isArray(step.found) ? step.found : [step.found];
      indices.forEach(i => {
        if (i >= 0 && i < n) this.barStates[i] = 'found';
      });
    }

    // 6. Current pointer
    if (step.current != null && step.current >= 0 && step.current < n) {
      this.barStates[step.current] = 'current';
    }

    // 7. Pointers
    this.pointers = step.pointers || {};

    // 8. Range (search zone) — dim everything outside
    this.range = step.range || null;
    if (this.range) {
      const [lo, hi] = this.range;
      for (let i = 0; i < n; i++) {
        if ((i < lo || i > hi) && this.barStates[i] === 'default') {
          this.barStates[i] = 'dimmed';
        }
      }
    }

    this.render();
  }

  markAllSorted() {
    this.barStates = new Array(this.array.length).fill('sorted');
    this.pointers = {};
    this.range = null;
    this.render();
  }

  /* ── Core Render ── */

  render() {
    const { renderer, array, barStates, maxVal, barGap } = this;
    const ctx = renderer.ctx;
    const w = renderer.width;
    const h = renderer.height;

    renderer.clear();
    if (!array.length) return;

    // Layout
    const pad = { top: 24, bottom: 48, left: 28, right: 28 };
    const availW = w - pad.left - pad.right;
    const availH = (h - pad.top - pad.bottom) * 0.85;
    const barW = Math.max(1, (availW - barGap * (array.length - 1)) / array.length);
    const showLabels = barW >= 16 && array.length <= 50;
    const showIndices = barW >= 12 && array.length <= 70;

    // ── Draw range bracket (searching) ──
    if (this.range && this.mode === 'search') {
      this._drawRangeBracket(pad, barW, barGap, h, availH);
    }

    // ── Draw bars ──
    array.forEach((val, i) => {
      const barH = Math.max(2, (val / maxVal) * availH);
      const x = pad.left + i * (barW + barGap);
      const y = h - pad.bottom - barH;
      const state = barStates[i];
      const color = this._color(state);

      // Glow for active states (skip for thin bars)
      const isActive = ['compare', 'swap', 'current', 'found', 'active'].includes(state);
      if (isActive && barW > 2) {
        ctx.save();
        ctx.shadowColor = color;
        ctx.shadowBlur = barW > 6 ? 10 : 4;
        ctx.shadowOffsetY = 1;
      }

      // Bar shape
      ctx.fillStyle = color;
      if (barW > 3) {
        renderer.roundRect(x, y, barW, barH, Math.min(barW / 4, 3));
        ctx.fill();
      } else {
        ctx.fillRect(x, y, Math.max(barW, 1), barH);
      }

      if (isActive && barW > 2) ctx.restore();

      // Value label above bar
      if (showLabels) {
        const labelColor = isActive ? color : '#000';
        renderer.drawText(val, x + barW / 2, y - 10, {
          font: `600 ${Math.min(11, Math.max(8, barW * 0.55))}px JetBrains Mono`,
          color: labelColor,
        });
      }

      // Index label below bar
      if (showIndices) {
        renderer.drawText(i, x + barW / 2, h - pad.bottom + 12, {
          font: `400 ${Math.min(9, Math.max(7, barW * 0.45))}px JetBrains Mono`,
          color: '#bbb',
        });
      }
    });

    // ── Draw pointer labels ──
    this._drawPointers(pad, barW, barGap, h);
  }

  /* ── Range Bracket (searching) ── */

  _drawRangeBracket(pad, barW, barGap, canvasH, availH) {
    if (!this.range) return;
    const [lo, hi] = this.range;
    const ctx = this.renderer.ctx;
    const x1 = pad.left + lo * (barW + barGap) - 2;
    const x2 = pad.left + hi * (barW + barGap) + barW + 2;
    const y = pad.top - 2;
    const bracketH = canvasH - pad.top - pad.bottom + 4;

    // Subtle highlight zone
    ctx.fillStyle = 'rgba(59, 130, 246, 0.04)';
    ctx.fillRect(x1, y, x2 - x1, bracketH);

    // Bracket lines
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 3]);

    // Left bracket
    ctx.beginPath();
    ctx.moveTo(x1, y + 6);
    ctx.lineTo(x1, y);
    ctx.lineTo(x1 + 8, y);
    ctx.stroke();

    // Right bracket
    ctx.beginPath();
    ctx.moveTo(x2, y + 6);
    ctx.lineTo(x2, y);
    ctx.lineTo(x2 - 8, y);
    ctx.stroke();

    // Bottom brackets
    const bY = y + bracketH;
    ctx.beginPath();
    ctx.moveTo(x1, bY - 6);
    ctx.lineTo(x1, bY);
    ctx.lineTo(x1 + 8, bY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x2, bY - 6);
    ctx.lineTo(x2, bY);
    ctx.lineTo(x2 - 8, bY);
    ctx.stroke();

    ctx.setLineDash([]);

    // Range label
    this.renderer.drawText(`[${lo}..${hi}]`, (x1 + x2) / 2, y - 6, {
      font: '500 9px JetBrains Mono',
      color: '#3b82f6',
    });
  }

  /* ── Pointer Labels ── */

  _drawPointers(pad, barW, barGap, canvasH) {
    const colorMap = {
      low:  '#3b82f6', high: '#ef4444', mid:  '#f97316',
      mid1: '#f97316', mid2: '#8b5cf6',
      pos:  '#f97316', probe: '#f97316',
      left: '#3b82f6', right: '#ef4444',
      pivot: '#f59e0b', i: '#2a9d8f', j: '#6c5ce7',
      min: '#00b4d8', block_start: '#3b82f6', block_end: '#3b82f6',
    };

    const pointerY = canvasH - pad.bottom + 26;

    Object.entries(this.pointers).forEach(([name, index]) => {
      if (index == null || index < 0 || index >= this.array.length) return;

      const x = pad.left + index * (barW + barGap) + barW / 2;
      const color = colorMap[name] || '#f97316';
      const ctx = this.renderer.ctx;

      // Triangle
      ctx.beginPath();
      ctx.fillStyle = color;
      ctx.moveTo(x, pointerY - 6);
      ctx.lineTo(x - 4, pointerY + 1);
      ctx.lineTo(x + 4, pointerY + 1);
      ctx.closePath();
      ctx.fill();

      // Label
      this.renderer.drawText(name, x, pointerY + 11, {
        font: '600 8px JetBrains Mono',
        color,
      });
    });
  }

  /* ── Color Map ── */

  _color(state) {
    const colors = {
      default:  '#c4c4c4',                  // light grey
      compare:  '#e63946',                  // red — comparing
      swap:     '#f4a261',                  // orange — swapping
      sorted:   '#2a9d8f',                  // teal — sorted/done
      active:   '#457b9d',                  // blue — active/pivot
      current:  '#e76f51',                  // coral — current probe
      found:    '#06d6a0',                  // bright green — found!
      checked:  '#b8d8d0',                  // light teal — already checked (search)
      dimmed:   '#e8e8e8',                  // very light grey — eliminated
    };
    return colors[state] || colors.default;
  }
}

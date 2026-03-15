/* ═══════════════════════════════════════════════════
   AlgoVision — canvasRenderer.js
   Base Canvas Rendering Engine
   ═══════════════════════════════════════════════════ */

class CanvasRenderer {
  constructor(canvasId = 'main-canvas') {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.dpr = window.devicePixelRatio || 1;
    this.width = 0;
    this.height = 0;
    this.animationId = null;

    // Bind resize
    this._resizeHandler = Helpers.debounce(() => this.resize(), 100);
    window.addEventListener('resize', this._resizeHandler);
    this.resize();
  }

  /**
   * Resize canvas to fit container, accounting for device pixel ratio
   */
  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.width = rect.width;
    this.height = rect.height;
    this.canvas.width = this.width * this.dpr;
    this.canvas.height = this.height * this.dpr;
    this.canvas.style.width = this.width + 'px';
    this.canvas.style.height = this.height + 'px';
    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
  }

  /**
   * Clear the entire canvas
   */
  clear() {
    this.ctx.clearRect(0, 0, this.width, this.height);
  }

  /**
   * Fill background
   */
  fillBackground(color) {
    this.ctx.fillStyle = color || Helpers.getCSSVar('--bg-root');
    this.ctx.fillRect(0, 0, this.width, this.height);
  }

  /**
   * Draw a rounded rectangle
   */
  roundRect(x, y, w, h, r = 4) {
    const ctx = this.ctx;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  /**
   * Draw text centered at position
   */
  drawText(text, x, y, {
    font = '12px Outfit',
    color = '#fff',
    align = 'center',
    baseline = 'middle',
  } = {}) {
    const ctx = this.ctx;
    ctx.font = font;
    ctx.fillStyle = color;
    ctx.textAlign = align;
    ctx.textBaseline = baseline;
    ctx.fillText(text, x, y);
  }

  /**
   * Draw a circle
   */
  drawCircle(x, y, radius, { fill, stroke, lineWidth = 2 } = {}) {
    const ctx = this.ctx;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    if (fill) {
      ctx.fillStyle = fill;
      ctx.fill();
    }
    if (stroke) {
      ctx.strokeStyle = stroke;
      ctx.lineWidth = lineWidth;
      ctx.stroke();
    }
  }

  /**
   * Draw a line between two points
   */
  drawLine(x1, y1, x2, y2, { color = '#555', width = 1.5, dash = [] } = {}) {
    const ctx = this.ctx;
    ctx.beginPath();
    ctx.setLineDash(dash);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  /**
   * Draw an arrow from (x1,y1) to (x2,y2)
   */
  drawArrow(x1, y1, x2, y2, { color = '#555', width = 1.5, headSize = 8 } = {}) {
    const ctx = this.ctx;
    const angle = Math.atan2(y2 - y1, x2 - x1);
    // Shorten line to stop at arrowhead base
    const dx = x2 - headSize * Math.cos(angle);
    const dy = y2 - headSize * Math.sin(angle);

    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.moveTo(x1, y1);
    ctx.lineTo(dx, dy);
    ctx.stroke();

    // Arrowhead
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.moveTo(x2, y2);
    ctx.lineTo(
      x2 - headSize * Math.cos(angle - Math.PI / 6),
      y2 - headSize * Math.sin(angle - Math.PI / 6)
    );
    ctx.lineTo(
      x2 - headSize * Math.cos(angle + Math.PI / 6),
      y2 - headSize * Math.sin(angle + Math.PI / 6)
    );
    ctx.closePath();
    ctx.fill();
  }

  /**
   * Stop any running animation loop
   */
  stopAnimation() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  /**
   * Destroy and cleanup
   */
  destroy() {
    this.stopAnimation();
    window.removeEventListener('resize', this._resizeHandler);
  }
}

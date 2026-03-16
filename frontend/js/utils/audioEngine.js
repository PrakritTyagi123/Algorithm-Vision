/* ═══════════════════════════════════════════════════
   AlgoVision — audioEngine.js
   Sequential ascending octave sonification.
   Each step plays the next note up a scale.
   Sorting sounds like a rising melody.
   ═══════════════════════════════════════════════════ */

const AudioEngine = (() => {
  let ctx = null;
  let isEnabled = false;
  let vol = 0.3;

  // Musical scale: C major across 2 octaves
  // C4=262, D4=294, E4=330, F4=349, G4=392, A4=440, B4=494,
  // C5=523, D5=587, E5=659, F5=698, G5=784, A5=880, B5=988, C6=1047
  const SCALE = [
    262, 294, 330, 349, 392, 440, 494,
    523, 587, 659, 698, 784, 880, 988, 1047
  ];

  // Track position in the ascending sequence
  let noteIndex = 0;

  function _ensureCtx() {
    if (!ctx) {
      try {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
      } catch (e) { return false; }
    }
    if (ctx.state === 'suspended') ctx.resume();
    return true;
  }

  function toggle() {
    isEnabled = !isEnabled;
    if (isEnabled && _ensureCtx()) {
      noteIndex = 0;
      _beep(SCALE[0], 0.15, 'sine', 0);
    }
    return isEnabled;
  }

  function setEnabled(v) { isEnabled = v; if (v) _ensureCtx(); }
  function setVolume(v) { vol = Math.max(0, Math.min(1, v)); }

  // Not used in sequential mode but kept for API compat
  function setMaxValue() {}

  function resetSequence() { noteIndex = 0; }

  /* ── Core beep ── */
  function _beep(freq, duration, wave, pan) {
    if (!ctx) return;
    if (ctx.state === 'suspended') ctx.resume();

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = wave || 'sine';
    osc.frequency.setValueAtTime(freq, now);

    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(vol, now + 0.006);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

    if (typeof pan === 'number' && ctx.createStereoPanner) {
      const panner = ctx.createStereoPanner();
      panner.pan.setValueAtTime(Math.max(-1, Math.min(1, pan)), now);
      osc.connect(gain);
      gain.connect(panner);
      panner.connect(ctx.destination);
    } else {
      osc.connect(gain);
      gain.connect(ctx.destination);
    }

    osc.start(now);
    osc.stop(now + duration + 0.02);
  }

  /* ── Get next ascending note, wrapping through octaves ── */
  function _nextNote() {
    const freq = SCALE[noteIndex % SCALE.length];
    noteIndex++;
    return freq;
  }

  /* ── Map array index to stereo pan ── */
  function _pan(idx, len) {
    if (len <= 1) return 0;
    return (idx / (len - 1)) * 2 - 1;
  }

  /* ══════════════════════════════════════════════════
     Play sound for a step — always ascending
     ══════════════════════════════════════════════════ */
  function playStep(step, arrayLen) {
    if (!isEnabled || !ctx) return;

    const arr = step.array;
    const len = arrayLen || (arr ? arr.length : 1);

    // Compare — play next note in sequence
    if (step.compare && Array.isArray(step.compare) && step.compare.length > 0) {
      const idx = step.compare[0];
      _beep(_nextNote(), 0.07, 'sine', _pan(idx, len));
      return;
    }

    // Swap — triangle, next note
    if (step.swap && Array.isArray(step.swap) && step.swap.length > 0) {
      const idx = step.swap[0];
      _beep(_nextNote(), 0.09, 'triangle', _pan(idx, len));
      return;
    }

    // Found — long satisfying high note
    if (step.found) {
      _beep(SCALE[SCALE.length - 1], 0.3, 'sine', 0);
      return;
    }

    // Current
    if (step.current != null) {
      const idx = Array.isArray(step.current) ? (step.current[1] ?? step.current[0]) : step.current;
      _beep(_nextNote(), 0.06, 'sine', _pan(idx, len));
      return;
    }

    // Active
    if (step.active) {
      const indices = Array.isArray(step.active) ? step.active : [step.active];
      _beep(_nextNote(), 0.06, 'sine', _pan(indices[0], len));
      return;
    }

    // Sorted marker — gentle ascending
    if (step.sorted && Array.isArray(step.sorted) && step.sorted.length > 0) {
      const idx = step.sorted[step.sorted.length - 1];
      _beep(_nextNote(), 0.1, 'sine', _pan(idx, len));
    }
  }

  /* ── Completion: fast ascending arpeggio through full scale ── */
  function playComplete(arr) {
    if (!isEnabled || !ctx) return;
    const notes = SCALE.length;
    for (let i = 0; i < notes; i++) {
      setTimeout(() => {
        _beep(SCALE[i], 0.12, 'sine', (i / notes) * 2 - 1);
      }, i * 40);
    }
    // Final high chord
    setTimeout(() => {
      _beep(1047, 0.4, 'sine', 0);   // C6
      _beep(1319, 0.4, 'sine', -0.5); // E6
      _beep(1568, 0.4, 'sine', 0.5);  // G6
    }, notes * 40 + 50);
  }

  /* ── Graph/tree ── */
  function playNode(nodeId, totalNodes, action) {
    if (!isEnabled || !ctx) return;
    _beep(_nextNote(), action === 'found' ? 0.25 : 0.07, 'sine', 0);
  }

  /* ── Table/board ── */
  function playCell(row, col, totalCols, action) {
    if (!isEnabled || !ctx) return;
    _beep(_nextNote(), 0.06, 'sine', _pan(col, totalCols));
  }

  return {
    toggle,
    setEnabled,
    setVolume,
    setMaxValue,
    resetSequence,
    playStep,
    playComplete,
    playNode,
    playCell,
    get enabled() { return isEnabled; },
  };
})();
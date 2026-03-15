/* ═══════════════════════════════════════════════════
   AlgoVision — sortingUI.js
   UI Controller for Sorting & Searching Algorithms
   ═══════════════════════════════════════════════════ */

const SortingUI = (() => {
  let visualizer = null;
  let currentArray = [];
  let steps = [];
  let currentStep = 0;

  /**
   * Initialize the sorting UI with a visualizer instance
   */
  function init(sortingVisualizer) {
    visualizer = sortingVisualizer;
  }

  /**
   * Generate and display a new random array
   */
  function randomize(size) {
    currentArray = Helpers.randomArray(size, 5, 100);
    visualizer.setArray(currentArray);
    resetPlayback();
    return currentArray;
  }

  /**
   * Set a custom array
   */
  function setArray(arr) {
    currentArray = [...arr];
    visualizer.setArray(currentArray);
    resetPlayback();
  }

  /**
   * Fetch steps from the backend and prepare playback
   */
  async function loadSteps(category, algorithm, target = null) {
    try {
      let data;
      if (category === 'searching') {
        const t = target != null ? target : currentArray[Math.floor(Math.random() * currentArray.length)];
        data = await API.getSearchingSteps(algorithm, currentArray, t);
      } else {
        data = await API.getSortingSteps(algorithm, currentArray);
      }

      steps = data.steps || data;
      currentStep = 0;

      // For searching: show sorted array immediately (backend sorts it)
      if (category === 'searching' && steps.length && steps[0].array) {
        currentArray = [...steps[0].array];
        visualizer.setArray(currentArray);
      }

      return steps;
    } catch (err) {
      console.error('Failed to load steps:', err);
      // Fallback: generate client-side steps
      steps = _generateClientSteps(algorithm, [...currentArray]);
      currentStep = 0;
      return steps;
    }
  }

  /**
   * Get the current step
   */
  function getCurrentStep() {
    return steps[currentStep] || null;
  }

  /**
   * Advance to next step and apply it
   * @returns {boolean} true if there are more steps
   */
  function nextStep() {
    if (currentStep >= steps.length) return false;

    const step = steps[currentStep];
    visualizer.applyStep(step);
    currentStep++;

    // Mark all sorted on final step
    if (currentStep >= steps.length) {
      visualizer.markAllSorted();
    }

    return currentStep < steps.length;
  }

  /**
   * Go to a specific step
   */
  function goToStep(index) {
    currentStep = Helpers.clamp(index, 0, steps.length);
    if (currentStep < steps.length) {
      visualizer.applyStep(steps[currentStep]);
    }
  }

  /**
   * Reset playback to start
   */
  function resetPlayback() {
    steps = [];
    currentStep = 0;
    visualizer.setArray(currentArray);
  }

  /**
   * Get playback progress info
   */
  function getProgress() {
    return {
      current: currentStep,
      total: steps.length,
      percent: steps.length ? (currentStep / steps.length) * 100 : 0,
    };
  }

  /**
   * Client-side fallback: generate visualization steps for common sorting algorithms
   * This runs when the backend is unavailable
   */
  function _generateClientSteps(algorithm, arr) {
    switch (algorithm) {
      case 'bubble': return _bubbleSortSteps(arr);
      case 'selection': return _selectionSortSteps(arr);
      case 'insertion': return _insertionSortSteps(arr);
      case 'quick': return _quickSortSteps(arr);
      case 'merge': return _mergeSortSteps(arr);
      default: return _bubbleSortSteps(arr);
    }
  }

  function _bubbleSortSteps(arr) {
    const a = [...arr];
    const steps = [];
    const sorted = [];
    const n = a.length;

    for (let i = 0; i < n - 1; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        steps.push({
          step: steps.length + 1,
          array: [...a],
          compare: [j, j + 1],
          swap: null,
          sorted: [...sorted],
          description: `Comparing index ${j} (${a[j]}) and ${j+1} (${a[j+1]})`,
        });

        if (a[j] > a[j + 1]) {
          [a[j], a[j + 1]] = [a[j + 1], a[j]];
          steps.push({
            step: steps.length + 1,
            array: [...a],
            compare: null,
            swap: [j, j + 1],
            sorted: [...sorted],
            description: `Swapping ${a[j+1]} and ${a[j]}`,
          });
        }
      }
      sorted.push(n - 1 - i);
    }
    sorted.push(0);

    steps.push({
      step: steps.length + 1,
      array: [...a],
      compare: null,
      swap: null,
      sorted: Array.from({ length: n }, (_, i) => i),
      description: 'Array is sorted!',
    });

    return steps;
  }

  function _selectionSortSteps(arr) {
    const a = [...arr];
    const steps = [];
    const sorted = [];
    const n = a.length;

    for (let i = 0; i < n - 1; i++) {
      let minIdx = i;
      for (let j = i + 1; j < n; j++) {
        steps.push({
          step: steps.length + 1,
          array: [...a],
          compare: [minIdx, j],
          active: [i],
          sorted: [...sorted],
          pointers: { min: minIdx, j },
          description: `Finding minimum: comparing index ${minIdx} (${a[minIdx]}) with ${j} (${a[j]})`,
        });

        if (a[j] < a[minIdx]) {
          minIdx = j;
        }
      }

      if (minIdx !== i) {
        [a[i], a[minIdx]] = [a[minIdx], a[i]];
        steps.push({
          step: steps.length + 1,
          array: [...a],
          swap: [i, minIdx],
          sorted: [...sorted],
          description: `Swapping index ${i} and ${minIdx}`,
        });
      }
      sorted.push(i);
    }
    sorted.push(n - 1);

    steps.push({
      step: steps.length + 1,
      array: [...a],
      sorted: Array.from({ length: n }, (_, i) => i),
      description: 'Array is sorted!',
    });

    return steps;
  }

  function _insertionSortSteps(arr) {
    const a = [...arr];
    const steps = [];
    const n = a.length;

    for (let i = 1; i < n; i++) {
      const key = a[i];
      let j = i - 1;

      steps.push({
        step: steps.length + 1,
        array: [...a],
        active: [i],
        description: `Inserting element at index ${i} (value: ${key})`,
      });

      while (j >= 0 && a[j] > key) {
        steps.push({
          step: steps.length + 1,
          array: [...a],
          compare: [j, j + 1],
          description: `Comparing ${a[j]} > ${key}`,
        });

        a[j + 1] = a[j];
        j--;

        steps.push({
          step: steps.length + 1,
          array: [...a],
          swap: [j + 1, j + 2],
          description: `Shifting element right`,
        });
      }
      a[j + 1] = key;

      steps.push({
        step: steps.length + 1,
        array: [...a],
        active: [j + 1],
        sorted: Array.from({ length: i + 1 }, (_, k) => k),
        description: `Placed ${key} at index ${j + 1}`,
      });
    }

    steps.push({
      step: steps.length + 1,
      array: [...a],
      sorted: Array.from({ length: n }, (_, i) => i),
      description: 'Array is sorted!',
    });

    return steps;
  }

  function _quickSortSteps(arr) {
    const a = [...arr];
    const steps = [];

    function quickSort(lo, hi) {
      if (lo >= hi) return;

      const pivotVal = a[hi];
      steps.push({
        step: steps.length + 1,
        array: [...a],
        active: [hi],
        range: [lo, hi],
        pointers: { pivot: hi },
        description: `Pivot = ${pivotVal} (index ${hi})`,
      });

      let i = lo;
      for (let j = lo; j < hi; j++) {
        steps.push({
          step: steps.length + 1,
          array: [...a],
          compare: [j, hi],
          pointers: { i, j, pivot: hi },
          range: [lo, hi],
          description: `Comparing ${a[j]} with pivot ${pivotVal}`,
        });

        if (a[j] <= pivotVal) {
          if (i !== j) {
            [a[i], a[j]] = [a[j], a[i]];
            steps.push({
              step: steps.length + 1,
              array: [...a],
              swap: [i, j],
              range: [lo, hi],
              description: `Swapping ${a[j]} and ${a[i]}`,
            });
          }
          i++;
        }
      }

      [a[i], a[hi]] = [a[hi], a[i]];
      steps.push({
        step: steps.length + 1,
        array: [...a],
        swap: [i, hi],
        description: `Placing pivot ${pivotVal} at index ${i}`,
      });

      quickSort(lo, i - 1);
      quickSort(i + 1, hi);
    }

    quickSort(0, a.length - 1);

    steps.push({
      step: steps.length + 1,
      array: [...a],
      sorted: Array.from({ length: a.length }, (_, i) => i),
      description: 'Array is sorted!',
    });

    return steps;
  }

  function _mergeSortSteps(arr) {
    const a = [...arr];
    const steps = [];

    function mergeSort(lo, hi) {
      if (lo >= hi) return;
      const mid = Math.floor((lo + hi) / 2);

      steps.push({
        step: steps.length + 1,
        array: [...a],
        range: [lo, hi],
        active: [mid],
        description: `Splitting [${lo}..${hi}] at mid=${mid}`,
      });

      mergeSort(lo, mid);
      mergeSort(mid + 1, hi);

      // Merge
      const left = a.slice(lo, mid + 1);
      const right = a.slice(mid + 1, hi + 1);
      let i = 0, j = 0, k = lo;

      while (i < left.length && j < right.length) {
        steps.push({
          step: steps.length + 1,
          array: [...a],
          compare: [lo + i, mid + 1 + j],
          range: [lo, hi],
          description: `Merging: comparing ${left[i]} and ${right[j]}`,
        });

        if (left[i] <= right[j]) {
          a[k] = left[i];
          i++;
        } else {
          a[k] = right[j];
          j++;
        }
        k++;

        steps.push({
          step: steps.length + 1,
          array: [...a],
          active: [k - 1],
          range: [lo, hi],
          description: `Placed ${a[k-1]} at index ${k-1}`,
        });
      }

      while (i < left.length) { a[k] = left[i]; i++; k++; }
      while (j < right.length) { a[k] = right[j]; j++; k++; }

      steps.push({
        step: steps.length + 1,
        array: [...a],
        range: [lo, hi],
        sorted: Array.from({ length: hi - lo + 1 }, (_, idx) => lo + idx),
        description: `Merged range [${lo}..${hi}]`,
      });
    }

    mergeSort(0, a.length - 1);

    steps.push({
      step: steps.length + 1,
      array: [...a],
      sorted: Array.from({ length: a.length }, (_, i) => i),
      description: 'Array is sorted!',
    });

    return steps;
  }

  return {
    init,
    randomize,
    setArray,
    loadSteps,
    getCurrentStep,
    nextStep,
    goToStep,
    resetPlayback,
    getProgress,
    get currentArray() { return currentArray; },
    get steps() { return steps; },
  };
})();

/* ═══════════════════════════════════════════════════
   AlgoVision — api.js
   Backend API Communication Layer
   ═══════════════════════════════════════════════════ */

const API = (() => {
  const BASE_URL = 'http://localhost:8000';

  /**
   * Generic fetch wrapper with error handling
   */
  async function request(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint}`;
    try {
      const response = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
      });
      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `HTTP ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  // ─── SORTING ───
  function getSortingSteps(algorithm, array) {
    const params = new URLSearchParams({ array: array.join(',') });
    return request(`/sorting/${algorithm}?${params}`);
  }

  // ─── SEARCHING ───
  function getSearchingSteps(algorithm, array, target) {
    const params = new URLSearchParams({
      array: array.join(','),
      target: target,
    });
    return request(`/searching/${algorithm}?${params}`);
  }

  // ─── GRAPH ───
  function getGraphSteps(algorithm, nodes, edges, startNode = 0, endNode = null) {
    return request(`/graph/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify({ nodes, edges, start_node: startNode, end_node: endNode }),
    });
  }

  // ─── TREE ───
  function getTreeSteps(algorithm, values, operation = 'build') {
    return request(`/tree/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify({ values, operation }),
    });
  }

  // ─── PATHFINDING ───
  function getPathfindingSteps(algorithm, grid, start, end) {
    return request(`/pathfinding/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify({ grid, start, end }),
    });
  }

  // ─── DYNAMIC PROGRAMMING ───
  function getDPSteps(algorithm, params) {
    return request(`/dp/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  // ─── BACKTRACKING ───
  function getBacktrackingSteps(algorithm, params) {
    return request(`/backtracking/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  // ─── STRING ───
  function getStringSteps(algorithm, text, pattern) {
    const params = new URLSearchParams({ text, pattern });
    return request(`/string/${algorithm}?${params}`);
  }

  // ─── MATH ───
  function getMathSteps(algorithm, params) {
    return request(`/math/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  // ─── DATA STRUCTURES ───
  function getDataStructureSteps(algorithm, operations) {
    return request(`/datastructure/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify({ operations }),
    });
  }

  // ─── GEOMETRY ───
  function getGeometrySteps(algorithm, points, segments) {
    return request(`/geometry/${algorithm}`, {
      method: 'POST',
      body: JSON.stringify({ points, segments }),
    });
  }

  // ─── REGISTRY ───
  function getRegistry() {
    return request('/registry');
  }

  // ─── HEALTH CHECK ───
  async function healthCheck() {
    try {
      const data = await request('/health');
      return data.status === 'ok';
    } catch {
      return false;
    }
  }

  return {
    BASE_URL,
    request,
    getSortingSteps,
    getSearchingSteps,
    getGraphSteps,
    getTreeSteps,
    getPathfindingSteps,
    getDPSteps,
    getBacktrackingSteps,
    getStringSteps,
    getMathSteps,
    getDataStructureSteps,
    getGeometrySteps,
    getRegistry,
    healthCheck,
  };
})();

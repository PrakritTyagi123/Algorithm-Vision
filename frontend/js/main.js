/* ═══════════════════════════════════════════════════
   AlgoVision — main.js
   Application Orchestrator
   Wires together UI, visualizers, API, and controls
   ═══════════════════════════════════════════════════ */

(() => {
  'use strict';

  // ─── ALGORITHM REGISTRY ───
  // Complete list of every algorithm organized by category
  const REGISTRY = {
    sorting: [
      { id: 'bubble',     name: 'Bubble Sort',     time: 'O(n²)',     space: 'O(1)',     stable: 'Yes',  desc: 'Repeatedly swaps adjacent elements if they are in the wrong order.' },
      { id: 'selection',  name: 'Selection Sort',  time: 'O(n²)',     space: 'O(1)',     stable: 'No',   desc: 'Finds the minimum element and places it at the beginning.' },
      { id: 'insertion',  name: 'Insertion Sort',  time: 'O(n²)',     space: 'O(1)',     stable: 'Yes',  desc: 'Builds the sorted array one item at a time by inserting each element into its correct position.' },
      { id: 'merge',      name: 'Merge Sort',      time: 'O(n log n)', space: 'O(n)',    stable: 'Yes',  desc: 'Divides array in half, sorts each half, then merges them.' },
      { id: 'quick',      name: 'Quick Sort',      time: 'O(n log n)', space: 'O(log n)', stable: 'No', desc: 'Picks a pivot, partitions array around it, then recursively sorts sub-arrays.' },
      { id: 'heap',       name: 'Heap Sort',       time: 'O(n log n)', space: 'O(1)',    stable: 'No',   desc: 'Builds a max heap and repeatedly extracts the maximum.' },
      { id: 'shell',      name: 'Shell Sort',      time: 'O(n log²n)', space: 'O(1)',   stable: 'No',   desc: 'Generalization of insertion sort using diminishing gap sequences.' },
      { id: 'counting',   name: 'Counting Sort',   time: 'O(n+k)',    space: 'O(k)',     stable: 'Yes',  desc: 'Counts occurrences of each value to determine positions.' },
      { id: 'radix',      name: 'Radix Sort',      time: 'O(d·n)',    space: 'O(n+k)',   stable: 'Yes',  desc: 'Sorts digit by digit from least significant to most significant.' },
      { id: 'bucket',     name: 'Bucket Sort',     time: 'O(n+k)',    space: 'O(n)',     stable: 'Yes',  desc: 'Distributes elements into buckets, sorts each, then concatenates.' },
      { id: 'tim',        name: 'Tim Sort',        time: 'O(n log n)', space: 'O(n)',    stable: 'Yes',  desc: 'Hybrid of merge sort and insertion sort used in Python and Java.' },
      { id: 'cocktail',   name: 'Cocktail Sort',   time: 'O(n²)',     space: 'O(1)',     stable: 'Yes',  desc: 'Bidirectional bubble sort that traverses in both directions.' },
      { id: 'comb',       name: 'Comb Sort',       time: 'O(n²)',     space: 'O(1)',     stable: 'No',   desc: 'Improves on bubble sort by comparing elements with a gap that shrinks.' },
      { id: 'gnome',      name: 'Gnome Sort',      time: 'O(n²)',     space: 'O(1)',     stable: 'Yes',  desc: 'Similar to insertion sort but moves elements by swapping.' },
      { id: 'bitonic',    name: 'Bitonic Sort',    time: 'O(n log²n)', space: 'O(1)',   stable: 'No',   desc: 'Parallel sorting algorithm that creates bitonic sequences and merges them.' },
    ],
    searching: [
      { id: 'linear',        name: 'Linear Search',        time: 'O(n)',      space: 'O(1)', stable: '—', desc: 'Checks each element one by one.' },
      { id: 'binary',        name: 'Binary Search',        time: 'O(log n)',  space: 'O(1)', stable: '—', desc: 'Divides sorted array in half repeatedly.' },
      { id: 'jump',          name: 'Jump Search',          time: 'O(√n)',     space: 'O(1)', stable: '—', desc: 'Jumps ahead by fixed blocks, then does linear search.' },
      { id: 'interpolation', name: 'Interpolation Search', time: 'O(log log n)', space: 'O(1)', stable: '—', desc: 'Estimates position based on value distribution.' },
      { id: 'exponential',   name: 'Exponential Search',   time: 'O(log n)',  space: 'O(1)', stable: '—', desc: 'Finds range by doubling, then binary search within range.' },
      { id: 'fibonacci',     name: 'Fibonacci Search',     time: 'O(log n)',  space: 'O(1)', stable: '—', desc: 'Divides array using Fibonacci numbers.' },
      { id: 'ternary',       name: 'Ternary Search',       time: 'O(log₃n)', space: 'O(1)', stable: '—', desc: 'Divides sorted array into three parts.' },
    ],
    graph: [
      { id: 'bfs',             name: 'BFS',                    time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Explores all neighbors at current depth before moving deeper.' },
      { id: 'dfs',             name: 'DFS',                    time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Explores as far as possible along each branch before backtracking.' },
      { id: 'dijkstra',        name: 'Dijkstra',               time: 'O(V² / E log V)', space: 'O(V)', stable: '—', desc: 'Finds shortest path from source to all vertices (non-negative weights).' },
      { id: 'bellman_ford',    name: 'Bellman-Ford',           time: 'O(V·E)',    space: 'O(V)',   stable: '—', desc: 'Finds shortest paths; handles negative weights.' },
      { id: 'floyd_warshall',  name: 'Floyd-Warshall',         time: 'O(V³)',     space: 'O(V²)',  stable: '—', desc: 'All-pairs shortest path using dynamic programming.' },
      { id: 'a_star',          name: 'A* Search',              time: 'O(E)',      space: 'O(V)',   stable: '—', desc: 'Uses heuristic to find shortest path efficiently.' },
      { id: 'kruskal',         name: 'Kruskal (MST)',          time: 'O(E log E)', space: 'O(V)', stable: '—', desc: 'Builds MST by greedily adding cheapest edges.' },
      { id: 'prim',            name: 'Prim (MST)',             time: 'O(V²)',     space: 'O(V)',   stable: '—', desc: 'Builds MST by growing from a starting vertex.' },
      { id: 'boruvka',         name: 'Borůvka (MST)',          time: 'O(E log V)', space: 'O(V)', stable: '—', desc: 'Builds MST by connecting components with cheapest edges.' },
      { id: 'topological',     name: 'Topological Sort',       time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Linear ordering of DAG vertices respecting edge directions.' },
      { id: 'kosaraju',        name: 'Kosaraju SCC',           time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Finds strongly connected components using two DFS passes.' },
      { id: 'tarjan',          name: 'Tarjan SCC',             time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Finds SCCs in a single DFS pass.' },
      { id: 'bridges',         name: 'Bridges',                time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Finds edges whose removal disconnects the graph.' },
      { id: 'articulation',    name: 'Articulation Points',    time: 'O(V+E)',    space: 'O(V)',   stable: '—', desc: 'Finds vertices whose removal disconnects the graph.' },
      { id: 'euler_path',      name: 'Euler Path / Circuit',   time: 'O(V+E)',    space: 'O(V+E)', stable: '—', desc: 'Finds a path that visits every edge exactly once.' },
      { id: 'ford_fulkerson',  name: 'Ford-Fulkerson',         time: 'O(V·E²)',   space: 'O(V²)',  stable: '—', desc: 'Computes maximum flow in a flow network.' },
      { id: 'edmonds_karp',    name: 'Edmonds-Karp',           time: 'O(V·E²)',   space: 'O(V²)',  stable: '—', desc: 'BFS-based implementation of Ford-Fulkerson for max flow.' },
      { id: 'union_find',      name: 'Union-Find / DSU',       time: 'O(α(n))',   space: 'O(n)',   stable: '—', desc: 'Disjoint Set Union with path compression and union by rank.' },
      { id: 'kahns',           name: "Kahn's Topological Sort", time: 'O(V+E)',   space: 'O(V)',   stable: '—', desc: 'BFS-based topological sort using in-degree counting.' },
      { id: 'cycle_directed',  name: 'Cycle Detection (Directed)', time: 'O(V+E)', space: 'O(V)', stable: '—', desc: 'Detect cycles in directed graphs using DFS coloring.' },
      { id: 'cycle_undirected', name: 'Cycle Detection (Undirected)', time: 'O(V+E)', space: 'O(V)', stable: '—', desc: 'Detect cycles in undirected graphs using DFS.' },
      { id: 'johnson',         name: "Johnson's Algorithm",    time: 'O(V²logV+VE)', space: 'O(V²)', stable: '—', desc: 'All-pairs shortest paths for sparse graphs.' },
    ],
    geometry: [
      { id: 'convex_hull_graham', name: 'Convex Hull (Graham Scan)', time: 'O(n log n)', space: 'O(n)', stable: '—', desc: 'Compute convex hull by sorting points by polar angle.' },
      { id: 'convex_hull_jarvis', name: 'Convex Hull (Jarvis March)', time: 'O(nh)', space: 'O(n)', stable: '—', desc: 'Compute convex hull via gift wrapping.' },
      { id: 'closest_pair',    name: 'Closest Pair of Points', time: 'O(n log n)', space: 'O(n)', stable: '—', desc: 'Find two closest points using divide and conquer.' },
      { id: 'line_intersection', name: 'Line Segment Intersection', time: 'O(n²)', space: 'O(1)', stable: '—', desc: 'Check all segment pairs for intersections.' },
      { id: 'sweep_line',      name: 'Sweep Line Algorithm', time: 'O((n+k) log n)', space: 'O(n)', stable: '—', desc: 'Detect intersections using a sweep line.' },
    ],
    tree: [
      { id: 'inorder',    name: 'Inorder Traversal',  time: 'O(n)', space: 'O(h)', stable: '—', desc: 'Left → Root → Right traversal.' },
      { id: 'preorder',   name: 'Preorder Traversal', time: 'O(n)', space: 'O(h)', stable: '—', desc: 'Root → Left → Right traversal.' },
      { id: 'postorder',  name: 'Postorder Traversal', time: 'O(n)', space: 'O(h)', stable: '—', desc: 'Left → Right → Root traversal.' },
      { id: 'levelorder', name: 'Level-Order Traversal', time: 'O(n)', space: 'O(w)', stable: '—', desc: 'Breadth-first, level by level traversal.' },
      { id: 'bst',        name: 'BST Operations',     time: 'O(h)',  space: 'O(h)', stable: '—', desc: 'Insert, search, and delete in a Binary Search Tree.' },
      { id: 'avl',        name: 'AVL Tree',           time: 'O(log n)', space: 'O(n)', stable: '—', desc: 'Self-balancing BST using rotation after every insert/delete.' },
      { id: 'red_black',  name: 'Red-Black Tree',     time: 'O(log n)', space: 'O(n)', stable: '—', desc: 'Self-balancing BST with red/black coloring rules.' },
      { id: 'segment',    name: 'Segment Tree',       time: 'O(log n)', space: 'O(n)', stable: '—', desc: 'Tree for efficient range queries and updates.' },
      { id: 'fenwick',    name: 'Fenwick Tree (BIT)', time: 'O(log n)', space: 'O(n)', stable: '—', desc: 'Binary Indexed Tree for prefix sums.' },
      { id: 'trie',       name: 'Trie',               time: 'O(m)',  space: 'O(m·n)', stable: '—', desc: 'Prefix tree for efficient string operations.' },
      { id: 'lca',        name: 'Lowest Common Ancestor', time: 'O(h)', space: 'O(1)', stable: '—', desc: 'Find the lowest common ancestor of two nodes in a BST.' },
      { id: 'height',     name: 'Tree Height',         time: 'O(n)',  space: 'O(h)', stable: '—', desc: 'Compute the height of a binary tree.' },
      { id: 'diameter',   name: 'Tree Diameter',        time: 'O(n)', space: 'O(h)', stable: '—', desc: 'Find the longest path between any two nodes.' },
    ],
    pathfinding: [
      { id: 'a_star_grid',    name: 'A* (Grid)',            time: 'O(E)',    space: 'O(V)', stable: '—', desc: 'Optimal pathfinding using heuristic on a grid.' },
      { id: 'dijkstra_grid',  name: 'Dijkstra (Grid)',      time: 'O(V²)',   space: 'O(V)', stable: '—', desc: 'Shortest path on weighted grid.' },
      { id: 'bfs_grid',       name: 'BFS (Grid)',           time: 'O(V+E)',  space: 'O(V)', stable: '—', desc: 'Shortest path on unweighted grid.' },
      { id: 'dfs_maze',       name: 'DFS (Maze)',           time: 'O(V+E)',  space: 'O(V)', stable: '—', desc: 'Explores maze using depth-first approach.' },
      { id: 'greedy_best',    name: 'Greedy Best-First',    time: 'O(E)',    space: 'O(V)', stable: '—', desc: 'Always expands the node closest to the goal (by heuristic).' },
      { id: 'jump_point',     name: 'Jump Point Search',    time: 'O(E)',    space: 'O(V)', stable: '—', desc: 'Optimization of A* that skips intermediate nodes.' },
    ],
    dp: [
      { id: 'fibonacci',     name: 'Fibonacci DP',              time: 'O(n)',    space: 'O(n)',   stable: '—', desc: 'Compute Fibonacci using dynamic programming table.' },
      { id: 'knapsack',      name: 'Knapsack (0/1)',            time: 'O(n·W)', space: 'O(n·W)',  stable: '—', desc: 'Maximize value with weight constraint.' },
      { id: 'lcs',           name: 'Longest Common Subsequence', time: 'O(m·n)', space: 'O(m·n)', stable: '—', desc: 'Find longest subsequence present in both strings.' },
      { id: 'lis',           name: 'Longest Increasing Subseq', time: 'O(n²)',  space: 'O(n)',    stable: '—', desc: 'Find longest strictly increasing subsequence.' },
      { id: 'matrix_chain',  name: 'Matrix Chain Multiplication', time: 'O(n³)', space: 'O(n²)', stable: '—', desc: 'Find optimal way to multiply chain of matrices.' },
      { id: 'edit_distance', name: 'Edit Distance',             time: 'O(m·n)', space: 'O(m·n)',  stable: '—', desc: 'Minimum operations to transform one string to another.' },
      { id: 'coin_change',   name: 'Coin Change',               time: 'O(n·S)', space: 'O(S)',    stable: '—', desc: 'Minimum coins needed to make a given amount.' },
      { id: 'rod_cutting',   name: 'Rod Cutting',               time: 'O(n²)',  space: 'O(n)',    stable: '—', desc: 'Maximize revenue by cutting a rod into pieces.' },
      { id: 'palindromic_subseq', name: 'Longest Palindromic Subseq', time: 'O(n²)', space: 'O(n²)', stable: '—', desc: 'Find longest palindromic subsequence.' },
      { id: 'min_path_sum', name: 'Minimum Path Sum',       time: 'O(m·n)', space: 'O(m·n)', stable: '—', desc: 'Find path with minimum sum in a grid from top-left to bottom-right.' },
      { id: 'partition_subset', name: 'Partition Equal Subset Sum', time: 'O(n·S)', space: 'O(S)', stable: '—', desc: 'Determine if array can be partitioned into two equal-sum subsets.' },
      { id: 'tsp',         name: 'Traveling Salesman (DP)',  time: 'O(n²·2ⁿ)', space: 'O(n·2ⁿ)', stable: '—', desc: 'Find shortest tour visiting all cities using bitmask DP.' },
    ],
    backtracking: [
      { id: 'n_queens',     name: 'N-Queens',        time: 'O(n!)',    space: 'O(n²)', stable: '—', desc: 'Place N queens on an N×N board so none attack each other.' },
      { id: 'sudoku',       name: 'Sudoku Solver',   time: 'O(9^m)',   space: 'O(1)',  stable: '—', desc: 'Fill a 9×9 grid so each row/col/box has 1–9.' },
      { id: 'knights_tour', name: "Knight's Tour",   time: 'O(8^n²)', space: 'O(n²)', stable: '—', desc: 'Find path for knight to visit every square exactly once.' },
      { id: 'subset_sum',   name: 'Subset Sum',      time: 'O(2^n)',   space: 'O(n)',  stable: '—', desc: 'Find subset that sums to a target value.' },
      { id: 'permutations', name: 'Permutations',    time: 'O(n!)',    space: 'O(n)',  stable: '—', desc: 'Generate all permutations of a set.' },
      { id: 'combinations', name: 'Combinations',    time: 'O(C(n,k))', space: 'O(k)', stable: '—', desc: 'Generate all k-combinations of a set.' },
      { id: 'graph_coloring', name: 'Graph Coloring', time: 'O(m^V)', space: 'O(V)', stable: '—', desc: 'Color graph vertices so no two adjacent share a color.' },
      { id: 'rat_in_maze', name: 'Rat in a Maze',    time: 'O(2^n²)', space: 'O(n²)', stable: '—', desc: 'Find path from top-left to bottom-right in a maze.' },
      { id: 'word_search', name: 'Word Search',      time: 'O(n·m·4^L)', space: 'O(L)', stable: '—', desc: 'Find if a word exists in a 2D character board.' },
    ],
    string: [
      { id: 'kmp',           name: 'KMP Search',     time: 'O(n+m)',  space: 'O(m)',  stable: '—', desc: 'Pattern matching using prefix function.' },
      { id: 'rabin_karp',    name: 'Rabin-Karp',     time: 'O(n+m)',  space: 'O(1)',  stable: '—', desc: 'Pattern matching using rolling hash.' },
      { id: 'boyer_moore',   name: 'Boyer-Moore',    time: 'O(n/m)',  space: 'O(m)',  stable: '—', desc: 'Pattern matching using bad character and good suffix rules.' },
      { id: 'z_algorithm',   name: 'Z Algorithm',    time: 'O(n)',    space: 'O(n)',  stable: '—', desc: 'Computes Z-array for pattern matching.' },
      { id: 'longest_palindrome', name: 'Longest Palindrome', time: 'O(n²)', space: 'O(n)', stable: '—', desc: 'Find the longest palindromic substring.' },
      { id: 'suffix_array',  name: 'Suffix Array',   time: 'O(n log n)', space: 'O(n)', stable: '—', desc: 'Sorted array of all suffixes of a string.' },
      { id: 'manacher',     name: "Manacher's Algorithm", time: 'O(n)', space: 'O(n)', stable: '—', desc: 'Find all palindromic substrings in linear time.' },
      { id: 'aho_corasick', name: 'Aho-Corasick',   time: 'O(n+m+z)', space: 'O(m)', stable: '—', desc: 'Multi-pattern string matching using automaton.' },
      { id: 'suffix_tree',  name: 'Suffix Tree',     time: 'O(n)',    space: 'O(n)',  stable: '—', desc: 'Tree of all suffixes for fast pattern matching.' },
    ],
    math: [
      { id: 'gcd',          name: 'Euclidean GCD',   time: 'O(log min)', space: 'O(1)', stable: '—', desc: 'Greatest common divisor using Euclid\'s algorithm.' },
      { id: 'sieve',        name: 'Sieve of Eratosthenes', time: 'O(n log log n)', space: 'O(n)', stable: '—', desc: 'Find all primes up to n.' },
      { id: 'fast_pow',     name: 'Fast Exponentiation', time: 'O(log n)', space: 'O(1)', stable: '—', desc: 'Compute a^n in logarithmic time using binary exponentiation.' },
      { id: 'mod_inverse',  name: 'Modular Inverse', time: 'O(log m)', space: 'O(1)', stable: '—', desc: 'Find multiplicative inverse under modular arithmetic.' },
      { id: 'crt',          name: 'Chinese Remainder Theorem', time: 'O(n log n)', space: 'O(n)', stable: '—', desc: 'Solve system of simultaneous congruences.' },
      { id: 'prime_factor', name: 'Prime Factorization', time: 'O(√n)', space: 'O(log n)', stable: '—', desc: 'Decompose a number into prime factors.' },
      { id: 'extended_gcd', name: 'Extended Euclidean', time: 'O(log min)', space: 'O(log min)', stable: '—', desc: 'Find gcd and Bézout coefficients x, y such that ax + by = gcd.' },
      { id: 'euler_totient', name: "Euler's Totient φ(n)", time: 'O(√n)', space: 'O(1)', stable: '—', desc: 'Count integers 1..n that are coprime to n.' },
      { id: 'miller_rabin', name: 'Miller-Rabin Primality', time: 'O(k·log²n)', space: 'O(1)', stable: '—', desc: 'Probabilistic primality test with k rounds.' },
    ],
    datastructure: [
      { id: 'array_ops',     name: 'Array Operations',   time: 'O(n)', space: 'O(n)', stable: '—', desc: 'Insert, delete, rotate operations on arrays.' },
      { id: 'stack_ops',     name: 'Stack Operations',   time: 'O(1)', space: 'O(n)', stable: '—', desc: 'Push and pop operations on a stack.' },
      { id: 'queue_ops',     name: 'Queue Operations',   time: 'O(1)', space: 'O(n)', stable: '—', desc: 'Enqueue and dequeue operations on a queue.' },
      { id: 'heap_ops',      name: 'Heap Operations',    time: 'O(log n)', space: 'O(n)', stable: '—', desc: 'Insert and extract-min on a min-heap.' },
      { id: 'linkedlist_ops', name: 'Linked List Ops',   time: 'O(n)', space: 'O(n)', stable: '—', desc: 'Insert, delete, reverse, cycle detection.' },
      { id: 'hashtable_ops', name: 'Hash Table Ops',     time: 'O(1)', space: 'O(n)', stable: '—', desc: 'Chaining and open addressing with collision handling.' },
    ],
  };

  // ─── STATE ───
  let currentCategory = 'sorting';
  let currentAlgorithm = null;
  let isPlaying = false;
  let isPaused = false;
  let playbackTimer = null;

  // ─── ELEMENTS ───
  const $ = id => document.getElementById(id);
  const els = {
    navBtns:       document.querySelectorAll('.nav-btn'),
    algoList:      $('algo-list'),
    algoCount:     $('algo-count'),
    categoryTitle: $('category-title'),
    algoInfoName:  $('algo-info-name'),
    algoTime:      $('algo-time'),
    algoSpace:     $('algo-space'),
    algoStable:    $('algo-stable'),
    algoDesc:      $('algo-desc'),
    btnStart:      $('btn-start'),
    btnPause:      $('btn-pause'),
    btnStep:       $('btn-step'),
    btnReset:      $('btn-reset'),
    btnRandom:     $('btn-random'),
    btnCustom:     $('btn-custom'),
    speedSlider:   $('speed-slider'),
    speedValue:    $('speed-value'),
    sizeSlider:    $('size-slider'),
    sizeValue:     $('size-value'),
    stepFill:      $('step-fill'),
    stepCounter:   $('step-counter'),
    stepDesc:      $('step-description'),
    codeDisplay:   $('code-display'),
    logEntries:    $('log-entries'),
    legendItems:   $('legend-items'),
    panelTabs:     document.querySelectorAll('.panel-tab'),
    themeToggle:   $('theme-toggle'),
    infoBtn:       $('info-btn'),
    infoOverlay:   $('info-overlay'),
    infoClose:     $('info-close'),
    infoOk:        $('info-ok'),
    modalOverlay:  $('modal-overlay'),
    modalClose:    $('modal-close'),
    modalCancel:   $('modal-cancel'),
    modalApply:    $('modal-apply'),
    customArray:   $('custom-array'),
    customTarget:  $('custom-target'),
    canvas:        $('main-canvas'),
    gridContainer: $('grid-container'),
    dpContainer:   $('dp-table-container'),
  };

  // ─── VISUALIZER INSTANCES ───
  const canvasRenderer = new CanvasRenderer('main-canvas');
  const graphRenderer = new GraphRenderer('main-canvas');
  const gridRenderer = new GridRenderer('grid-container');
  const sortingViz = new SortingVisualizer(canvasRenderer);
  const graphViz = new GraphVisualizer(graphRenderer);
  const treeViz = new TreeVisualizer(canvasRenderer);
  const dpViz = new DPVisualizer();

  // ─── INIT UI CONTROLLERS ───
  SortingUI.init(sortingViz);
  GraphUI.init(graphViz, gridRenderer);
  TreeUI.init(treeViz, dpViz, canvasRenderer);

  // ─── HELPER: GET ACTIVE UI CONTROLLER ───
  function getController() {
    switch (currentCategory) {
      case 'sorting':
      case 'searching':
        return SortingUI;
      case 'graph':
      case 'pathfinding':
      case 'geometry':
        return GraphUI;
      default:
        return TreeUI;
    }
  }

  // ─── ALGORITHM GROUPS (for sidebar hierarchy) ───
  const GROUPS = {
    sorting: {
      'Simple':           ['bubble', 'selection', 'insertion', 'gnome'],
      'Divide & Conquer': ['merge', 'quick'],
      'Heap-based':       ['heap'],
      'Gap-based':        ['shell', 'comb', 'cocktail'],
      'Non-comparison':   ['counting', 'radix', 'bucket'],
      'Hybrid / Other':   ['tim', 'bitonic'],
    },
    graph: {
      'Traversal':        ['bfs', 'dfs'],
      'Shortest Path':    ['dijkstra', 'bellman_ford', 'floyd_warshall', 'a_star', 'johnson'],
      'Minimum Spanning': ['kruskal', 'prim', 'boruvka'],
      'Connectivity':     ['topological', 'kahns', 'kosaraju', 'tarjan', 'bridges', 'articulation', 'union_find'],
      'Cycle Detection':  ['cycle_directed', 'cycle_undirected'],
      'Network Flow':     ['ford_fulkerson', 'edmonds_karp', 'euler_path'],
    },
    tree: {
      'Traversal':        ['inorder', 'preorder', 'postorder', 'levelorder'],
      'Search Trees':     ['bst', 'avl', 'red_black'],
      'Advanced':         ['segment', 'fenwick', 'trie'],
      'Properties':       ['lca', 'height', 'diameter'],
    },
    dp: {
      'Classic':          ['fibonacci', 'knapsack', 'coin_change', 'rod_cutting'],
      'String DP':        ['lcs', 'lis', 'edit_distance', 'palindromic_subseq'],
      'Grid / Matrix':    ['min_path_sum', 'matrix_chain', 'partition_subset'],
      'Combinatorial':    ['tsp'],
    },
    backtracking: {
      'Board Problems':   ['n_queens', 'sudoku', 'knights_tour', 'rat_in_maze'],
      'Combinatorial':    ['subset_sum', 'permutations', 'combinations'],
      'Graph':            ['graph_coloring', 'word_search'],
    },
  };

  // ─── METRICS STATE ───
  let metrics = { comparisons: 0, swaps: 0, steps: 0 };

  function resetMetrics() {
    metrics = { comparisons: 0, swaps: 0, steps: 0 };
    _updateMetricsUI();
  }

  function _updateMetricsUI() {
    const mc = document.getElementById('metric-comparisons');
    const ms = document.getElementById('metric-swaps');
    const mt = document.getElementById('metric-steps');
    if (mc) mc.textContent = metrics.comparisons;
    if (ms) ms.textContent = metrics.swaps;
    if (mt) mt.textContent = metrics.steps;
  }

  // ─── CATEGORY SWITCHING ───
  function switchCategory(category) {
    currentCategory = category;
    currentAlgorithm = null;
    stopPlayback();
    resetMetrics();

    // Update nav
    els.navBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.category === category);
    });

    // Update sidebar
    const algos = REGISTRY[category] || [];
    els.categoryTitle.textContent = category.charAt(0).toUpperCase() + category.slice(1);
    els.algoCount.textContent = `${algos.length}`;

    // Clear search
    const searchInput = document.getElementById('algo-search-input');
    if (searchInput) searchInput.value = '';

    // Populate list with groups
    _populateAlgoList(algos, category);

    // Select first algorithm
    if (algos.length) {
      selectAlgorithm(algos[0]);
    }

    // Show/hide appropriate visualizer
    _setupVisualizerForCategory(category);
  }

  function _populateAlgoList(algos, category, filter = '') {
    els.algoList.innerHTML = '';
    const groups = GROUPS[category];
    const filterLower = filter.toLowerCase();

    if (groups && !filter) {
      // Grouped display
      let num = 0;
      for (const [groupName, ids] of Object.entries(groups)) {
        const groupAlgos = ids.map(id => algos.find(a => a.id === id)).filter(Boolean);
        if (!groupAlgos.length) continue;

        const header = document.createElement('div');
        header.className = 'algo-group-header';
        header.textContent = groupName;
        els.algoList.appendChild(header);

        groupAlgos.forEach(algo => {
          num++;
          els.algoList.appendChild(_createAlgoItem(algo, num));
        });
      }

      // Any ungrouped
      const groupedIds = new Set(Object.values(groups).flat());
      const ungrouped = algos.filter(a => !groupedIds.has(a.id));
      if (ungrouped.length) {
        ungrouped.forEach(algo => {
          num++;
          els.algoList.appendChild(_createAlgoItem(algo, num));
        });
      }
    } else {
      // Flat display (with optional filter)
      const filtered = filter
        ? algos.filter(a => a.name.toLowerCase().includes(filterLower) || a.id.includes(filterLower))
        : algos;
      filtered.forEach((algo, i) => {
        els.algoList.appendChild(_createAlgoItem(algo, i + 1));
      });
    }
  }

  function _createAlgoItem(algo, num) {
    const item = document.createElement('div');
    item.className = 'algo-item';
    item.dataset.id = algo.id;
    item.innerHTML = `
      <span class="algo-item-number">${String(num).padStart(2, '0')}</span>
      <span>${algo.name}</span>
    `;
    item.addEventListener('click', () => selectAlgorithm(algo));
    return item;
  }

  function _setupVisualizerForCategory(category) {
    // Reset all overlay containers
    els.gridContainer.style.display = 'none';
    els.dpContainer.style.display = 'none';
    els.canvas.style.display = 'block';

    const size = parseInt(els.sizeSlider.value);

    switch (category) {
      case 'sorting':
        sortingViz.setMode('sort');
        SortingUI.randomize(size);
        break;
      case 'searching':
        sortingViz.setMode('search');
        SortingUI.randomize(size);
        break;
      case 'graph':
        els.dpContainer.style.display = 'flex';
        GraphUI.randomizeGraph(Math.min(size, 12), 0.4, false);
        break;
      case 'pathfinding':
        els.canvas.style.display = 'none';
        GraphUI.randomizeGrid(20, 30, 0.25);
        break;
      case 'tree':
        TreeUI.randomTree(Math.min(size, 15));
        break;
      case 'dp':
        els.canvas.style.display = 'none';
        els.dpContainer.style.display = 'flex';
        _showDPPreview();
        break;
      case 'string':
        els.canvas.style.display = 'none';
        els.dpContainer.style.display = 'flex';
        _showStringPreview();
        break;
      case 'math':
        els.canvas.style.display = 'none';
        els.dpContainer.style.display = 'flex';
        _showMathPreview();
        break;
      case 'backtracking':
        els.canvas.style.display = 'none';
        els.dpContainer.style.display = 'flex';
        _showBoardPreview(currentAlgorithm);
        break;
      case 'datastructure':
        canvasRenderer.resize();
        _showDSPreview();
        break;
      case 'geometry':
        GraphUI.randomizeGraph(Math.min(size, 10), 0.0, false);
        break;
    }

    updateLegend(category);
  }

  // ─── LIVE PREVIEWS ───

  function _showDPPreview() {
    // Show a sample DP table preview
    dpViz.initTable(4, 6,
      ['0', '1', '2', '3'],
      ['', '0', '1', '2', '3', '4']
    );
    // Fill with sample fibonacci-like values
    const sample = [
      [0, 0, 1, 1, 2, 3],
      [0, 0, 0, 1, 1, 2],
      [0, 0, 0, 0, 1, 1],
      [0, 0, 0, 0, 0, 1],
    ];
    dpViz.applyStep({
      table: sample,
      current: [0, 4],
      highlighted: [[0, 3], [0, 2]],
      description: 'Press Run to start DP visualization',
    });
  }

  function _showStringPreview() {
    const text = 'ABABCABAB';
    dpViz.initTable(1, text.length, null, text.split(''));
    dpViz.applyStep({
      table: [text.split('').map(c => c.charCodeAt(0))],
      highlighted: [[0, 0], [0, 1], [0, 2]],
      description: 'Press Run to start pattern matching',
    });
  }

  function _showMathPreview() {
    dpViz.initTable(2, 3, ['Step', 'Result'], ['a', 'b', 'a mod b']);
    dpViz.applyStep({
      table: [[48, 18, 12], [18, 12, 6]],
      current: [0, 2],
      description: 'Press Run to start math visualization',
    });
  }

  function _showBoardPreview(algo) {
    const boardAlgos = ['n_queens', 'sudoku', 'knights_tour', 'rat_in_maze', 'word_search'];
    const algoId = algo ? algo.id : 'n_queens';

    if (boardAlgos.includes(algoId)) {
      const sz = algoId === 'sudoku' ? 9 : algoId === 'knights_tour' ? 5 : 4;
      dpViz.initBoard(sz);
      // Show a sample placement
      if (algoId === 'n_queens') {
        dpViz.applyBoardStep({
          board: [['♛','','',''],['','','♛',''],['','','',''],['','','','']],
          placed: [[0,0],[1,2]],
          current: [2,0],
          description: 'Press Run to solve N-Queens',
        });
      }
    } else {
      // Array-based backtracking (subset_sum, permutations, etc.)
      canvasRenderer.resize();
      els.canvas.style.display = 'block';
      els.dpContainer.style.display = 'none';
      const arr = [3, 4, 5, 2, 7, 1];
      _renderPreviewArray(arr, 'Press Run to start backtracking');
    }
  }

  function _showDSPreview() {
    const arr = [15, 10, 20, 8, 25, 5, 30];
    _renderPreviewArray(arr, 'Press Run to visualize data structure');
  }

  function _renderPreviewArray(arr, label) {
    requestAnimationFrame(() => {
      canvasRenderer.resize();
      const ctx = canvasRenderer.ctx;
      canvasRenderer.clear();
      const w = canvasRenderer.width;
      const h = canvasRenderer.height;
      if (!w || !h) return;
      const cellW = Math.min(60, (w - 80) / arr.length);
      const startX = (w - arr.length * cellW) / 2;
      const y = h / 2 - 25;

      arr.forEach((val, i) => {
        const x = startX + i * cellW;
        ctx.fillStyle = '#efefef';
        canvasRenderer.roundRect(x + 2, y, cellW - 4, 50, 5);
        ctx.fill();
        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.fillStyle = '#000';
        ctx.font = '600 14px JetBrains Mono, monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(String(val), x + cellW / 2, y + 25);
        ctx.fillStyle = '#bbb';
        ctx.font = '400 9px JetBrains Mono, monospace';
        ctx.fillText(String(i), x + cellW / 2, y + 62);
      });

      // Label
      ctx.fillStyle = '#999';
      ctx.font = '400 12px IBM Plex Sans, sans-serif';
      ctx.fillText(label, w / 2, y + 90);
    });
  }

  // ─── ALGORITHM SELECTION ───
  function selectAlgorithm(algo) {
    currentAlgorithm = algo;
    stopPlayback();
    resetMetrics();

    // ── Reset the visualization properly ──
    const controller = getController();
    controller.resetPlayback();

    // Re-init the visualizer for the current category so canvas is clean
    _setupVisualizerForCategory(currentCategory);

    // Update sidebar highlight
    document.querySelectorAll('.algo-item').forEach(item => {
      item.classList.toggle('active', item.dataset.id === algo.id);
    });

    // Update info panel
    els.algoInfoName.textContent = algo.name;
    els.algoTime.textContent = algo.time;
    els.algoSpace.textContent = algo.space;
    els.algoStable.textContent = algo.stable;
    els.algoDesc.textContent = algo.desc;

    // Update complexity in step bar
    const cb = document.getElementById('complexity-best');
    const ca = document.getElementById('complexity-avg');
    const cw = document.getElementById('complexity-worst');
    if (cb) cb.textContent = algo.time;
    if (ca) ca.textContent = algo.time;
    if (cw) cw.textContent = algo.time;

    // Update code panel with syntax-highlighted pseudocode
    const rawCode = _getPseudocode(algo.id, currentCategory);
    els.codeDisplay.innerHTML = _syntaxHighlight(rawCode);

    // Reset step bar
    updateStepBar(0, 0, 'Press Run to start visualization.');

    addLog(`Selected: ${algo.name}`, 'info');
  }

  /**
   * Syntax highlighting for pseudocode.
   * Applies line numbers + color classes for keywords, numbers, comments.
   */
  function _syntaxHighlight(code) {
    const lines = code.split('\n');
    return lines.map((line, i) => {
      // Escape HTML
      let hl = line
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      // Split out comment portion (← or //) so we don't highlight inside it
      let mainPart = hl;
      let commentPart = '';
      const arrowIdx = hl.indexOf('←');
      const slashIdx = hl.indexOf('//');
      const commentStart = arrowIdx >= 0 ? arrowIdx : (slashIdx >= 0 ? slashIdx : -1);
      if (commentStart >= 0) {
        mainPart = hl.substring(0, commentStart);
        commentPart = '<span class="syn-comment">' + hl.substring(commentStart) + '</span>';
      }

      // Apply highlighting to mainPart only
      mainPart = mainPart
        // Keywords
        .replace(/\b(function|for|while|if|else|return|break|continue|and|or|not|do|until|to|downto|in|each|true|false|null|then|swap|output|error)\b/g,
          '<span class="syn-keyword">$1</span>')
        // Numbers
        .replace(/\b(\d+)\b/g, '<span class="syn-number">$1</span>')
        // Function definitions
        .replace(/^(\s*)(function\s+)(\w+)/gm,
          '$1<span class="syn-keyword">function</span> <span class="syn-function">$3</span>')
        // Operators
        .replace(/(≠|≤|≥|==|!=|&lt;=|&gt;=|\+=|-=)/g,
          '<span class="syn-operator">$1</span>');

      const lineNum = String(i + 1).padStart(3, ' ');
      return '<span class="line-num">' + lineNum + '</span>' + mainPart + commentPart;
    }).join('\n');
  }

  // ─── PLAYBACK CONTROLS ───
  async function startPlayback() {
    if (!currentAlgorithm) return;
    if (isPaused) {
      resumePlayback();
      return;
    }

    stopPlayback();

    const controller = getController();
    const startBtn = els.btnStart;

    // Show loading state
    startBtn.innerHTML = '<div class="spinner"></div><span>Loading…</span>';
    startBtn.disabled = true;

    try {
      const target = currentCategory === 'searching'
        ? parseInt(els.customTarget.value) || null
        : null;

      await controller.loadSteps(currentCategory, currentAlgorithm.id, target);

      const total = controller.getProgress().total;
      if (total === 0) {
        addLog('No steps returned. Is the backend running? (python run.py)', 'compare');
        startBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg><span>Run</span>';
        startBtn.disabled = false;
        return;
      }
      addLog(`Loaded ${total} steps`, 'info');
    } catch (err) {
      addLog(`Error: ${err.message || err}. Start backend with: python run.py`, 'compare');
      startBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg><span>Run</span>';
      startBtn.disabled = false;
      return;
    }

    // Restore button
    startBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5,3 19,12 5,21"/></svg><span>Run</span>';
    startBtn.disabled = false;

    isPlaying = true;
    isPaused = false;
    els.btnPause.disabled = false;
    els.btnPause.querySelector('span').textContent = 'Pause';

    _playLoop();
  }

  function _playLoop() {
    if (!isPlaying || isPaused) return;

    const controller = getController();
    const hasMore = controller.nextStep();
    const progress = controller.getProgress();

    // Update step bar
    const step = controller.getCurrentStep?.() || {};
    updateStepBar(progress.current, progress.total, step.description || '');

    // Track metrics + log
    const currentStepData = controller.steps?.[progress.current - 1];
    if (currentStepData) {
      metrics.steps = progress.current;
      if (currentStepData.compare) metrics.comparisons++;
      if (currentStepData.swap) metrics.swaps++;
      _updateMetricsUI();
      _logStep(currentStepData);
    }

    if (hasMore) {
      const delay = Helpers.speedToDelay(parseInt(els.speedSlider.value));
      playbackTimer = setTimeout(_playLoop, delay);
    } else {
      stopPlayback();
      addLog('Completed!', 'sorted');
      updateStepBar(progress.total, progress.total, 'Algorithm complete!');
    }
  }

  function pausePlayback() {
    isPaused = true;
    isPlaying = false;
    clearTimeout(playbackTimer);
    els.btnPause.querySelector('span').textContent = 'Resume';
    addLog('Paused', 'info');
  }

  function resumePlayback() {
    isPaused = false;
    isPlaying = true;
    els.btnPause.querySelector('span').textContent = 'Pause';
    _playLoop();
    addLog('Resumed', 'info');
  }

  function stopPlayback() {
    isPlaying = false;
    isPaused = false;
    clearTimeout(playbackTimer);
    els.btnPause.disabled = true;
    els.btnPause.querySelector('span').textContent = 'Pause';
  }

  function stepForward() {
    if (!currentAlgorithm) return;

    const controller = getController();
    if (controller.getProgress().total === 0) {
      // Need to load steps first
      startPlayback().then(() => {
        stopPlayback();
      });
      return;
    }

    stopPlayback();
    const hasMore = controller.nextStep();
    const progress = controller.getProgress();
    const step = controller.getCurrentStep?.() || {};
    updateStepBar(progress.current, progress.total, step.description || '');
  }

  function resetVisualization() {
    stopPlayback();
    const controller = getController();
    controller.resetPlayback();
    _setupVisualizerForCategory(currentCategory);
    updateStepBar(0, 0, 'Reset. Press Run to start.');
    addLog('Reset', 'info');
  }

  function randomizeData() {
    stopPlayback();
    const size = parseInt(els.sizeSlider.value);
    _setupVisualizerForCategory(currentCategory);
    updateStepBar(0, 0, 'New random data generated. Press Run.');
    addLog('Randomized data', 'info');
  }

  // ─── UI UPDATES ───
  function updateStepBar(current, total, desc) {
    const pct = total > 0 ? (current / total) * 100 : 0;
    els.stepFill.style.width = pct + '%';
    els.stepCounter.textContent = `Step ${current} / ${total}`;
    els.stepDesc.textContent = desc;

    // ── Pseudocode line highlighting ──
    if (currentAlgorithm) {
      _highlightPseudocodeLine(desc);
    }
  }

  /**
   * Highlight the pseudocode line that matches the current step action.
   * Uses keyword matching from the step description.
   */
  function _highlightPseudocodeLine(description) {
    const codeEl = els.codeDisplay;
    if (!codeEl || !description || !currentAlgorithm) return;

    const code = _getPseudocode(currentAlgorithm.id, currentCategory);
    const lines = code.split('\n');

    // Find the best matching line based on step description
    const desc = description.toLowerCase();
    let bestLine = -1;
    let bestScore = 0;

    const actionKeywords = {
      'swap': ['swap'],
      'compare': ['compare', 'if arr', 'if a['],
      'merge': ['merge'],
      'split': ['split', 'divide', 'mid ='],
      'pivot': ['pivot', 'partition'],
      'insert': ['insert', 'place', 'arr[j+1]'],
      'shift': ['shift', 'arr[j]'],
      'visit': ['visit', 'process', 'visited'],
      'relax': ['relax', 'dist[v]', 'dist['],
      'enqueue': ['enqueue', 'queue'],
      'dequeue': ['dequeue', 'queue.pop', 'queue.de'],
      'push': ['push', 'stack.push'],
      'pop': ['pop', 'stack.pop'],
      'found': ['found', 'return', 'solution'],
      'backtrack': ['backtrack', 'board[', '= 0', 'undo'],
      'rotate': ['rotate'],
      'sift': ['sift', 'heapify'],
      'hash': ['hash', 'bucket'],
      'match': ['match', 'pattern', 'text['],
      'digit': ['digit', 'exp'],
      'fill': ['dp[', 'table', 'fill'],
    };

    for (const [action, keywords] of Object.entries(actionKeywords)) {
      if (keywords.some(kw => desc.includes(kw))) {
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i].toLowerCase();
          let score = 0;
          for (const kw of keywords) {
            if (line.includes(kw)) score += 2;
          }
          if (line.includes('←') || line.includes('→')) score += 1;
          if (score > bestScore) {
            bestScore = score;
            bestLine = i;
          }
        }
        break;
      }
    }

    // Re-render with syntax highlighting + active line highlight
    const highlighted = _syntaxHighlight(code);
    if (bestLine >= 0) {
      const hlLines = highlighted.split('\n');
      if (hlLines[bestLine]) {
        hlLines[bestLine] = '<span class="line-highlight">' + hlLines[bestLine] + '</span>';
      }
      codeEl.innerHTML = hlLines.join('\n');
    } else {
      codeEl.innerHTML = highlighted;
    }
  }

  function addLog(message, type = 'info') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    els.logEntries.prepend(entry);

    // Keep max 100 entries
    while (els.logEntries.children.length > 100) {
      els.logEntries.removeChild(els.logEntries.lastChild);
    }
  }

  function _logStep(step) {
    if (step.swap) {
      addLog(`Swap: indices ${step.swap.join(', ')}`, 'swap');
    } else if (step.compare) {
      addLog(`Compare: indices ${step.compare.join(', ')}`, 'compare');
    } else if (step.current != null) {
      addLog(`Current: ${step.current}`, 'visit');
    }
  }

  function updateLegend(category) {
    const legends = {
      sorting: [
        { color: '--color-default',  label: 'Unsorted' },
        { color: '--color-compare',  label: 'Comparing' },
        { color: '--color-swap',     label: 'Swapping' },
        { color: '--color-sorted',   label: 'Sorted' },
        { color: '--color-active',   label: 'Active / Pivot' },
      ],
      searching: [
        { color: '--color-default',  label: 'Unchecked' },
        { color: '--color-current',  label: 'Current Probe' },
        { color: '--color-sorted',   label: 'Already Checked' },
        { color: '--color-found',    label: 'Found!' },
        { color: '--color-active',   label: 'Search Range [ ]' },
        { color: '--bg-surface-3',   label: 'Eliminated' },
      ],
      graph: [
        { color: '--color-default',  label: 'Unvisited' },
        { color: '--color-active',   label: 'In Queue / Frontier' },
        { color: '--color-current',  label: 'Current Node' },
        { color: '--color-visited',  label: 'Visited' },
        { color: '--color-path',     label: 'Shortest Path' },
        { color: '--color-found',    label: 'MST Edge' },
      ],
      pathfinding: [
        { color: '--color-start',    label: 'Start' },
        { color: '--color-end',      label: 'End' },
        { color: '--color-wall',     label: 'Wall' },
        { color: '--color-visited',  label: 'Visited' },
        { color: '--color-compare',  label: 'Frontier' },
        { color: '--color-current',  label: 'Current' },
        { color: '--color-path',     label: 'Path' },
      ],
      tree: [
        { color: '--color-default',  label: 'Node' },
        { color: '--color-current',  label: 'Current' },
        { color: '--color-visited',  label: 'Visited' },
        { color: '--color-found',    label: 'Inserted' },
        { color: '--color-swap',     label: 'Deleted' },
        { color: '--color-compare',  label: 'Rotating' },
      ],
      dp: [
        { color: '--bg-surface-3',   label: 'Empty Cell' },
        { color: '--color-current',  label: 'Computing' },
        { color: '--color-active',   label: 'Referenced' },
        { color: '--color-sorted',   label: 'Filled' },
      ],
      backtracking: [
        { color: '--color-current',  label: 'Trying' },
        { color: '--color-sorted',   label: 'Placed' },
        { color: '--color-swap',     label: 'Conflict / Backtrack' },
      ],
      geometry: [
        { color: '--color-default',  label: 'Point' },
        { color: '--color-active',   label: 'Active Edge' },
        { color: '--color-path',     label: 'Hull / Result' },
        { color: '--color-current',  label: 'Current' },
        { color: '--color-swap',     label: 'Intersection' },
      ],
    };

    const items = legends[category] || legends.sorting;
    els.legendItems.innerHTML = items.map(item => `
      <div class="legend-item">
        <div class="legend-swatch" style="background: var(${item.color})"></div>
        <span>${item.label}</span>
      </div>
    `).join('');
  }

  // ─── PSEUDOCODE (comprehensive for all algorithms) ───
  function _getPseudocode(algoId, category) {
    const codes = {
      // ══════ SORTING ══════
      bubble: `function bubbleSort(arr):
  for i = 0 to n-1:
    for j = 0 to n-i-2:
      if arr[j] > arr[j+1]:       ← compare
        swap(arr[j], arr[j+1])    ← swap`,

      selection: `function selectionSort(arr):
  for i = 0 to n-1:
    minIdx = i
    for j = i+1 to n-1:
      if arr[j] < arr[minIdx]:
        minIdx = j                ← find min
    swap(arr[i], arr[minIdx])     ← place min`,

      insertion: `function insertionSort(arr):
  for i = 1 to n-1:
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
      arr[j+1] = arr[j]          ← shift right
      j = j - 1
    arr[j+1] = key                ← insert key`,

      merge: `function mergeSort(arr, lo, hi):
  if lo >= hi: return
  mid = (lo + hi) / 2
  mergeSort(arr, lo, mid)         ← sort left half
  mergeSort(arr, mid+1, hi)       ← sort right half
  merge(arr, lo, mid, hi)         ← merge sorted halves`,

      quick: `function quickSort(arr, lo, hi):
  if lo >= hi: return
  p = partition(arr, lo, hi)
  quickSort(arr, lo, p-1)
  quickSort(arr, p+1, hi)

function partition(arr, lo, hi):
  pivot = arr[hi]
  i = lo
  for j = lo to hi-1:
    if arr[j] <= pivot:
      swap(arr[i], arr[j])
      i++
  swap(arr[i], arr[hi])           ← place pivot
  return i`,

      heap: `function heapSort(arr):
  buildMaxHeap(arr)
  for i = n-1 downto 1:
    swap(arr[0], arr[i])          ← extract max
    heapify(arr, 0, i)

function heapify(arr, i, n):
  largest = i
  l = 2*i+1, r = 2*i+2
  if l < n and arr[l] > arr[largest]:
    largest = l
  if r < n and arr[r] > arr[largest]:
    largest = r
  if largest ≠ i:
    swap(arr[i], arr[largest])
    heapify(arr, largest, n)`,

      shell: `function shellSort(arr):
  gap = n / 2
  while gap > 0:
    for i = gap to n-1:
      temp = arr[i], j = i
      while j >= gap and arr[j-gap] > temp:
        arr[j] = arr[j-gap]       ← shift by gap
        j -= gap
      arr[j] = temp
    gap /= 2`,

      counting: `function countingSort(arr):
  count = array of zeros [0..max]
  for each element x in arr:
    count[x]++                    ← count occurrences
  idx = 0
  for val = 0 to max:
    while count[val] > 0:
      arr[idx++] = val            ← place in order
      count[val]--`,

      radix: `function radixSort(arr):
  for each digit position (1s, 10s, 100s...):
    countingSortByDigit(arr, exp)  ← sort by digit
    exp *= 10`,

      bucket: `function bucketSort(arr):
  create n empty buckets
  for each element:
    insert into bucket[f(element)]  ← distribute
  sort each bucket
  concatenate all buckets           ← gather`,

      tim: `function timSort(arr):
  minRun = 32
  for each run of size minRun:
    insertionSort(run)              ← sort small runs
  size = minRun
  while size < n:
    merge adjacent runs of 'size'   ← merge passes
    size *= 2`,

      cocktail: `function cocktailSort(arr):
  while swapped:
    // Forward pass (like bubble)
    for i = start to end-1:
      if arr[i] > arr[i+1]: swap   ← left to right
    end--
    // Backward pass
    for i = end downto start+1:
      if arr[i-1] > arr[i]: swap   ← right to left
    start++`,

      comb: `function combSort(arr):
  gap = n, shrink = 1.3
  while gap > 1 or swapped:
    gap = max(1, gap / shrink)
    for i = 0 to n-gap-1:
      if arr[i] > arr[i+gap]:
        swap(arr[i], arr[i+gap])    ← compare with gap`,

      gnome: `function gnomeSort(arr):
  i = 0
  while i < n:
    if i == 0 or arr[i] >= arr[i-1]:
      i++                           ← step forward
    else:
      swap(arr[i], arr[i-1])
      i--                           ← step backward`,

      bitonic: `function bitonicSort(arr, lo, cnt, dir):
  if cnt > 1:
    k = cnt / 2
    bitonicSort(arr, lo, k, ASC)
    bitonicSort(arr, lo+k, k, DESC)
    bitonicMerge(arr, lo, cnt, dir)

function bitonicMerge(arr, lo, cnt, dir):
  if cnt > 1:
    k = cnt / 2
    for i = lo to lo+k-1:
      if (arr[i] > arr[i+k]) == dir:
        swap(arr[i], arr[i+k])`,

      // ══════ SEARCHING ══════
      linear: `function linearSearch(arr, target):
  for i = 0 to n-1:
    if arr[i] == target:
      return i                      ← found!
  return -1                         ← not found`,

      binary: `function binarySearch(arr, target):
  lo = 0, hi = n-1
  while lo <= hi:
    mid = (lo + hi) / 2
    if arr[mid] == target:
      return mid                    ← found!
    else if arr[mid] < target:
      lo = mid + 1                  ← search right
    else:
      hi = mid - 1                  ← search left
  return -1`,

      jump: `function jumpSearch(arr, target):
  step = √n
  prev = 0
  while arr[min(step,n)-1] < target:
    prev = step
    step += √n                      ← jump forward
  for i = prev to min(step, n):
    if arr[i] == target:
      return i                      ← linear scan`,

      interpolation: `function interpolationSearch(arr, target):
  lo = 0, hi = n-1
  while lo <= hi and target in range:
    // Estimate position
    pos = lo + (target - arr[lo]) *
          (hi - lo) / (arr[hi] - arr[lo])
    if arr[pos] == target: return pos
    else if arr[pos] < target: lo = pos+1
    else: hi = pos-1`,

      exponential: `function exponentialSearch(arr, target):
  bound = 1
  while bound < n and arr[bound] <= target:
    bound *= 2                      ← double the bound
  // Binary search in [bound/2, min(bound, n)]
  return binarySearch(arr, bound/2,
                      min(bound, n), target)`,

      fibonacci: `function fibonacciSearch(arr, target):
  find smallest Fib ≥ n
  while fib > 1:
    i = min(offset + fib2, n-1)
    if arr[i] < target:
      fib = fib1, offset = i        ← move right
    else if arr[i] > target:
      fib = fib2                    ← move left
    else: return i                  ← found!`,

      ternary: `function ternarySearch(arr, target):
  lo = 0, hi = n-1
  while lo <= hi:
    mid1 = lo + (hi-lo)/3
    mid2 = hi - (hi-lo)/3
    if arr[mid1] == target: return mid1
    if arr[mid2] == target: return mid2
    if target < arr[mid1]: hi = mid1-1
    else if target > arr[mid2]: lo = mid2+1
    else: lo = mid1+1, hi = mid2-1`,

      // ══════ GRAPH ══════
      bfs: `function BFS(graph, start):
  queue = [start]
  visited = {start}
  while queue not empty:
    node = queue.dequeue()          ← process
    for neighbor in adj(node):
      if neighbor not visited:
        visited.add(neighbor)
        queue.enqueue(neighbor)     ← discover`,

      dfs: `function DFS(graph, node):
  visited.add(node)                 ← visit
  for neighbor in adj(node):
    if neighbor not visited:
      DFS(graph, neighbor)          ← recurse`,

      dijkstra: `function Dijkstra(graph, source):
  dist[source] = 0, all others = ∞
  pq = MinHeap with (0, source)
  while pq not empty:
    (d, u) = pq.extractMin()
    for (v, w) in adj(u):
      if d + w < dist[v]:
        dist[v] = d + w             ← relax edge
        pq.insert(dist[v], v)`,

      bellman_ford: `function BellmanFord(graph, source):
  dist[source] = 0, all others = ∞
  for i = 1 to V-1:
    for each edge (u, v, w):
      if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w       ← relax
  // Check for negative cycles
  for each edge (u, v, w):
    if dist[u] + w < dist[v]:
      error "Negative cycle!"`,

      floyd_warshall: `function FloydWarshall(graph):
  dist[][] = adjacency matrix
  for k = 0 to V-1:
    for i = 0 to V-1:
      for j = 0 to V-1:
        if dist[i][k] + dist[k][j] < dist[i][j]:
          dist[i][j] = dist[i][k] + dist[k][j]
          // Route through k is shorter`,

      a_star: `function AStar(graph, start, goal):
  openSet = {start}
  g[start] = 0
  f[start] = h(start, goal)        ← heuristic
  while openSet not empty:
    u = node with lowest f
    if u == goal: reconstruct path
    for v in adj(u):
      tentative = g[u] + w(u,v)
      if tentative < g[v]:
        g[v] = tentative
        f[v] = g[v] + h(v, goal)    ← f = g + h`,

      kruskal: `function Kruskal(graph):
  sort edges by weight
  MST = {}
  for each edge (u, v, w) in order:
    if find(u) ≠ find(v):           ← different sets?
      MST.add(u, v, w)
      union(u, v)                   ← merge sets`,

      prim: `function Prim(graph, start):
  visited = {start}
  pq = edges from start
  while pq not empty:
    (w, u, v) = pq.extractMin()
    if v not visited:
      visited.add(v)
      MST.add(u, v, w)              ← add to MST
      add edges from v to pq`,

      boruvka: `function Boruvka(graph):
  each node is a component
  while components > 1:
    for each component:
      find cheapest outgoing edge    ← lightest bridge
    add all cheapest edges to MST
    merge connected components`,

      topological: `function TopologicalSort(graph):
  compute in-degree for all nodes
  queue = nodes with in-degree 0
  while queue not empty:
    u = queue.dequeue()
    output u                         ← append to order
    for v in adj(u):
      in-degree[v]--
      if in-degree[v] == 0:
        queue.enqueue(v)`,

      kosaraju: `function Kosaraju(graph):
  // Pass 1: DFS and record finish order
  for each unvisited node:
    DFS(node), push to stack on finish
  // Build reverse graph
  // Pass 2: DFS on reverse in stack order
  while stack not empty:
    node = stack.pop()
    if not visited: DFS(reverse, node)
    → each DFS tree = one SCC`,

      tarjan: `function Tarjan(graph):
  for each unvisited node v:
    index[v] = lowlink[v] = counter++
    push v to stack
    for w in adj(v):
      if w not visited:
        Tarjan(w)
        lowlink[v] = min(lowlink[v], lowlink[w])
      else if w on stack:
        lowlink[v] = min(lowlink[v], index[w])
    if lowlink[v] == index[v]:
      pop stack until v → SCC found`,

      bridges: `function FindBridges(graph):
  DFS with discovery time disc[]
  and low-link value low[]
  for each edge (u, v):
    if low[v] > disc[u]:
      (u, v) is a bridge            ← removing it
      // disconnects the graph`,

      articulation: `function ArticulationPoints(graph):
  DFS with disc[] and low[]
  node u is an articulation point if:
    1. u is root and has ≥ 2 children
    2. u is not root and has child v
       where low[v] >= disc[u]`,

      euler_path: `function EulerPath(graph): // Hierholzer's
  start from odd-degree vertex (or any)
  stack = [start]
  path = []
  while stack not empty:
    v = stack.top()
    if v has unused edge (v, u):
      remove edge (v, u)
      stack.push(u)                  ← traverse
    else:
      stack.pop()
      path.prepend(v)                ← add to circuit`,

      ford_fulkerson: `function FordFulkerson(graph, s, t):
  maxFlow = 0
  while exists augmenting path P from s to t:
    bottleneck = min capacity along P
    for each edge (u,v) in P:
      capacity[u][v] -= bottleneck   ← forward
      capacity[v][u] += bottleneck   ← backward
    maxFlow += bottleneck`,

      edmonds_karp: `function EdmondsKarp(graph, s, t):
  // Ford-Fulkerson with BFS
  while BFS finds path s → t:
    bottleneck = min capacity on path
    update residual capacities
    maxFlow += bottleneck
  // BFS guarantees O(VE²)`,

      union_find: `function UnionFind:
  parent[i] = i for all nodes

function find(x):
  if parent[x] ≠ x:
    parent[x] = find(parent[x])     ← path compression
  return parent[x]

function union(x, y):
  rx = find(x), ry = find(y)
  if rank[rx] >= rank[ry]:
    parent[ry] = rx                  ← union by rank
  else: parent[rx] = ry`,

      kahns: `function KahnsTopSort(graph):
  compute in_degree[] for all nodes
  queue = {nodes with in_degree 0}
  while queue not empty:
    u = queue.dequeue()
    result.add(u)
    for v in adj(u):
      in_degree[v]--
      if in_degree[v] == 0:
        queue.add(v)                 ← ready to process`,

      cycle_directed: `function hasCycleDirected(graph):
  color each node WHITE
  for each WHITE node u:
    DFS(u):
      color u = GRAY                ← in progress
      for v in adj(u):
        if color[v] == GRAY:
          → CYCLE! (back edge)      ← found cycle
      color u = BLACK               ← done`,

      cycle_undirected: `function hasCycleUndirected(graph):
  for each unvisited node u:
    DFS(u, parent=-1):
      visited.add(u)
      for v in adj(u):
        if v not visited:
          DFS(v, parent=u)
        else if v ≠ parent:
          → CYCLE! (back edge)`,

      johnson: `function Johnson(graph):
  // 1. Add virtual node q → all with weight 0
  // 2. Bellman-Ford from q → get h[] values
  // 3. Reweight: w'(u,v) = w(u,v) + h[u] - h[v]
  // 4. Run Dijkstra from each vertex
  // 5. Restore: dist[u][v] = d'[u][v] - h[u] + h[v]`,
      johnsons: `(same as Johnson's Algorithm above)`,

      convex_hull_graham: `function GrahamScan(points):
  find lowest point as pivot
  sort by polar angle from pivot
  stack = [p0, p1]
  for i = 2 to n-1:
    while cross(stack[-2], stack[-1], p[i]) ≤ 0:
      stack.pop()                   ← not left turn
    stack.push(p[i])                ← add to hull`,

      convex_hull_jarvis: `function JarvisMarch(points):
  start from leftmost point
  current = start
  do:
    hull.add(current)
    next = points[0]
    for each point p:
      if cross(current, next, p) < 0:
        next = p                    ← more counter-clockwise
    current = next
  until current == start`,

      closest_pair: `function ClosestPair(points):
  sort by x-coordinate
  divide points at median x
  d_left = ClosestPair(left half)
  d_right = ClosestPair(right half)
  d = min(d_left, d_right)
  // Check strip of width 2d around median
  for points in strip (sorted by y):
    check only next 7 points        ← O(n) strip check`,

      line_intersection: `function lineSegmentIntersection(segments):
  for i = 0 to n-1:
    for j = i+1 to n-1:
      A, B = segments[i]
      C, D = segments[j]
      if ccw(A,C,D) ≠ ccw(B,C,D) and
         ccw(A,B,C) ≠ ccw(A,B,D):
        report intersection (i, j)   ← segments cross

function ccw(A, B, C):
  return (C.y-A.y)(B.x-A.x) > (B.y-A.y)(C.x-A.x)`,

      sweep_line: `function SweepLine(segments):
  events = []
  for each segment:
    add (left_x, START, seg_id)
    add (right_x, END, seg_id)
  sort events by x
  active = {}
  for each event:
    if START:
      check seg vs all active segs   ← test intersections
      active.add(seg)
    if END:
      active.remove(seg)`,

      // ══════ PATHFINDING ══════
      a_star_grid: `function AStarGrid(grid, start, end):
  openSet = MinHeap with start
  g[start] = 0
  f[start] = heuristic(start, end)
  while openSet not empty:
    current = extractMin(openSet)
    if current == end: trace path
    for each neighbor (up/down/left/right):
      if not wall and not visited:
        newG = g[current] + 1
        if newG < g[neighbor]:
          update g, f, parent`,

      dijkstra_grid: `(same as Dijkstra, on grid cells)
  each cell is a node
  neighbors are 4-directional
  weight = 1 for uniform grid`,

      bfs_grid: `function BFSGrid(grid, start, end):
  queue = [start], visited = {start}
  while queue not empty:
    (r,c) = queue.dequeue()
    if (r,c) == end: trace path
    for (nr,nc) in neighbors(r,c):
      if not wall and not visited:
        visited.add(nr,nc)
        parent[nr,nc] = (r,c)
        queue.enqueue(nr,nc)`,

      dfs_maze: `function DFSMaze(grid, start, end):
  visited = {}
  function explore(r, c):
    visited.add(r, c)
    if (r,c) == end: return true
    for (nr,nc) in neighbors(r,c):
      if valid and not visited:
        if explore(nr,nc): return true
    return false                    ← backtrack`,

      greedy_best: `function GreedyBestFirst(grid, start, end):
  openSet = MinHeap by h(node, end)
  while openSet not empty:
    current = extractMin()
    if current == end: done
    for neighbor in adj(current):
      if not visited:
        add to openSet with h(neighbor, end)
  // Note: NOT guaranteed shortest path`,

      jump_point: `function JumpPointSearch(grid, start, end):
  // Optimization of A* for uniform grids
  // Only expand "jump points" — forced neighbors
  for each direction (dr, dc):
    jump(r, c, dr, dc):
      if blocked: return null
      if at goal: return (nr, nc)
      if has forced neighbor: return (nr, nc)
      // For diagonal: recursively check cardinal
      return jump(nr, nc, dr, dc)`,

      // ══════ TREE ══════
      inorder: `function inorder(node):
  if node == null: return
  inorder(node.left)                ← visit left
  process(node)                     ← visit root
  inorder(node.right)               ← visit right
  // Result: sorted order for BST`,

      preorder: `function preorder(node):
  if node == null: return
  process(node)                     ← visit root first
  preorder(node.left)               ← then left
  preorder(node.right)              ← then right`,

      postorder: `function postorder(node):
  if node == null: return
  postorder(node.left)              ← visit left first
  postorder(node.right)             ← then right
  process(node)                     ← root last`,

      levelorder: `function levelOrder(root):
  queue = [root]
  while queue not empty:
    node = queue.dequeue()
    process(node)                   ← visit level by level
    if node.left: queue.enqueue(node.left)
    if node.right: queue.enqueue(node.right)`,

      bst: `function BSTInsert(root, val):
  if root == null: return new Node(val)
  if val < root.val:
    root.left = insert(root.left, val)
  else if val > root.val:
    root.right = insert(root.right, val)
  return root`,

      avl: `function AVLInsert(node, val):
  // Standard BST insert
  node = BSTInsert(node, val)
  // Update height & balance factor
  bf = height(left) - height(right)
  // Rebalance if |bf| > 1:
  if bf > 1:  rotateRight or LR
  if bf < -1: rotateLeft or RL`,

      red_black: `Red-Black Tree Rules:
  1. Every node is red or black
  2. Root is black
  3. Leaves (NIL) are black
  4. Red node → children are black
  5. All paths: same # black nodes

Insert: add as red, then fix-up:
  - Uncle red → recolor
  - Uncle black → rotate + recolor`,

      segment: `function buildSegTree(arr, node, start, end):
  if start == end:
    tree[node] = arr[start]         ← leaf
  else:
    mid = (start + end) / 2
    build(left child, start, mid)
    build(right child, mid+1, end)
    tree[node] = tree[left] + tree[right]

function query(node, start, end, l, r):
  if [start,end] ⊆ [l,r]: return tree[node]
  if disjoint: return 0
  return query(left) + query(right)`,

      fenwick: `Fenwick Tree (BIT):
function update(i, delta):
  while i <= n:
    bit[i] += delta
    i += i & (-i)                   ← add LSB

function prefixSum(i):
  sum = 0
  while i > 0:
    sum += bit[i]
    i -= i & (-i)                   ← remove LSB
  return sum`,

      trie: `Trie:
function insert(word):
  node = root
  for char in word:
    if char not in node.children:
      node.children[char] = new Node
    node = node.children[char]
  node.isEnd = true

function search(word):
  node = root
  for char in word:
    if char not in node.children:
      return false
    node = node.children[char]
  return node.isEnd`,

      lca: `function LCA(root, a, b):  // BST
  node = root
  while node:
    if a < node.val and b < node.val:
      node = node.left               ← both left
    else if a > node.val and b > node.val:
      node = node.right              ← both right
    else:
      return node                    ← split point = LCA`,

      height: `function treeHeight(node):
  if node == null: return 0
  leftH  = treeHeight(node.left)
  rightH = treeHeight(node.right)
  return 1 + max(leftH, rightH)`,

      diameter: `function treeDiameter(node):
  if node == null: return 0
  lH = height(node.left)
  rH = height(node.right)
  // Diameter through this node
  diam = lH + rH
  maxDiam = max(maxDiam, diam)
  return 1 + max(lH, rH)`,

      // ══════ DYNAMIC PROGRAMMING ══════
      fibonacci: `function fibDP(n):
  dp[0] = 0, dp[1] = 1
  for i = 2 to n:
    dp[i] = dp[i-1] + dp[i-2]       ← add previous two
  return dp[n]`,

      knapsack: `function knapsack01(W, wt[], val[], n):
  for i = 1 to n:
    for w = 1 to W:
      if wt[i-1] <= w:
        dp[i][w] = max(
          dp[i-1][w],                ← skip item
          val[i-1] + dp[i-1][w-wt[i-1]]  ← take item
        )
      else: dp[i][w] = dp[i-1][w]`,

      lcs: `function LCS(X, Y):
  for i = 1 to m:
    for j = 1 to n:
      if X[i] == Y[j]:
        dp[i][j] = dp[i-1][j-1] + 1  ← match!
      else:
        dp[i][j] = max(dp[i-1][j],
                       dp[i][j-1])    ← skip one`,

      lis: `function LIS(arr):
  dp[i] = 1 for all i
  for i = 1 to n-1:
    for j = 0 to i-1:
      if arr[j] < arr[i]:
        dp[i] = max(dp[i], dp[j]+1)  ← extend
  return max(dp[])`,

      coin_change: `function coinChange(coins, amount):
  dp[0] = 0, dp[1..amount] = ∞
  for i = 1 to amount:
    for each coin c:
      if c <= i and dp[i-c]+1 < dp[i]:
        dp[i] = dp[i-c] + 1          ← use coin c`,

      edit_distance: `function editDistance(s1, s2):
  dp[i][0] = i, dp[0][j] = j
  for i = 1 to m:
    for j = 1 to n:
      if s1[i] == s2[j]:
        dp[i][j] = dp[i-1][j-1]      ← match
      else:
        dp[i][j] = 1 + min(
          dp[i-1][j],                ← delete
          dp[i][j-1],                ← insert
          dp[i-1][j-1]               ← replace
        )`,

      rod_cutting: `function rodCutting(prices, n):
  dp[0] = 0
  for i = 1 to n:
    for j = 1 to i:
      dp[i] = max(dp[i],
        prices[j] + dp[i-j])         ← cut at length j`,

      matrix_chain: `function matrixChain(dims):
  for len = 2 to n:
    for i = 0 to n-len:
      j = i + len - 1
      dp[i][j] = ∞
      for k = i to j-1:
        cost = dp[i][k] + dp[k+1][j]
             + dims[i]*dims[k+1]*dims[j+1]
        dp[i][j] = min(dp[i][j], cost)`,

      palindromic_subseq: `function longestPalSubseq(s):
  dp[i][i] = 1
  for len = 2 to n:
    for i = 0 to n-len:
      j = i + len - 1
      if s[i] == s[j]:
        dp[i][j] = dp[i+1][j-1] + 2  ← extend
      else:
        dp[i][j] = max(dp[i+1][j],
                       dp[i][j-1])`,

      min_path_sum: `function minPathSum(grid):
  dp[0][0] = grid[0][0]
  // Fill first row and column
  for i,j starting from (1,1):
    dp[i][j] = grid[i][j] +
      min(dp[i-1][j], dp[i][j-1])    ← from top or left`,

      partition_subset: `function canPartition(nums):
  target = sum(nums) / 2
  dp[0] = true
  for each num:
    for j = target downto num:
      dp[j] = dp[j] || dp[j-num]     ← include or skip`,

      tsp: `function TSP_DP(dist):
  // Bitmask DP: dp[mask][i]
  dp[1][0] = 0  // start at city 0
  for each mask (subset of cities):
    for each city u in mask:
      for each city v not in mask:
        newMask = mask | (1 << v)
        dp[newMask][v] = min(
          dp[newMask][v],
          dp[mask][u] + dist[u][v])
  answer = min(dp[all][u] + dist[u][0])`,

      // ══════ BACKTRACKING ══════
      n_queens: `function nQueens(board, row):
  if row == N: return true            ← solution!
  for col = 0 to N-1:
    if isSafe(row, col):
      board[row][col] = 1             ← place queen
      if nQueens(board, row+1):
        return true
      board[row][col] = 0             ← backtrack`,

      sudoku: `function solveSudoku(board):
  find empty cell (r, c)
  if none: return true                ← solved!
  for num = 1 to 9:
    if isValid(r, c, num):
      board[r][c] = num
      if solveSudoku(board): return true
      board[r][c] = 0                 ← backtrack`,

      knights_tour: `function knightsTour(board, x, y, move):
  board[x][y] = move
  if move == N²-1: return true        ← complete!
  for each knight move (dx, dy):
    nx, ny = x+dx, y+dy
    if valid and unvisited:
      if knightsTour(board, nx, ny, move+1):
        return true
  board[x][y] = -1                    ← backtrack`,

      subset_sum: `function subsetSum(arr, idx, target):
  if target == 0: return true         ← found!
  if idx == n: return false
  // Include arr[idx]
  if subsetSum(arr, idx+1, target-arr[idx]):
    return true
  // Exclude arr[idx]
  return subsetSum(arr, idx+1, target)`,

      permutations: `function permute(arr, start):
  if start == n:
    output arr                        ← one permutation
    return
  for i = start to n-1:
    swap(arr[start], arr[i])
    permute(arr, start+1)             ← recurse
    swap(arr[start], arr[i])          ← undo`,

      combinations: `function combine(arr, start, combo, k):
  if len(combo) == k:
    output combo                      ← one combination
    return
  for i = start to n-1:
    combo.add(arr[i])
    combine(arr, i+1, combo, k)       ← recurse
    combo.remove(last)                ← backtrack`,

      graph_coloring: `function graphColor(node, numColors):
  if node == V: return true           ← all colored!
  for c = 0 to numColors-1:
    if isSafe(node, c):               ← no neighbor has c
      colors[node] = c
      if graphColor(node+1): return true
      colors[node] = -1               ← backtrack`,

      rat_in_maze: `function ratMaze(maze, r, c):
  if (r,c) == destination: return true
  if valid(r, c):
    solution[r][c] = 1
    if ratMaze(r+1, c): return true   ← go down
    if ratMaze(r, c+1): return true   ← go right
    solution[r][c] = 0                ← backtrack`,

      word_search: `function wordSearch(board, word, r, c, idx):
  if idx == len(word): return true    ← found!
  if out of bounds or visited or
     board[r][c] ≠ word[idx]: return false
  visited.add(r, c)
  for (dr, dc) in 4 directions:
    if wordSearch(r+dr, c+dc, idx+1):
      return true
  visited.remove(r, c)               ← backtrack`,

      // ══════ STRING ══════
      kmp: `function KMP(text, pattern):
  // Build LPS (failure function)
  lps = computeLPS(pattern)
  i = 0, j = 0
  while i < len(text):
    if text[i] == pattern[j]:
      i++, j++
      if j == m: found at i-m        ← match!
    else:
      if j ≠ 0: j = lps[j-1]         ← use LPS
      else: i++`,

      rabin_karp: `function RabinKarp(text, pattern):
  pHash = hash(pattern)
  tHash = hash(text[0..m-1])
  for i = 0 to n-m:
    if pHash == tHash:
      if text[i..i+m] == pattern:
        found at i                    ← verify match
    // Rolling hash update
    tHash = rehash(tHash, text[i],
                   text[i+m])`,

      boyer_moore: `function BoyerMoore(text, pattern):
  build badChar table
  s = 0
  while s <= n-m:
    j = m-1
    while j >= 0 and pattern[j] == text[s+j]:
      j--                            ← match right to left
    if j < 0: found at s
    else:
      s += max(1, j - badChar[text[s+j]])`,

      z_algorithm: `function ZAlgorithm(text, pattern):
  concat = pattern + "$" + text
  Z = array of length |concat|
  l = r = 0
  for i = 1 to |concat|-1:
    if i < r: Z[i] = min(r-i, Z[i-l])
    while i+Z[i] < n and
          concat[Z[i]] == concat[i+Z[i]]:
      Z[i]++
    if i+Z[i] > r: l=i, r=i+Z[i]
    if Z[i] == m: found at i-m-1`,

      longest_palindrome: `function longestPalindromeDP(s):
  dp[i][i] = true for all i
  for len = 2 to n:
    for i = 0 to n-len:
      j = i + len - 1
      dp[i][j] = (s[i]==s[j]) and
                 (len≤3 or dp[i+1][j-1])
  track max length palindrome`,

      suffix_array: `function buildSuffixArray(text):
  suffixes = [(text[i:], i) for i in 0..n]
  sort suffixes lexicographically
  SA = [index for each sorted suffix]
  // Build LCP array from SA
  // LCP[i] = longest common prefix
  //   of SA[i] and SA[i-1]`,

      manacher: `function Manacher(s):
  // Transform: "abc" → "^#a#b#c#$"
  P[i] = palindrome radius at i
  C = center, R = right boundary
  for i = 1 to n-1:
    mirror = 2*C - i
    if i < R: P[i] = min(R-i, P[mirror])
    // Expand around center i
    while s[i+P[i]+1] == s[i-P[i]-1]:
      P[i]++
    if i+P[i] > R: C=i, R=i+P[i]`,

      aho_corasick: `function AhoCorasick(text, patterns):
  // Build trie from all patterns
  // Build failure links (like KMP for trie)
  // Process text character by character
  state = 0
  for each char in text:
    follow failure links until match
    state = goto[state][char]
    if output[state]: report matches`,

      suffix_tree: `Suffix Tree Construction:
  // Ukkonen's algorithm (online)
  for each character added:
    extend all suffixes
    use suffix links for efficiency
  // Or naive: insert all suffixes
  // Applications: pattern matching,
  //   LCS, repeated substrings`,

      // ══════ MATH ══════
      gcd: `function GCD(a, b):  // Euclidean
  while b ≠ 0:
    a, b = b, a mod b                ← divide
  return a`,

      sieve: `function SieveOfEratosthenes(n):
  is_prime[0..n] = true
  for i = 2 to √n:
    if is_prime[i]:
      for j = i² to n step i:
        is_prime[j] = false           ← composite`,

      fast_pow: `function fastPow(base, exp, mod):
  result = 1
  while exp > 0:
    if exp is odd:
      result = result * base          ← multiply
    base = base * base                ← square
    exp = exp / 2                     ← halve`,

      mod_inverse: `function modInverse(a, m):
  // Using Extended Euclidean
  gcd, x, y = extGCD(a, m)
  if gcd ≠ 1: no inverse exists
  return (x % m + m) % m`,

      prime_factor: `function primeFactors(n):
  d = 2
  while d * d <= n:
    while n % d == 0:
      output d                       ← found factor
      n = n / d
    d++
  if n > 1: output n                 ← remaining prime`,

      crt: `Chinese Remainder Theorem:
  Given: x ≡ r_i (mod m_i)
  M = product of all m_i
  for each equation:
    M_i = M / m_i
    y_i = modInverse(M_i, m_i)
    x += r_i * M_i * y_i
  x = x mod M`,

      extended_gcd: `function extGCD(a, b):
  if a == 0: return (b, 0, 1)
  gcd, x1, y1 = extGCD(b%a, a)
  x = y1 - (b/a) * x1
  y = x1
  return (gcd, x, y)
  // a*x + b*y = gcd(a,b)`,

      euler_totient: `function eulerTotient(n):
  result = n
  for each prime factor p of n:
    result -= result / p
    // Multiply by (1 - 1/p)
  return result
  // φ(n) = count of 1..n coprime to n`,

      miller_rabin: `function millerRabin(n, k):
  write n-1 = 2^r · d
  for k rounds:
    a = random in [2, n-2]
    x = a^d mod n
    if x == 1 or x == n-1: continue  ← probably prime
    for r-1 squarings:
      x = x² mod n
      if x == n-1: break
    if x ≠ n-1: return COMPOSITE
  return PROBABLY PRIME`,

      // ══════ DATA STRUCTURES ══════
      heap_ops: `Min-Heap Operations:
insert(val):
  add val at end
  sift-up: swap with parent
           while smaller than parent

extractMin():
  min = heap[0]
  heap[0] = heap[last]
  remove last
  sift-down: swap with smallest child
             while larger than children`,

      linkedlist_ops: `Linked List Operations:
insertHead(val): new→next = head; head = new
insertTail(val): traverse to end; last→next = new
delete(val): find prev; prev→next = node→next
reverse():
  prev = null, curr = head
  while curr:
    next = curr→next
    curr→next = prev                 ← reverse link
    prev = curr; curr = next
  head = prev`,

      hashtable_ops: `Hash Table:
insert(key):
  idx = hash(key) % size
  // Separate Chaining:
  table[idx].append(key)
  // Open Addressing (Linear Probing):
  while table[idx] occupied:
    idx = (idx + 1) % size           ← probe next
  table[idx] = key`,

      array_ops: `Array Operations:
insert(i, val): shift right from i; a[i]=val
delete(i): shift left from i+1
rotate(k): reverse(0,n); reverse(0,k); reverse(k,n)`,

      stack_ops: `Stack (LIFO):
push(val): top++; stack[top] = val
pop(): val = stack[top]; top--; return val
peek(): return stack[top]`,

      queue_ops: `Queue (FIFO):
enqueue(val): rear++; queue[rear] = val
dequeue(): val = queue[front]; front++; return val`,
    };

    return codes[algoId] || `// ${algoId} — ${category}\n// Algorithm pseudocode`;
  }

  // ─── EVENT BINDINGS ───
  function bindEvents() {
    // Navigation
    els.navBtns.forEach(btn => {
      btn.addEventListener('click', () => switchCategory(btn.dataset.category));
    });

    // Controls
    els.btnStart.addEventListener('click', startPlayback);
    els.btnPause.addEventListener('click', () => {
      isPaused ? resumePlayback() : pausePlayback();
    });
    els.btnStep.addEventListener('click', stepForward);
    els.btnReset.addEventListener('click', resetVisualization);
    els.btnRandom.addEventListener('click', randomizeData);

    // Speed slider
    els.speedSlider.addEventListener('input', () => {
      els.speedValue.textContent = els.speedSlider.value;
    });

    // Size slider
    els.sizeSlider.addEventListener('input', () => {
      els.sizeValue.textContent = els.sizeSlider.value;
    });
    els.sizeSlider.addEventListener('change', () => {
      randomizeData();
    });

    // Algorithm search
    const searchInput = document.getElementById('algo-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        const algos = REGISTRY[currentCategory] || [];
        _populateAlgoList(algos, currentCategory, searchInput.value);
      });
    }

    // Panel tabs
    els.panelTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        els.panelTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.panel-content').forEach(p => p.classList.add('hidden'));
        document.getElementById(`panel-${tab.dataset.panel}`).classList.remove('hidden');
      });
    });

    // Info modal
    els.infoBtn.addEventListener('click', () => {
      els.infoOverlay.style.display = 'flex';
    });
    els.infoClose.addEventListener('click', () => {
      els.infoOverlay.style.display = 'none';
    });
    els.infoOk.addEventListener('click', () => {
      els.infoOverlay.style.display = 'none';
    });

    // Quit button
    const quitBtn = document.getElementById('quit-btn');
    if (quitBtn) {
      quitBtn.addEventListener('click', () => {
        if (confirm('Quit AlgoVision? This will stop the server.')) {
          fetch(API.BASE_URL + '/shutdown', { method: 'POST' }).catch(() => {});
          document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;flex-direction:column;gap:12px;"><h1 style="font-size:2rem;">◈ AlgoVision</h1><p style="color:#888;">Server stopped. You can close this tab.</p></div>';
        }
      });
    }

    // Custom input modal
    els.btnCustom.addEventListener('click', () => {
      els.modalOverlay.style.display = 'flex';
    });
    els.modalClose.addEventListener('click', () => {
      els.modalOverlay.style.display = 'none';
    });
    els.modalCancel.addEventListener('click', () => {
      els.modalOverlay.style.display = 'none';
    });
    els.modalApply.addEventListener('click', () => {
      const raw = els.customArray.value.trim();
      if (raw) {
        const arr = raw.split(/[,\s]+/).map(Number).filter(n => !isNaN(n));
        if (arr.length) {
          SortingUI.setArray(arr);
          addLog(`Custom array: [${arr.join(', ')}]`, 'info');
        }
      }
      els.modalOverlay.style.display = 'none';
    });

    // Close modals on overlay click
    [els.modalOverlay, els.infoOverlay].forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) overlay.style.display = 'none';
      });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      switch (e.key) {
        case ' ':
          e.preventDefault();
          isPlaying ? pausePlayback() : startPlayback();
          break;
        case 'ArrowRight':
          e.preventDefault();
          stepForward();
          break;
        case 'r':
        case 'R':
          resetVisualization();
          break;
        case 'n':
        case 'N':
          randomizeData();
          break;
        case '+':
        case '=':
          els.speedSlider.value = Math.min(100, parseInt(els.speedSlider.value) + 5);
          els.speedValue.textContent = els.speedSlider.value;
          break;
        case '-':
        case '_':
          els.speedSlider.value = Math.max(1, parseInt(els.speedSlider.value) - 5);
          els.speedValue.textContent = els.speedSlider.value;
          break;
      }
    });

    // Canvas resize
    window.addEventListener('resize', Helpers.debounce(() => {
      canvasRenderer.resize();
      graphRenderer.resize();
      // Re-render current state
      const controller = getController();
      if (controller.getProgress?.().current > 0) {
        controller.goToStep?.(controller.getProgress().current);
      }
    }, 200));
  }

  // ─── INITIALIZATION ───
  function init() {
    bindEvents();
    switchCategory('sorting');
    addLog('AlgoVision ready. Pick an algorithm and press Run.', 'info');

    // Check backend
    API.healthCheck().then(ok => {
      if (ok) {
        addLog('Backend connected ✓', 'sorted');
      } else {
        addLog('Backend offline — using client-side mode', 'compare');
      }
    });
  }

  // Boot
  init();
})();

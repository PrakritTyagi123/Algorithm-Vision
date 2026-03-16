# ◈ AlgoVision

**113 algorithms. 11 categories. One visualizer.**

AlgoVision is an interactive algorithm visualization platform built with Python and vanilla JavaScript. Every algorithm runs step-by-step with colored bars, graph nodes, DP tables, and board grids — with sound.

![AlgoVision Demo](screenshots/01-hero-overview.png)

No React. No npm. No webpack. Just `python run.py` and it works.

---

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/algovision.git
cd algovision
python run.py
```

That's it. Opens `http://localhost:8000` in your browser. Dependencies install automatically.

**Requirements:** Python 3.9+ (nothing else needed)

![Landing Screen](screenshots/02-landing-sorting-default.png)

The app loads with sorting selected, random bars generated, ready to go. Pick any algorithm from the sidebar and hit Run.

---

## Sound

Click the speaker icon in the top-right corner to enable sound.

Every bar's height maps to a pitch on a **pentatonic scale** (C-D-E-G-A across 3 octaves). Short bars play low notes, tall bars play high notes. As the algorithm sorts the array, the tones naturally sweep from low to high — like the classic sorting sound videos on YouTube.

- Soft sine waves — no harsh buzzing
- Pentatonic scale — impossible to sound bad
- Stereo panning — left bars play in the left speaker, right bars in the right
- Completion sweep — a harp-like glissando plays through the sorted array when done
- Works for all categories — sorting, searching, graph traversal, DP tables, pathfinding

Press `M` to toggle mute.

---

## Features

- **113 algorithms** covering the full CS curriculum
- **Sorting sounds** — pentatonic pitch mapping, stereo panning, completion arpeggio
- **Step-by-step playback** with Play / Pause / Step / Reset controls
- **Speed & size sliders** to control animation speed and data size
- **Syntax-highlighted pseudocode** with active line tracking
- **Live metrics** — comparisons, swaps, steps counter
- **Algorithm search** — find any algorithm instantly
- **Grouped sidebar** — algorithms organized by subcategory
- **Complexity display** — time and space complexity for every algorithm
- **Custom input** — enter your own arrays, targets, graphs
- **Quit button** — cleanly stops the server from the browser
- **Standalone EXE** — build with Cython + PyArmor + PyInstaller

---

## Screenshots

### Overview

![Full App](screenshots/01-hero-overview.png)

The three-panel layout: algorithm sidebar on the left, visualization canvas in the center, code panel on the right. Metrics bar shows real-time comparisons, swaps, and steps.

![Landing Screen](screenshots/02-landing-sorting-default.png)

Fresh load — random bars generated, algorithm info panel showing time/space complexity, pseudocode ready in the code panel.

### Sorting Algorithms

15 sorting algorithms with colored semantic bars.

![Bubble Sort — comparing two elements](screenshots/03-sorting-bubble-compare.png)

Red bars show the current comparison. When they're out of order, they turn orange and swap.

![Quick Sort — pivot partitioning](screenshots/04-sorting-quick-pivot.png)

Blue pivot bar with orange swaps during partitioning.

![Merge Sort — merging two halves](screenshots/05-sorting-merge-merging.png)

Blue active sections show which subarrays are being merged together.

![Heap Sort — sift down operation](screenshots/06-sorting-heap-sift.png)

Compare and swap bars colored during the heap sift-down operation.

![Radix Sort — digit pass](screenshots/07-sorting-radix-pass.png)

Non-comparison sort — bars rearrange by digit position each pass.

![Sorting complete — all bars teal](screenshots/08-sorting-complete.png)

All bars turn teal when sorted. The completion sound plays an ascending sweep through the array.

### Searching Algorithms

7 searching algorithms with range brackets and pointer labels.

![Binary Search — range brackets narrowing](screenshots/09-searching-binary-brackets.png)

Blue dashed brackets show the active search range. Coral bar is the current probe. Grey bars are eliminated. Pointer labels show `low`, `mid`, `high` below the bars.

![Jump Search — block scanning](screenshots/10-searching-jump-blocks.png)

Block boundaries highlighted during the jump phase, then linear scan within the block.

![Interpolation Search — estimated probe](screenshots/11-searching-interpolation.png)

Probe position shifts proportionally based on value distribution, not just the midpoint.

### Graph Algorithms

22 graph algorithms rendered as nodes and edges with color-coded states.

![BFS — wave spreading through graph](screenshots/12-graph-bfs-traversal.png)

Purple visited nodes, blue frontier, coral current. The wavefront expands outward from the source.

![Dijkstra — shortest path found](screenshots/13-graph-dijkstra-path.png)

Cyan path from source to destination with distance labels.

![Kruskal — MST edges building](screenshots/14-graph-kruskal-mst.png)

Green MST edges added incrementally, skipping edges that would form cycles.

![Floyd-Warshall — distance matrix table](screenshots/15-graph-floyd-table.png)

All-pairs shortest paths rendered as a DP table with coral current cell and blue referenced values.

![Topological Sort — node ordering](screenshots/16-graph-topological.png)

Directed graph with nodes processing in dependency order.

![Ford-Fulkerson — augmenting path](screenshots/17-graph-ford-fulkerson.png)

Maximum flow with cyan augmenting paths from source to sink.

### Pathfinding

6 pathfinding algorithms on a 2D grid with guaranteed walkable paths.

![A* — solving the grid](screenshots/18-pathfinding-astar-solving.png)

Purple visited cells, blue frontier ring, coral current. A* expands fewer cells than BFS by using a heuristic.

![BFS Grid — wave expansion](screenshots/19-pathfinding-bfs-wave.png)

Uniform wave expanding in all directions from the start position.

![Path found — cyan trail](screenshots/20-pathfinding-path-found.png)

Cyan path traced from green start to red end through the explored area.

### Tree Algorithms

13 tree algorithms drawn as circles and edges on canvas.

![BST — inserting a node](screenshots/21-tree-bst-insert.png)

Green node shows where the new value was inserted in the binary search tree.

![AVL — rotation after imbalance](screenshots/22-tree-avl-rotation.png)

Orange highlighted nodes involved in a balance rotation.

![Inorder Traversal — left-root-right](screenshots/23-tree-inorder-traversal.png)

Coral current node, purple visited. For a BST, inorder produces sorted output.

### Dynamic Programming

12 DP algorithms with animated table filling.

![Knapsack — table filling](screenshots/24-dp-knapsack-table.png)

2D table with coral current cell being computed, blue cells being referenced.

![LCS — longest common subsequence](screenshots/25-dp-lcs-filling.png)

Character headers on rows and columns, diagonal references highlighted.

![Edit Distance — transformation cost](screenshots/26-dp-edit-distance.png)

Table showing minimum edit operations with traceback path.

### Backtracking, String, Math

![N-Queens — placing queens](screenshots/27-bt-nqueens-board.png)

4×4 board with teal placed queens and coral current try position. Conflicts flash orange before backtracking.

![KMP — prefix-based matching](screenshots/28-string-kmp-matching.png)

Character table with text and pattern rows, highlighted comparison window sliding across.

![Sieve of Eratosthenes — crossing out composites](screenshots/29-math-sieve-primes.png)

Number table with current prime highlighted, multiples being crossed out.

### UI Details

![Code panel with active line highlighting](screenshots/30-ui-code-panel.png)

Syntax-highlighted pseudocode: purple keywords, amber functions, blue numbers, grey comments. Yellow active line marker tracks the current step. Line numbers on the left.

---

## Algorithms (113)

### Sorting (15)
Bubble · Selection · Insertion · Merge · Quick · Heap · Shell · Counting · Radix · Bucket · Tim · Cocktail · Comb · Gnome · Bitonic

### Searching (7)
Linear · Binary · Jump · Interpolation · Exponential · Fibonacci · Ternary

### Graph (22)
BFS · DFS · Dijkstra · Bellman-Ford · Floyd-Warshall · A* · Kruskal · Prim · Borůvka · Topological Sort · Kahn's · Kosaraju SCC · Tarjan SCC · Bridges · Articulation Points · Euler Path · Ford-Fulkerson · Edmonds-Karp · Union-Find · Cycle Detection (Directed) · Cycle Detection (Undirected) · Johnson's

### Pathfinding (6)
A* Grid · Dijkstra Grid · BFS Grid · DFS Maze · Greedy Best-First · Jump Point Search

### Computational Geometry (5)
Convex Hull (Graham Scan) · Convex Hull (Jarvis March) · Closest Pair · Line Segment Intersection · Sweep Line

### Tree (13)
BST · Inorder · Preorder · Postorder · Level-Order · AVL · Red-Black · Segment Tree · Fenwick Tree · Trie · LCA · Height · Diameter

### Dynamic Programming (12)
Fibonacci · Knapsack · LCS · LIS · Matrix Chain · Edit Distance · Coin Change · Rod Cutting · Palindromic Subsequence · Min Path Sum · Partition Subset · TSP

### Backtracking (9)
N-Queens · Sudoku · Knight's Tour · Subset Sum · Permutations · Combinations · Graph Coloring · Rat in Maze · Word Search

### String (9)
KMP · Rabin-Karp · Boyer-Moore · Z Algorithm · Longest Palindrome · Suffix Array · Manacher · Aho-Corasick · Suffix Tree

### Math (9)
Euclidean GCD · Extended Euclidean · Sieve of Eratosthenes · Fast Exponentiation · Modular Inverse · Prime Factorization · Chinese Remainder Theorem · Euler's Totient · Miller-Rabin

### Data Structures (6)
Heap · Linked List · Hash Table · Array · Stack (LIFO) · Queue (FIFO)

---

## Project Structure

```
algovision/
├── backend/
│   ├── app.py                    # FastAPI main app
│   ├── routes/                   # API route handlers
│   ├── algorithms/               # 113 algorithm implementations
│   └── models/                   # Pydantic models
├── frontend/
│   ├── index.html                # Main UI
│   ├── css/                      # Styles (black/white theme)
│   └── js/
│       ├── main.js               # App orchestrator
│       ├── utils/
│       │   ├── helpers.js        # Utilities
│       │   ├── api.js            # Backend API client
│       │   └── audioEngine.js    # Pentatonic sorting sounds
│       ├── canvas/               # Canvas, graph, grid renderers
│       ├── visualizers/          # Sorting, tree, graph, DP visualizers
│       └── algorithms/           # UI controllers per category
├── shared/
│   └── algorithm_registry.json   # Metadata for all 113 algorithms
├── screenshots/                  # 30 screenshots for this README
├── run.py                        # One-click launcher
├── build_exe.py                  # Secure EXE builder (Cython + PyArmor + PyInstaller)
├── .gitignore
└── README.md
```

---

## API

```bash
curl "http://localhost:8000/sorting/bubble?array=5,3,8,1"
curl -X POST http://localhost:8000/dp/fibonacci -d '{"n":10}'
curl http://localhost:8000/registry
```

Full API docs at `http://localhost:8000/docs` (auto-generated by FastAPI).

---

## Build Standalone EXE

```bash
python build_exe.py              # Full: Cython + PyArmor + PyInstaller
python build_exe.py --no-cython  # PyArmor + PyInstaller only
python build_exe.py --no-armor   # Cython + PyInstaller only
python build_exe.py --basic      # PyInstaller only (no protection)
```

Creates `dist/AlgoVision.exe` — double-click to run, no Python needed.

| Layer | Protection |
|-------|-----------|
| Cython | Compiles `.py` → `.pyd` native binaries. Source code is gone. |
| PyArmor | Encrypts remaining `.py` with AES. Decrypted only in memory. |
| PyInstaller | Bundles Python + all deps into single `.exe`. |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `→` | Step Forward |
| `R` | Reset |
| `N` | Randomize |
| `M` | Toggle Sound |
| `+` / `-` | Speed Up / Slow Down |

---

## Tech Stack

Python · FastAPI · Uvicorn · Vanilla JavaScript · Canvas API · Web Audio API · HTML/CSS · IBM Plex Sans · JetBrains Mono

---

## License

MIT
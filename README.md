# ◈ AlgoVision — Algorithm Visualizer

An interactive platform that visualizes **113 algorithms** across **11 categories** with step-by-step animation, pseudocode highlighting, and real-time metrics.

<!-- Add your screenshots here -->
![AlgoVision Demo](screenshots/demo.png)

---

## Features

- **113 algorithms** covering the full CS curriculum
- **Step-by-step playback** with Play / Pause / Step / Reset controls
- **Speed & size sliders** to control animation speed and data size
- **Syntax-highlighted pseudocode** with active line tracking
- **Live metrics** — comparisons, swaps, steps counter
- **Algorithm search** — find any algorithm instantly
- **Grouped sidebar** — algorithms organized by subcategory
- **Complexity display** — time and space complexity for every algorithm
- **Custom input** — enter your own arrays, targets, graphs
- **One-click EXE build** — distribute as a standalone desktop app

---

## Screenshots

<!-- Replace these with your actual screenshots -->

| Sorting | Searching | Graph |
|---------|-----------|-------|
| ![Sorting](screenshots/sorting.png) | ![Searching](screenshots/searching.png) | ![Graph](screenshots/graph.png) |

| Tree | DP Table | Pathfinding |
|------|----------|-------------|
| ![Tree](screenshots/tree.png) | ![DP](screenshots/dp.png) | ![Pathfinding](screenshots/pathfinding.png) |

| Backtracking | String Matching | Data Structures |
|-------------|-----------------|-----------------|
| ![Backtracking](screenshots/backtracking.png) | ![String](screenshots/string.png) | ![DS](screenshots/ds.png) |

---

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/algovision.git
cd algovision

# Run (installs dependencies automatically)
python run.py
```

Opens `http://localhost:8000` in your browser. That's it.

### Requirements

- Python 3.9+
- No other setup needed — `run.py` installs FastAPI + Uvicorn automatically

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
│   ├── routes/
│   │   ├── sorting_routes.py     # GET /sorting/{algo}
│   │   ├── graph_routes.py       # POST /graph/{algo}, /pathfinding/{algo}
│   │   ├── tree_routes.py        # POST /tree, /dp, /backtracking, /string, /math, /ds
│   │   └── geometry_routes.py    # POST /geometry/{algo}
│   ├── algorithms/
│   │   ├── sorting/              # 15 sorting algorithms
│   │   ├── searching/            # 7 searching algorithms
│   │   ├── graph/                # 22 graph algorithms
│   │   ├── pathfinding/          # 6 pathfinding algorithms
│   │   ├── trees/                # 13 tree algorithms
│   │   ├── dp/                   # 12 DP algorithms
│   │   ├── backtracking/         # 9 backtracking algorithms
│   │   ├── string/               # 9 string algorithms
│   │   ├── math/                 # 9 math algorithms
│   │   ├── geometry/             # 5 geometry algorithms
│   │   └── datastructure/        # 6 data structure algorithms
│   └── models/                   # Pydantic models
├── frontend/
│   ├── index.html                # Main UI
│   ├── css/
│   │   ├── style.css             # Black/white theme, semantic colors
│   │   ├── layout.css            # 3-column grid layout
│   │   └── animations.css        # Entry animations
│   └── js/
│       ├── main.js               # App orchestrator
│       ├── utils/                # API client, helpers
│       ├── canvas/               # Canvas, graph, grid renderers
│       ├── visualizers/          # Sorting, tree, graph, DP visualizers
│       └── algorithms/           # UI controllers per category
├── shared/
│   └── algorithm_registry.json   # Metadata for all 113 algorithms
├── screenshots/                  # Add your screenshots here
├── run.py                        # One-click launcher
├── build_exe.py                  # Build standalone EXE
└── README.md
```

---

## API

Every algorithm returns step-by-step JSON:

```bash
# Sorting
curl "http://localhost:8000/sorting/bubble?array=38,27,43,3,9"

# Searching
curl "http://localhost:8000/searching/binary?array=3,9,27,38,43&target=27"

# Graph
curl -X POST http://localhost:8000/graph/dijkstra \
  -H "Content-Type: application/json" \
  -d '{"nodes":[{"id":0,"label":"A","x":0,"y":0},...], "edges":[...], "start_node":0, "end_node":4}'

# DP
curl -X POST http://localhost:8000/dp/fibonacci \
  -H "Content-Type: application/json" \
  -d '{"n": 10}'

# Registry (all algorithm metadata)
curl http://localhost:8000/registry
```

Each step contains visualization data:

```json
{
  "step": 1,
  "array": [38, 27, 43, 3, 9],
  "compare": [0, 1],
  "swap": [0, 1],
  "sorted": [],
  "description": "Compare 38 and 27 → swap"
}
```

---

## Build Standalone EXE

```bash
python build_exe.py
```

Creates `dist/AlgoVision.exe` (~40MB) — double-click to run, no Python needed.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `→` | Step Forward |
| `R` | Reset |
| `N` | Randomize |
| `+` | Speed Up |
| `-` | Slow Down |

---

## Design

- **Black & white UI** — pure white background, black text
- **Color only for semantics** — red=comparing, orange=swapping, teal=sorted, blue=active, coral=current
- **IBM Plex Sans** for UI, **JetBrains Mono** for code
- **Responsive** — works on desktop and tablets

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | Vanilla JS, Canvas API, HTML/CSS |
| Fonts | IBM Plex Sans, JetBrains Mono |
| Build | PyInstaller (optional EXE) |

No React, no npm, no webpack. Just Python + vanilla JS.

---

## Contributing

1. Fork the repo
2. Add your algorithm in `backend/algorithms/{category}/`
3. Return steps in the standard format: `[{step, array/table/board/tree, description, ...}]`
4. Add pseudocode in `frontend/js/main.js` under `_getPseudocode`
5. Add metadata to `shared/algorithm_registry.json`
6. Submit a PR

---

## License

MIT

---

Built with curiosity and too much coffee.
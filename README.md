# AlgoVision — Interactive Algorithm Visualizer

A professional interactive algorithm visualization platform built with FastAPI + Vanilla JS + Canvas.

## Quick Start

```bash
chmod +x run.sh
./run.sh
```

Then open **http://localhost:8000** in your browser.

## Architecture

```
├── backend/           FastAPI server
│   ├── algorithms/    Pure algorithm implementations (return step lists)
│   ├── routes/        API endpoints per category
│   ├── models/        Pydantic data models
│   ├── services/      Algorithm runner & step generator
│   └── utils/         Validators & data generators
├── frontend/          Vanilla JS + Canvas UI
│   ├── css/           Design tokens, layout, animations
│   └── js/
│       ├── canvas/    Low-level renderers (bars, graphs, grids)
│       ├── visualizers/ Step-applying logic per viz type
│       ├── algorithms/  UI controllers with client-side fallbacks
│       └── utils/     API client & helpers
└── run.sh             One-command launcher
```

## Algorithms Implemented (70+)

| Category       | Count | Examples                                        |
|----------------|-------|-------------------------------------------------|
| Sorting        | 15    | Bubble, Merge, Quick, Heap, Radix, Tim, Bitonic |
| Searching      | 7     | Binary, Jump, Interpolation, Fibonacci, Ternary |
| Graph          | 17    | BFS, DFS, Dijkstra, A*, Kruskal, Prim, Tarjan   |
| Pathfinding    | 6     | A* Grid, BFS Grid, DFS Maze, Greedy Best-First  |
| Tree           | 10    | BST, AVL, Traversals, Segment Tree, Trie         |
| Dynamic Prog   | 8     | Knapsack, LCS, LIS, Coin Change, Edit Distance  |
| Backtracking   | 6     | N-Queens, Sudoku, Knight's Tour, Subset Sum      |
| String         | 6     | KMP, Rabin-Karp, Boyer-Moore, Z-Algorithm        |
| Math           | 6     | GCD, Sieve, Fast Pow, Prime Factorization        |

## API

Every algorithm returns a list of **steps** the frontend animates:

```
GET  /sorting/bubble?array=5,3,8,1
GET  /searching/binary?array=1,3,5,8&target=5
POST /graph/dijkstra        { nodes, edges, start_node }
POST /pathfinding/a_star_grid { grid, start, end }
POST /dp/knapsack           { weights, profits, capacity }
POST /backtracking/n_queens { n: 8 }
GET  /string/kmp?text=ABCABC&pattern=ABC
POST /math/sieve            { n: 100 }
```

Interactive docs at **/docs** (Swagger UI).

## Keyboard Shortcuts

| Key     | Action       |
|---------|-------------|
| Space   | Play/Pause   |
| →       | Step Forward |
| R       | Reset        |
| N       | Randomize    |
| +/-     | Speed Up/Down|

## Features

- **Client-side fallback**: Works offline for core algorithms (Bubble, Selection, Insertion, Quick, Merge, BFS, DFS, N-Queens)
- **Dark/Light theme** toggle
- **Responsive layout** — collapses panels on smaller screens
- **Pseudocode panel** with current-line highlighting
- **Step log** with color-coded operations
- **Custom input** modal for manual data entry

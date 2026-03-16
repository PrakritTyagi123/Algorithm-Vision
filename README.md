# ◈ AlgoVision

**113 algorithms. 11 categories. One visualizer.**

AlgoVision is an interactive algorithm visualization platform built with Python and vanilla JavaScript. Every algorithm runs step-by-step with colored bars, graph nodes, DP tables, and board grids — so you can actually *see* how algorithms think.

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

## Sorting — 15 Algorithms

The sorting visualizer renders array elements as colored bars. Each step highlights what the algorithm is doing right now:

- **Red** = comparing two elements
- **Orange** = swapping positions
- **Teal** = element is in its final sorted position
- **Blue** = active element (pivot, current insertion point)

![Bubble Sort — comparing two elements](screenshots/03-sorting-bubble-compare.png)

Bubble Sort walks through the array repeatedly, comparing adjacent pairs. Red bars show the current comparison. When they're out of order, they turn orange and swap.

![Quick Sort — pivot partitioning](screenshots/04-sorting-quick-pivot.png)

Quick Sort picks a pivot (blue), then partitions everything around it. You can see elements being compared against the pivot and swapped into place.

![Merge Sort — merging two halves](screenshots/05-sorting-merge-merging.png)

Merge Sort splits the array recursively, then merges sorted halves back together. The blue sections show which subarrays are being merged.

The full list: Bubble, Selection, Insertion, Merge, Quick, Heap, Shell, Counting, Radix, Bucket, Tim, Cocktail, Comb, Gnome, Bitonic.

![Heap Sort — sift down operation](screenshots/06-sorting-heap-sift.png)

Heap Sort builds a max-heap then repeatedly extracts the maximum. You can watch the sift-down operation comparing parent and child nodes.

![Radix Sort — digit pass](screenshots/07-sorting-radix-pass.png)

Non-comparison sorts like Radix work differently — they distribute elements by digit. Each pass rearranges based on the current digit position.

![Sorting complete — all bars teal](screenshots/08-sorting-complete.png)

When the algorithm finishes, every bar turns teal. The metrics bar shows total comparisons, swaps, and steps.

---

## Searching — 7 Algorithms

Searching mode shows a sorted array with visual markers for the algorithm's search strategy:

- **Coral** = current probe position
- **Light teal** = already checked and eliminated
- **Bright green** = target found
- **Blue dashed brackets** = active search range `[lo..hi]`
- **Dimmed grey** = eliminated from search

![Binary Search — range brackets narrowing](screenshots/09-searching-binary-brackets.png)

Binary Search divides the range in half each step. The blue brackets show `[lo..hi]`, the coral bar is `mid`, and grey bars are eliminated. Pointer labels (`low`, `mid`, `high`) appear below the bars.

![Jump Search — block scanning](screenshots/10-searching-jump-blocks.png)

Jump Search leaps forward in fixed blocks, then scans linearly when it overshoots. You can see the block boundaries and the linear scan phase.

![Interpolation Search — estimated probe](screenshots/11-searching-interpolation.png)

Interpolation Search estimates where the target should be based on value distribution, not just the midpoint. The probe position shifts proportionally.

Also includes: Linear, Exponential, Fibonacci, and Ternary search.

---

## Graph — 22 Algorithms

The graph visualizer renders nodes as circles and edges as lines. Colors show algorithm state:

- **Coral** = current node being processed
- **Purple** = already visited
- **Blue** = in the frontier/queue
- **Cyan** = shortest path or result
- **Green edges** = MST or selected edges

![BFS — wave spreading through graph](screenshots/12-graph-bfs-traversal.png)

BFS explores all neighbors at the current depth before going deeper. You can see the wavefront of blue frontier nodes expanding outward from the source.

![Dijkstra — shortest path found](screenshots/13-graph-dijkstra-path.png)

Dijkstra finds the shortest weighted path. When complete, the cyan path lights up from source to destination, with distance labels on each node.

![Kruskal — MST edges building](screenshots/14-graph-kruskal-mst.png)

Kruskal's MST algorithm sorts edges by weight and adds them if they don't form a cycle. Green edges show the MST being built incrementally.

![Floyd-Warshall — distance matrix table](screenshots/15-graph-floyd-table.png)

Floyd-Warshall computes all-pairs shortest paths using a DP table. The coral cell is the one currently being updated, blue cells are the referenced values.

![Topological Sort — node ordering](screenshots/16-graph-topological.png)

Topological Sort processes nodes in dependency order. Nodes light up as they're added to the topological ordering. Works with directed graphs automatically.

![Ford-Fulkerson — augmenting path](screenshots/17-graph-ford-fulkerson.png)

Ford-Fulkerson finds maximum flow by repeatedly finding augmenting paths from source to sink. The cyan path shows the current augmenting path being used.

Also includes: DFS, Bellman-Ford, A*, Prim, Borůvka, Kahn's, Kosaraju SCC, Tarjan SCC, Bridges, Articulation Points, Euler Path, Edmonds-Karp, Union-Find, Cycle Detection (both directed and undirected), Johnson's.

---

## Pathfinding — 6 Algorithms

The grid visualizer shows a 2D grid with:

- **Green cell** = start position
- **Red cell** = end position
- **Dark cells** = walls
- **Purple** = visited cells
- **Blue** = frontier (cells about to be explored)
- **Coral** = current cell
- **Cyan line** = final path

Every grid is generated with a guaranteed walkable path between start and end.

![A* — solving the grid](screenshots/18-pathfinding-astar-solving.png)

A* uses a heuristic to guide the search toward the goal. You can see how it expands fewer cells than BFS by prioritizing cells closer to the end.

![BFS Grid — wave expansion](screenshots/19-pathfinding-bfs-wave.png)

BFS expands uniformly in all directions like a ripple in water. It guarantees the shortest path on unweighted grids.

![Path found — cyan trail](screenshots/20-pathfinding-path-found.png)

When the algorithm reaches the end, it traces back the shortest path in cyan. The visited purple cells show how much of the grid was explored.

Also includes: Dijkstra Grid, DFS Maze, Greedy Best-First, Jump Point Search.

---

## Tree — 13 Algorithms

Tree algorithms render binary trees with nodes and edges. Colors indicate what the algorithm is doing:

- **Green** = newly inserted node
- **Coral** = current node being processed
- **Purple** = already visited
- **Orange** = nodes involved in a rotation

![BST — inserting a node](screenshots/21-tree-bst-insert.png)

BST insertion traverses from root, comparing at each level, then places the new node as a leaf. The green node shows where it landed.

![AVL — rotation after imbalance](screenshots/22-tree-avl-rotation.png)

AVL trees self-balance after insertions. When a node becomes unbalanced, the tree performs a rotation. Orange nodes show the rotation participants.

![Inorder Traversal — left-root-right](screenshots/23-tree-inorder-traversal.png)

Inorder traversal visits left subtree, then root, then right subtree. The coral node is the current position, purple nodes have been visited. For a BST, this produces sorted output.

Also includes: Preorder, Postorder, Level-Order, Red-Black Tree, Segment Tree, Fenwick Tree, Trie, LCA, Tree Height, Tree Diameter.

---

## Dynamic Programming — 12 Algorithms

DP algorithms display a table that fills in cell by cell:

- **Coral cell** = currently being computed
- **Blue cells** = cells being referenced to compute the current value
- **Grey cells** = already filled

![Knapsack — table filling](screenshots/24-dp-knapsack-table.png)

The 0/1 Knapsack fills a 2D table where rows are items and columns are capacities. Each cell shows the maximum value achievable. You can see which previous cells contribute to the current computation.

![LCS — longest common subsequence](screenshots/25-dp-lcs-filling.png)

LCS compares two strings character by character. When characters match, the cell gets a diagonal value +1. The highlighted cells show the comparison being made.

![Edit Distance — transformation cost](screenshots/26-dp-edit-distance.png)

Edit Distance shows the minimum number of insertions, deletions, and substitutions to transform one string into another. The traceback path highlights the actual operations.

Also includes: Fibonacci, LIS, Matrix Chain, Coin Change, Rod Cutting, Palindromic Subsequence, Min Path Sum, Partition Equal Subset, TSP.

---

## Backtracking — 9 Algorithms

Board-based problems render as a grid. Array-based problems show element boxes:

- **Teal** = successfully placed
- **Coral** = currently trying
- **Orange** = conflict/backtrack

![N-Queens — placing queens](screenshots/27-bt-nqueens-board.png)

N-Queens places queens one row at a time. When a conflict is detected (same column or diagonal), the algorithm backtracks — you can see the coral "trying" cell and teal "placed" queens.

Also includes: Sudoku Solver, Knight's Tour, Subset Sum, Permutations, Combinations, Graph Coloring, Rat in Maze, Word Search.

---

## String Matching — 9 Algorithms

String algorithms display a character table showing text and pattern positions:

- **Highlighted cells** = current comparison window
- **Coral** = position being checked
- **Green** = match found

![KMP — prefix-based matching](screenshots/28-string-kmp-matching.png)

KMP uses a precomputed prefix table to skip redundant comparisons. The highlighted window slides across the text, and the current position shows which characters are being compared.

Also includes: Rabin-Karp, Boyer-Moore, Z Algorithm, Longest Palindrome, Suffix Array, Manacher, Aho-Corasick, Suffix Tree.

---

## Math — 9 Algorithms

Math algorithms display computation tables showing each step of the calculation:

![Sieve of Eratosthenes — crossing out composites](screenshots/29-math-sieve-primes.png)

The Sieve highlights the current prime, then crosses out all its multiples. Numbers that survive are prime. The table updates in real-time as each multiple gets eliminated.

Also includes: Euclidean GCD, Extended Euclidean, Fast Exponentiation, Modular Inverse, Prime Factorization, Chinese Remainder Theorem, Euler's Totient, Miller-Rabin.

---

## The Code Panel

Every algorithm has syntax-highlighted pseudocode on the right panel. The currently executing line highlights as the algorithm runs:

- **Purple** = keywords (`for`, `while`, `if`, `return`)
- **Amber** = function names
- **Blue** = numbers
- **Grey** = comments

![Code panel with active line highlighting](screenshots/30-ui-code-panel.png)

The line numbers and active-line marker help you follow exactly which line of pseudocode corresponds to the current visualization step. The description bar at the bottom explains what's happening in plain English.

---

## Data Structures — 6 Algorithms

Data structure operations render as array boxes with pointer labels:

- Stack shows `top` pointer, push slides in from right, pop removes from top (LIFO)
- Queue shows `front` and `rear` pointers, enqueue at rear, dequeue from front (FIFO)
- Heap shows sift-up/sift-down with compare and swap colors

Also includes: Linked List (insert/delete/reverse), Hash Table (chaining/open addressing), Array (insert/delete/rotate).

---

## Computational Geometry — 5 Algorithms

Geometry algorithms render points as nodes and hull/intersection edges as highlighted lines. Convex Hull (Graham Scan), Convex Hull (Jarvis March), Closest Pair of Points, Line Segment Intersection, Sweep Line.

---

## Architecture

```
algovision/
├── backend/          Python FastAPI — 113 algorithm implementations
├── frontend/         Vanilla JS + Canvas — zero dependencies
├── shared/           Algorithm registry JSON
├── screenshots/      30 screenshots for this README
├── run.py            One-click launcher
├── build_exe.py      Build standalone .exe
└── README.md
```

**Backend:** Each algorithm returns `[{step, array/table/board/tree, compare, swap, current, description, ...}]`. The frontend consumes this and renders frame by frame.

**Frontend:** Canvas renderer for bars/trees/graphs, HTML tables for DP/string/math, grid divs for pathfinding. No framework — just 12 vanilla JS files.

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
python build_exe.py
```

Creates `dist/AlgoVision.exe` (~40MB). Double-click to run — no Python installation needed on the target machine.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `→` | Step Forward |
| `R` | Reset |
| `N` | Randomize |
| `+` / `-` | Speed Up / Slow Down |

---

## Tech Stack

Python · FastAPI · Uvicorn · Vanilla JavaScript · Canvas API · HTML/CSS · IBM Plex Sans · JetBrains Mono

---

## License

MIT
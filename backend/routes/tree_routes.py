"""Routes for tree, DP, backtracking, string, and math algorithms."""
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from models.step import TreeInput, DPInput, BacktrackingInput, MathInput

router = APIRouter()

# ── Trees ──
from algorithms.trees.tree_algorithms import (
    bst_operations, inorder_traversal, preorder_traversal,
    postorder_traversal, levelorder_traversal, avl_operations,
)
from algorithms.trees.advanced_trees import (
    red_black_tree, segment_tree, fenwick_tree, trie_operations,
)
from algorithms.trees.missing_trees import (
    lowest_common_ancestor, tree_height, tree_diameter,
)

# ── DP ──
from algorithms.dp.dp_algorithms import (
    fibonacci_dp, knapsack, lcs, lis, coin_change,
    edit_distance, rod_cutting, matrix_chain,
)
from algorithms.dp.missing_dp import (
    longest_palindromic_subsequence, minimum_path_sum,
    partition_equal_subset_sum, traveling_salesman_dp,
)

# ── Backtracking ──
from algorithms.backtracking.backtracking_algorithms import (
    n_queens, sudoku_solver, knights_tour,
    subset_sum, permutations, combinations,
)
from algorithms.backtracking.missing_backtracking import (
    graph_coloring, rat_in_maze, word_search,
)
from algorithms.backtracking.fix_combinations import combinations_fixed

# ── String ──
from algorithms.string.string_algorithms import (
    kmp_search, rabin_karp, boyer_moore, z_algorithm, longest_palindrome,
)
from algorithms.string.suffix_array import suffix_array
from algorithms.string.missing_string import (
    manachers_algorithm, aho_corasick, suffix_tree_demo,
)

# ── Math ──
from algorithms.math.math_algorithms import (
    euclidean_gcd, sieve_of_eratosthenes, fast_exponentiation,
    modular_inverse, prime_factorization,
)
from algorithms.math.crt import chinese_remainder_theorem
from algorithms.math.missing_math import (
    extended_euclidean, euler_totient, miller_rabin,
)


@router.post("/tree/{algorithm}")
async def tree_endpoint(algorithm: str, data: TreeInput):
    values = data.values or [50, 30, 70, 20, 40, 60, 80]
    tree_map = {
        "bst": lambda: bst_operations(values),
        "inorder": lambda: inorder_traversal(values),
        "preorder": lambda: preorder_traversal(values),
        "postorder": lambda: postorder_traversal(values),
        "levelorder": lambda: levelorder_traversal(values),
        "avl": lambda: avl_operations(values),
        "red_black": lambda: red_black_tree(values),
        "segment": lambda: segment_tree(values),
        "fenwick": lambda: fenwick_tree(values),
        "trie": lambda: trie_operations(),
        "lca": lambda: lowest_common_ancestor(values, values[1] if len(values) > 1 else values[0], values[-1]),
        "height": lambda: tree_height(values),
        "diameter": lambda: tree_diameter(values),
    }
    func = tree_map.get(algorithm)
    if not func:
        return {"error": f"Unknown tree algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "tree", "total_steps": len(steps)}


@router.post("/dp/{algorithm}")
async def dp_endpoint(algorithm: str, data: DPInput):
    dp_map = {
        "fibonacci": lambda: fibonacci_dp(data.n or 10),
        "knapsack": lambda: knapsack(data.weights or [2,3,4,5], data.profits or [3,4,5,6], data.capacity or 8),
        "lcs": lambda: lcs(data.text1 or "ABCBDAB", data.text2 or "BDCAB"),
        "lis": lambda: lis(data.values or [10,22,9,33,21,50,41,60,80]),
        "coin_change": lambda: coin_change(data.coins or [1,5,10,25], data.amount or 30),
        "edit_distance": lambda: edit_distance(data.text1 or "kitten", data.text2 or "sitting"),
        "rod_cutting": lambda: rod_cutting(
            data.prices or data.values or [1,5,8,9,10,17,17,20],
            min(data.n or 8, len(data.prices or data.values or [1,5,8,9,10,17,17,20]))
        ),
        "matrix_chain": lambda: matrix_chain(data.values or [10,20,30,40,30]),
        "longest_palindromic_subseq": lambda: longest_palindromic_subsequence(data.text1 or "BBABCBCAB"),
        "palindromic_subseq": lambda: longest_palindromic_subsequence(data.text1 or "BBABCBCAB"),
        "min_path_sum": lambda: minimum_path_sum(_make_grid(data.values or [1,3,1,1,5,1,4,2,1])),
        "partition_subset": lambda: partition_equal_subset_sum(data.values or [1,5,11,5]),
        "tsp": lambda: traveling_salesman_dp(_make_dist_matrix(data.values or [0,10,15,20,10,0,35,25,15,35,0,30,20,25,30,0])),
    }
    func = dp_map.get(algorithm)
    if not func:
        return {"error": f"Unknown DP algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "dp", "total_steps": len(steps)}


def _make_grid(flat):
    import math as m
    n = int(m.sqrt(len(flat)))
    if n * n != len(flat):
        n, flat = 3, (flat + [1]*9)[:9]
    return [flat[i*n:(i+1)*n] for i in range(n)]


def _make_dist_matrix(flat):
    import math as m
    n = int(m.sqrt(len(flat)))
    return [flat[i*n:(i+1)*n] for i in range(n)]


@router.post("/backtracking/{algorithm}")
async def backtracking_endpoint(algorithm: str, data: BacktrackingInput):
    bt_map = {
        "n_queens": lambda: n_queens(data.n or 8),
        "sudoku": lambda: sudoku_solver(data.board or [
            [5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]),
        "knights_tour": lambda: knights_tour(min(data.n or 5, 6)),
        "subset_sum": lambda: subset_sum(data.values or [3,34,4,12,5,2], data.target or 9),
        "permutations": lambda: permutations(data.values or [1,2,3]),
        "combinations": lambda: combinations_fixed(data.values or [1,2,3,4], data.target or 2),
        "graph_coloring": lambda: graph_coloring(_build_adj(data.n or 4), data.n or 4, 3),
        "rat_maze": lambda: rat_in_maze(_default_maze(data.n or 4)),
        "rat_in_maze": lambda: rat_in_maze(_default_maze(data.n or 4)),
        "word_search": lambda: word_search([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"),
    }
    func = bt_map.get(algorithm)
    if not func:
        return {"error": f"Unknown backtracking algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "backtracking", "total_steps": len(steps)}


def _build_adj(n):
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if (i+j) % 2 == 0 or j == i+1:
                adj[i].append((j,1)); adj[j].append((i,1))
    return adj


def _default_maze(n):
    # Maze where 1=open, 0=blocked. Path must exist from (0,0) to (n-1,n-1).
    if n == 4:
        return [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
        ]
    # Generic: diagonal path always open
    maze = [[0]*n for _ in range(n)]
    for i in range(n):
        maze[i][i] = 1
        if i + 1 < n:
            maze[i][i + 1] = 1
    return maze


@router.get("/string/{algorithm}")
async def string_endpoint(algorithm: str,
                          text: str = Query("ABABDABACDABABCABAB"),
                          pattern: str = Query("ABABCABAB")):
    str_map = {
        "kmp": lambda: kmp_search(text, pattern),
        "rabin_karp": lambda: rabin_karp(text, pattern),
        "boyer_moore": lambda: boyer_moore(text, pattern),
        "z_algorithm": lambda: z_algorithm(text, pattern),
        "longest_palindrome": lambda: longest_palindrome(text),
        "suffix_array": lambda: suffix_array(text),
        "manacher": lambda: manachers_algorithm(text),
        "aho_corasick": lambda: aho_corasick(text, pattern.split(",")),
        "suffix_tree": lambda: suffix_tree_demo(text),
    }
    func = str_map.get(algorithm)
    if not func:
        return {"error": f"Unknown string algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "string", "total_steps": len(steps)}


@router.post("/math/{algorithm}")
async def math_endpoint(algorithm: str, data: MathInput):
    math_map = {
        "gcd": lambda: euclidean_gcd(data.a or 48, data.b or 18),
        "sieve": lambda: sieve_of_eratosthenes(data.n or 50),
        "fast_pow": lambda: fast_exponentiation(data.base or 2, data.exp or 10, data.mod),
        "mod_inverse": lambda: modular_inverse(data.a or 3, data.n or 11),
        "prime_factor": lambda: prime_factorization(data.n or 360),
        "crt": lambda: chinese_remainder_theorem([data.a or 2, data.b or 3, 2], [3, 5, 7]),
        "extended_gcd": lambda: extended_euclidean(data.a or 48, data.b or 18),
        "ext_euclid": lambda: extended_euclidean(data.a or 48, data.b or 18),
        "euler_totient": lambda: euler_totient(data.n or 36),
        "miller_rabin": lambda: miller_rabin(data.n or 97),
    }
    func = math_map.get(algorithm)
    if not func:
        return {"error": f"Unknown math algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "math", "total_steps": len(steps)}


# ── DATA STRUCTURES ──
from algorithms.datastructure.ds_operations import (
    heap_operations, linked_list_operations, hash_table_operations,
    stack_operations, queue_operations,
)

class DSInput(BaseModel):
    values: Optional[list] = None
    keys: Optional[list] = None
    table_size: Optional[int] = None

@router.post("/datastructure/{algorithm}")
async def ds_endpoint(algorithm: str, data: DSInput):
    ds_map = {
        "heap_ops": lambda: heap_operations(data.values or [15, 10, 20, 8, 25, 5, 30]),
        "linkedlist_ops": lambda: linked_list_operations(data.values or [10, 20, 30, 40, 50]),
        "hashtable_ops": lambda: hash_table_operations(
            data.keys or [12, 25, 36, 47, 58, 69, 72, 81], data.table_size or 10),
        "array_ops": lambda: linked_list_operations(data.values or [10, 20, 30, 40, 50]),
        "stack_ops": lambda: stack_operations(data.values or [10, 20, 30, 40, 50]),
        "queue_ops": lambda: queue_operations(data.values or [10, 20, 30, 40, 50]),
    }
    func = ds_map.get(algorithm)
    if not func:
        return {"error": f"Unknown data structure: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "datastructure", "total_steps": len(steps)}

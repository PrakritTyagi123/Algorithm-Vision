"""Routes for graph, pathfinding, geometry, and data structure algorithms."""
from fastapi import APIRouter
from models.step import GraphInput, GridInput
from models.graph import GraphModel

router = APIRouter()

# ── Graph core ──
from algorithms.graph.bfs import bfs
from algorithms.graph.dfs import dfs
from algorithms.graph.dijkstra import dijkstra
from algorithms.graph.bellman_ford import bellman_ford
from algorithms.graph.kruskal import kruskal
from algorithms.graph.prim import prim
from algorithms.graph.boruvka import boruvka
from algorithms.graph.topological_sort import topological_sort
from algorithms.graph.floyd_warshall import floyd_warshall
from algorithms.graph.a_star import a_star
from algorithms.graph.advanced import kosaraju, tarjan, find_bridges, find_articulation_points
from algorithms.graph.euler import euler_path
from algorithms.graph.max_flow import ford_fulkerson, edmonds_karp
from algorithms.graph.missing_graph import (
    union_find_demo, kahns_algorithm,
    cycle_detection_directed, cycle_detection_undirected,
    johnsons_algorithm,
)
from algorithms.geometry.geometry_algorithms import (
    convex_hull_graham, convex_hull_jarvis, closest_pair_of_points,
)

# ── Pathfinding ──
from algorithms.pathfinding.pathfinding_algorithms import (
    bfs_grid, dfs_maze, a_star_grid, dijkstra_grid, greedy_best_first,
)
from algorithms.pathfinding.jump_point_search import jump_point_search


@router.post("/graph/{algorithm}")
async def graph_endpoint(algorithm: str, data: GraphInput):
    g = GraphModel(data.nodes, data.edges, data.directed)

    # These algorithms require a directed graph
    directed_algos = {"topological", "kahns", "cycle_directed", "kosaraju", "tarjan"}
    if algorithm in directed_algos and not data.directed:
        g_dir = GraphModel(data.nodes, data.edges, True)
    else:
        g_dir = g

    end = data.end_node if data.end_node is not None else g.node_count - 1

    algo_map = {
        "bfs": lambda: bfs(g.adj, data.start_node, end),
        "dfs": lambda: dfs(g.adj, data.start_node, end),
        "dijkstra": lambda: dijkstra(g.adj, data.start_node, end),
        "bellman_ford": lambda: bellman_ford(g.adj, g.get_unique_edges(), g.node_count, data.start_node),
        "kruskal": lambda: kruskal(g.get_unique_edges(), g.node_count),
        "prim": lambda: prim(g.adj, data.start_node),
        "boruvka": lambda: boruvka(g.get_unique_edges(), g.node_count),
        "topological": lambda: topological_sort(g_dir.adj, g_dir.node_count),
        "floyd_warshall": lambda: floyd_warshall(g.adj, g.node_count),
        "a_star": lambda: a_star(g.adj, data.nodes, data.start_node, end),
        "kosaraju": lambda: kosaraju(g_dir.adj, g_dir.node_count),
        "tarjan": lambda: tarjan(g_dir.adj, g_dir.node_count),
        "bridges": lambda: find_bridges(g.adj, g.node_count),
        "articulation": lambda: find_articulation_points(g.adj, g.node_count),
        "euler_path": lambda: euler_path(g.adj, g.node_count),
        "ford_fulkerson": lambda: ford_fulkerson(g.adj, g.node_count, data.start_node, end),
        "edmonds_karp": lambda: edmonds_karp(g.adj, g.node_count, data.start_node, end),
        "union_find": lambda: union_find_demo(g.get_unique_edges(), g.node_count),
        "kahns": lambda: kahns_algorithm(g_dir.adj, g_dir.node_count),
        "cycle_directed": lambda: cycle_detection_directed(g_dir.adj, g_dir.node_count),
        "cycle_undirected": lambda: cycle_detection_undirected(g.adj, g.node_count),
        "johnsons": lambda: johnsons_algorithm(g.adj, g.node_count),
        "johnson": lambda: johnsons_algorithm(g.adj, g.node_count),
        # Geometry (pass node coordinates as points)
        "convex_hull_graham": lambda: convex_hull_graham([[n["x"], n["y"]] for n in data.nodes]),
        "convex_hull_jarvis": lambda: convex_hull_jarvis([[n["x"], n["y"]] for n in data.nodes]),
        "closest_pair": lambda: closest_pair_of_points([[n["x"], n["y"]] for n in data.nodes]),
    }

    func = algo_map.get(algorithm)
    if not func:
        return {"error": f"Unknown graph algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "graph", "total_steps": len(steps)}


@router.post("/pathfinding/{algorithm}")
async def pathfinding_endpoint(algorithm: str, data: GridInput):
    algo_map = {
        "bfs_grid": bfs_grid,
        "dfs_maze": dfs_maze,
        "a_star_grid": a_star_grid,
        "dijkstra_grid": dijkstra_grid,
        "greedy_best": greedy_best_first,
        "jump_point": jump_point_search,
    }
    func = algo_map.get(algorithm)
    if not func:
        return {"error": f"Unknown pathfinding algorithm: {algorithm}"}
    steps = func(data.grid, data.start, data.end)
    return {"steps": steps, "algorithm": algorithm, "category": "pathfinding", "total_steps": len(steps)}

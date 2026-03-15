"""
AlgoVision — Step Model
Pydantic models for algorithm visualization steps.
Each algorithm returns a list of Step objects describing
every atomic operation the frontend should animate.
"""

from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel


class Step(BaseModel):
    """A single visualization step."""
    step: int
    description: str = ""

    # ── Array-based (sorting / searching) ──
    array: Optional[list[int | float]] = None
    compare: Optional[list[int]] = None
    swap: Optional[list[int]] = None
    sorted: Optional[list[int]] = None
    active: Optional[list[int] | int] = None
    current: Optional[int] = None
    found: Optional[int | list[int]] = None
    pointers: Optional[dict[str, int | None]] = None
    range: Optional[list[int]] = None  # [lo, hi] for search zone

    # ── Graph-based ──
    visited: Optional[list[Any]] = None
    frontier: Optional[list[Any]] = None
    edge_active: Optional[list[int]] = None
    edges_visited: Optional[list[list[int]]] = None
    mst_edges: Optional[list[list[int]]] = None
    distances: Optional[dict[str, float]] = None
    path: Optional[list[Any]] = None
    start_node: Optional[int] = None
    end_node: Optional[int] = None

    # ── Tree-based ──
    tree: Optional[dict] = None
    highlighted: Optional[list[Any]] = None
    inserted: Optional[Any] = None
    deleted: Optional[Any] = None
    rotated: Optional[list[Any]] = None

    # ── DP / Table-based ──
    table: Optional[list[list[Any]]] = None
    row_headers: Optional[list[str]] = None
    col_headers: Optional[list[str]] = None

    # ── Board-based (backtracking) ──
    board: Optional[list[list[Any]]] = None
    placed: Optional[list[list[int]]] = None
    conflict: Optional[list[list[int]]] = None


class StepList(BaseModel):
    """Response wrapper: a list of steps."""
    steps: list[Step]
    algorithm: str = ""
    category: str = ""
    total_steps: int = 0


class GraphInput(BaseModel):
    """Input payload for graph algorithms."""
    nodes: list[dict]
    edges: list[dict]
    start_node: int = 0
    end_node: Optional[int] = None
    directed: bool = False


class TreeInput(BaseModel):
    """Input payload for tree algorithms."""
    values: list[int | float] = []
    operation: str = "build"


class GridInput(BaseModel):
    """Input payload for pathfinding algorithms."""
    grid: list[list[int]]
    start: list[int]
    end: list[int]


class DPInput(BaseModel):
    """Generic input for DP algorithms."""
    values: Optional[list[int | float]] = None
    target: Optional[int] = None
    text1: Optional[str] = None
    text2: Optional[str] = None
    capacity: Optional[int] = None
    weights: Optional[list[int]] = None
    profits: Optional[list[int]] = None
    coins: Optional[list[int]] = None
    amount: Optional[int] = None
    n: Optional[int] = None
    prices: Optional[list[int]] = None


class BacktrackingInput(BaseModel):
    """Input for backtracking algorithms."""
    n: int = 8
    board: Optional[list[list[int]]] = None
    values: Optional[list[int]] = None
    target: Optional[int] = None


class StringInput(BaseModel):
    """Input for string algorithms."""
    text: str = ""
    pattern: str = ""


class MathInput(BaseModel):
    """Input for math algorithms."""
    a: Optional[int] = None
    b: Optional[int] = None
    n: Optional[int] = None
    base: Optional[int] = None
    exp: Optional[int] = None
    mod: Optional[int] = None

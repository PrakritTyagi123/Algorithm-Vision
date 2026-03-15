"""Routes for Computational Geometry algorithms."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

from algorithms.geometry.geometry_algorithms import (
    convex_hull_graham, convex_hull_jarvis, closest_pair_of_points,
)
from algorithms.geometry.advanced_geometry import (
    line_segment_intersection, sweep_line_intersections,
)


class GeometryInput(BaseModel):
    points: Optional[list] = None
    segments: Optional[list] = None


@router.post("/geometry/{algorithm}")
async def geometry_endpoint(algorithm: str, data: GeometryInput):
    default_points = [[0, 0], [4, 0], [4, 4], [0, 4], [2, 2], [1, 3], [3, 1]]

    algo_map = {
        "convex_hull_graham": lambda: convex_hull_graham(data.points or default_points),
        "convex_hull_jarvis": lambda: convex_hull_jarvis(data.points or default_points),
        "closest_pair": lambda: closest_pair_of_points(data.points or default_points),
        "line_intersection": lambda: line_segment_intersection(data.segments),
        "sweep_line": lambda: sweep_line_intersections(data.segments),
    }

    func = algo_map.get(algorithm)
    if not func:
        return {"error": f"Unknown geometry algorithm: {algorithm}"}
    steps = func()
    return {"steps": steps, "algorithm": algorithm, "category": "geometry", "total_steps": len(steps)}

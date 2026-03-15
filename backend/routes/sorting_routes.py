"""Routes for sorting and searching algorithms."""
from fastapi import APIRouter, Query

router = APIRouter()

from algorithms.sorting.bubble_sort import bubble_sort
from algorithms.sorting.selection_sort import selection_sort
from algorithms.sorting.insertion_sort import insertion_sort
from algorithms.sorting.merge_sort import merge_sort
from algorithms.sorting.quick_sort import quick_sort
from algorithms.sorting.heap_sort import heap_sort
from algorithms.sorting.shell_sort import shell_sort
from algorithms.sorting.radix_sort import radix_sort
from algorithms.sorting.cocktail_sort import cocktail_sort
from algorithms.sorting.comb_sort import comb_sort
from algorithms.sorting.gnome_sort import gnome_sort
from algorithms.sorting.counting_sort import counting_sort
from algorithms.sorting.bucket_sort import bucket_sort
from algorithms.sorting.tim_sort import tim_sort
from algorithms.sorting.bitonic_sort import bitonic_sort

from algorithms.searching.linear_search import linear_search
from algorithms.searching.binary_search import binary_search
from algorithms.searching.jump_search import jump_search
from algorithms.searching.interpolation_search import interpolation_search
from algorithms.searching.exponential_search import exponential_search
from algorithms.searching.fibonacci_search import fibonacci_search
from algorithms.searching.ternary_search import ternary_search

SORT_MAP = {
    "bubble": bubble_sort, "selection": selection_sort, "insertion": insertion_sort,
    "merge": merge_sort, "quick": quick_sort, "heap": heap_sort, "shell": shell_sort,
    "radix": radix_sort, "cocktail": cocktail_sort, "comb": comb_sort,
    "gnome": gnome_sort, "counting": counting_sort, "bucket": bucket_sort,
    "tim": tim_sort, "bitonic": bitonic_sort,
}

SEARCH_MAP = {
    "linear": linear_search, "binary": binary_search, "jump": jump_search,
    "interpolation": interpolation_search, "exponential": exponential_search,
    "fibonacci": fibonacci_search, "ternary": ternary_search,
}


def _parse_array(s: str) -> list[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip()]


@router.get("/sorting/{algorithm}")
async def sorting_endpoint(algorithm: str, array: str = Query("38,27,43,3,9,82,10")):
    func = SORT_MAP.get(algorithm)
    if not func:
        return {"error": f"Unknown sorting algorithm: {algorithm}"}
    steps = func(_parse_array(array))
    return {"steps": steps, "algorithm": algorithm, "category": "sorting", "total_steps": len(steps)}


@router.get("/searching/{algorithm}")
async def searching_endpoint(algorithm: str, array: str = Query("2,5,8,12,16,23,38,56,72,91"),
                              target: int = Query(23)):
    func = SEARCH_MAP.get(algorithm)
    if not func:
        return {"error": f"Unknown searching algorithm: {algorithm}"}
    steps = func(_parse_array(array), target)
    return {"steps": steps, "algorithm": algorithm, "category": "searching", "total_steps": len(steps)}

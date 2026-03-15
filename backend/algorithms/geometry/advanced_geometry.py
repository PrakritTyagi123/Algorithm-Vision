"""Additional Computational Geometry Algorithms."""
import math


def line_segment_intersection(segments: list) -> list[dict]:
    """Check all pairs of line segments for intersections. O(n^2)."""
    steps = []

    if not segments:
        segments = [
            [[1, 1], [4, 4]], [[1, 4], [4, 1]],
            [[2, 0], [2, 5]], [[0, 3], [5, 3]],
            [[5, 0], [6, 2]], [[0, 0], [1, 3]],
        ]

    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersects(seg1, seg2):
        A, B = seg1
        C, D = seg2
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    steps.append({"step": len(steps)+1,
                  "description": f"Testing {len(segments)} line segments for intersections"})

    found = []
    for i in range(len(segments)):
        for j in range(i+1, len(segments)):
            s1, s2 = segments[i], segments[j]
            hit = intersects(s1, s2)
            steps.append({
                "step": len(steps)+1,
                "edge_active": [i, j],
                "description": f"Segment {i} vs {j}: {'INTERSECT' if hit else 'no intersection'}",
            })
            if hit:
                found.append((i, j))

    steps.append({"step": len(steps)+1,
                  "description": f"Found {len(found)} intersection(s): {found}"})
    return steps


def sweep_line_intersections(segments: list) -> list[dict]:
    """Sweep line algorithm for segment intersections. O((n+k) log n)."""
    steps = []

    if not segments:
        segments = [
            [[1, 1], [4, 4]], [[1, 4], [4, 1]],
            [[2, 0], [2, 5]], [[0, 3], [5, 3]],
        ]

    # Create events: left endpoint = start, right endpoint = end
    events = []
    for i, seg in enumerate(segments):
        p1, p2 = seg
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        events.append((p1[0], 'start', i, p1, p2))
        events.append((p2[0], 'end', i, p1, p2))

    events.sort(key=lambda e: (e[0], 0 if e[1] == 'start' else 1))

    active = set()
    intersections = []

    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def segs_intersect(seg1, seg2):
        A, B = segments[seg1]
        C, D = segments[seg2]
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    for x, event_type, seg_id, p1, p2 in events:
        steps.append({
            "step": len(steps)+1,
            "current": [0, seg_id],
            "description": f"Sweep x={x:.1f}: {event_type} segment {seg_id}",
        })

        if event_type == 'start':
            # Check against all active segments
            for other in active:
                if segs_intersect(seg_id, other):
                    intersections.append((seg_id, other))
                    steps.append({
                        "step": len(steps)+1,
                        "edge_active": [seg_id, other],
                        "description": f"  INTERSECTION: segment {seg_id} x segment {other}",
                    })
            active.add(seg_id)
        else:
            active.discard(seg_id)

    steps.append({"step": len(steps)+1,
                  "description": f"Sweep complete: {len(intersections)} intersection(s) found"})
    return steps

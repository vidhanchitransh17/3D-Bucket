import pandas as pd
from parse_coordinates import parse_coordinates
from parse_lines import parse_lines


def build_adjacency(lines):
    adj = {}
    for c1, c2 in lines:
        adj.setdefault(c1, set()).add(c2)
        adj.setdefault(c2, set()).add(c1)
    return adj

def are_collinear(p1, p2, p3):
    # Check if points p1, p2, p3 are collinear in horizontal plane (y constant)
    # p = (x,y,z)
    if not (p1[1] == p2[1] == p3[1]):
        return False
    # Vector p1->p2 and p1->p3
    v1 = (p2[0]-p1[0], p2[2]-p1[2])  # ignore y since same
    v2 = (p3[0]-p1[0], p3[2]-p1[2])
    # Cross product zero means collinear
    cross = v1[0]*v2[1] - v1[1]*v2[0]
    return abs(cross) < 1e-6

def find_lines_with_3plus_points(coordinates, adj):
    # For each point, find all sets of 3+ collinear points connected by lines
    lines_sets = []  # list of sets of coordinate IDs that form lines of 3+
    visited_triplets = set()

    coord_ids = list(coordinates.keys())
    for i in range(len(coord_ids)):
        c1 = coord_ids[i]
        neighbors = adj.get(c1, [])
        for c2 in neighbors:
            for c3 in neighbors:
                if c2 >= c3:
                    continue
                triplet = tuple(sorted([c1,c2,c3]))
                if triplet in visited_triplets:
                    continue
                visited_triplets.add(triplet)
                p1, p2, p3 = coordinates[c1], coordinates[c2], coordinates[c3]
                if are_collinear(p1, p2, p3):
                    # Expand line beyond 3 points by checking neighbors along line direction
                    line_points = set(triplet)
                    # We try to grow in both directions:
                    # get direction vector from p1->p2
                    dx = p2[0]-p1[0]
                    dz = p2[2]-p1[2]
                    dy = p2[1]-p1[1]
                    # Try to add points collinear with these 3 points
                    for c_other in coord_ids:
                        if c_other in line_points:
                            continue
                        p_other = coordinates[c_other]
                        if abs(p_other[1] - p1[1]) > 1e-6:
                            continue
                        # check collinearity of p_other with p1 and p2
                        v1 = (dx, dz)
                        v2 = (p_other[0]-p1[0], p_other[2]-p1[2])
                        cross = v1[0]*v2[1] - v1[1]*v2[0]
                        if abs(cross) < 1e-6:
                            # Also ensure it connects via lines (adjacency)
                            # Simplified check: c_other connects to at least one point in line_points
                            if any(c_other in adj.get(pt, []) for pt in line_points):
                                line_points.add(c_other)
                    if len(line_points) >= 3:
                        lines_sets.append(line_points)
    return lines_sets

def classify_bucket1(coordinates, adj):
    lines_sets = find_lines_with_3plus_points(coordinates, adj)

    # For each coordinate, count how many distinct lines_sets it belongs to
    point_lines_count = {c:0 for c in coordinates.keys()}
    for line_set in lines_sets:
        for pt in line_set:
            point_lines_count[pt] += 1

    classification = {}
    for c, count in point_lines_count.items():
        if count >= 2:
            classification[c] = "multiple lines"
        elif count == 1:
            classification[c] = "one line"
        else:
            classification[c] = "none"
    return classification

def classify_bucket2(coordinates, adj):
    # For each coordinate, check if connected in all four directions on horizontal plane y constant:
    # Left (x decrease), Right (x increase), Forward (z increase), Backward (z decrease)
    bucket2 = {}
    for c, (x,y,z) in coordinates.items():
        neighbors = adj.get(c, set())
        directions = {'left': False, 'right': False, 'forward': False, 'backward': False}
        for n in neighbors:
            xn, yn, zn = coordinates[n]
            if abs(yn - y) > 1e-6:
                continue
            if abs(zn - z) < 1e-6:
                if xn < x:
                    directions['left'] = True
                elif xn > x:
                    directions['right'] = True
            if abs(xn - x) < 1e-6:
                if zn > z:
                    directions['forward'] = True
                elif zn < z:
                    directions['backward'] = True
        if all(directions.values()):
            bucket2[c] = "'+' intersection"
        else:
            bucket2[c] = "no '+'"
    return bucket2

def export_to_excel(coordinates, bucket1_cls, bucket2_cls, filename="Assignment/output.xlsx"):
    data = []
    for c, (x,y,z) in coordinates.items():
        data.append({
            "Coordinate ID": c,
            "x": x,
            "y": y,
            "z": z,
            "Bucket 1": bucket1_cls.get(c, ""),
            "Bucket 2": bucket2_cls.get(c, "")
        })
    df = pd.DataFrame(data)
    df.sort_values("Coordinate ID", inplace=True)
    df.to_excel(filename, index=False)
    print(f"Exported results to {filename}")

def main():
    # Read raw data from text files
    with open("Assignment\coordinates.txt", "r") as f:
        raw_coords = f.read()
    with open("Assignment\lines.txt", "r") as f:
        raw_lines = f.read()

    # Parse the input
    coordinates, _ = parse_coordinates(raw_coords)
    adj = parse_lines(raw_lines)

    # Classify
    bucket1_cls = classify_bucket1(coordinates, adj)
    bucket2_cls = classify_bucket2(coordinates, adj)

    # Export
    export_to_excel(coordinates, bucket1_cls, bucket2_cls)


if __name__ == "__main__":
    main()

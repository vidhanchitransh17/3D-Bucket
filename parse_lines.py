from collections import defaultdict

def parse_lines(raw_lines):
    line_entries = raw_lines.replace("\n", " ").split(";")
    connections = defaultdict(set)

    for entry in line_entries:
        parts = entry.strip().split()
        if len(parts) == 3:
            _, id1, id2 = parts
            id1, id2 = int(id1), int(id2)
            connections[id1].add(id2)
            connections[id2].add(id1)

    return connections

# Example usage
if __name__ == "__main__":
    with open("lines.txt", "r") as file:
        raw_lines = file.read()

    adjacency_dict = parse_lines(raw_lines)

    print("Parsed Line Connections (first 5):")
    for k in list(adjacency_dict.keys())[:5]:
        print(f"{k}: {adjacency_dict[k]}")

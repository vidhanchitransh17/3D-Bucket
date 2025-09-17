import pandas as pd

def parse_coordinates(raw_coordinates):
    coordinate_entries = raw_coordinates.replace("\n", " ").split(";")
    
    coord_dict = {}
    data = []

    for entry in coordinate_entries:
        parts = entry.strip().split()
        if len(parts) == 4:
            point_id = int(parts[0])
            x, y, z = map(float, parts[1:])
            coord_dict[point_id] = (x, y, z)
            data.append({"ID": point_id, "x": x, "y": y, "z": z})

    df = pd.DataFrame(data)
    return coord_dict, df

# Example usage
if __name__ == "__main__":
    with open("coordinates.txt", "r") as file:
        raw_coordinates = file.read()

    coord_dict, coord_df = parse_coordinates(raw_coordinates)

    print("Parsed Coordinate Dictionary (first 5):")
    print(dict(list(coord_dict.items())[:5]))

    print("\nCoordinate DataFrame Preview:")
    print(coord_df.head())

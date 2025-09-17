## 🔍 Problem Overview

We are given:
- A set of 3D coordinates: each with `(ID, x, y, z)`
- A set of connections (lines): each connecting two coordinate IDs.

### Goal:
Classify each coordinate into the following **two buckets** and export results into an Excel file:

---

## 🪣 Bucket Classification Logic

### ✅ **Bucket 1 — Line Membership**

Each coordinate is classified based on how many **distinct horizontal lines (of 3 or more connected points)** it is a part of.

- **"multiple lines"** → the coordinate is part of 2 or more such lines  
- **"one line"** → the coordinate is part of exactly 1 such line  
- **"none"** → not part of any such line

#### 🔍 Horizontal Line Definition
- A **horizontal line** lies entirely on a single constant **y-plane**
- A line of **3 or more collinear points** is considered a valid line
- Points must be connected through given lines (direct or indirect)

#### 📐 Collinearity Check (in x-z plane):
Given three points \\( A, B, C \\) with the same y-coordinate, we check if they lie on a straight line using the **2D cross product**:

Let:

- \\( \\vec{AB} = (x_2 - x_1, z_2 - z_1) \\)
- \\( \\vec{AC} = (x_3 - x_1, z_3 - z_1) \\)

Then:

\\[
\\text{cross} = (x_2 - x_1)(z_3 - z_1) - (z_2 - z_1)(x_3 - x_1)
\\]

If `cross == 0` (within floating-point tolerance), the points are collinear.

We expand this check beyond 3 points to find all connected, collinear points.

---

### ✅ **Bucket 2 — '+' Intersection Check**

A coordinate is classified as:

- **"'+' intersection"** → if it is connected in **all four** directions on the **horizontal plane**:
  - **Left** (x decreases)
  - **Right** (x increases)
  - **Forward** (z increases)
  - **Backward** (z decreases)

- **"no '+'"** → if any direction is missing

#### 🔍 Direction Determination
For a neighbor point to be considered in a direction:
- Must lie on the same **y-plane**
- Difference in only **x** or **z** determines direction:
  - Same z → left/right via x comparison
  - Same x → forward/backward via z comparison

---

## 🧠 Assumptions

- All input points and connections are valid and consistent
- Connections are **undirected**
- No diagonal directions considered in '+' detection
- Floating-point tolerance used for comparison (1e-6)

---

## 📦 Output

- Output is saved to an Excel file `output.xlsx`
- Each row contains:
  - `Coordinate ID`
  - `(x, y, z)`
  - `Bucket 1` classification
  - `Bucket 2` classification

---

## 🛠️ Implementation Structure

Project includes 3 Python modules:

1. **`parse_coordinates.py`** – Parses coordinate data into dictionary and DataFrame
2. **`parse_lines.py`** – Parses line data into adjacency list (undirected graph)
3. **`classify.py`** – Applies bucket logic and exports results

---

## ✅ Example Output (Excel Preview)

| Coordinate ID | x     | y    | z     | Bucket 1      | Bucket 2         |
|---------------|-------|------|-------|----------------|------------------|
| 1             | 0.0   | -1.5 | 0.0   | multiple lines | '+' intersection |
| 2             | 6.287 | -1.5 | 0.0   | one line       | no '+'           |
| 3             | 10.211| -1.5 | 0.0   | none           | no '+'           |

# R-tree Implementation for Spatial Indexing

This repository contains an implementation of an R-tree, a spatial data structure used for efficient searching of spatial objects, such as points or rectangles (representing areas of interest). This implementation is based on Python and utilizes basic object-oriented principles and spatial indexing techniques.

## Implementation Details

### Components

1. **Point Class**: Represents a point in 2D space with coordinates (x, y).
2. **Rect Class**: Represents a rectangle defined by two points (low and high).
3. **EntryBlock Class**: Represents an entry in the R-tree, containing a rectangle and associated points.
4. **LeafNode Class**: Represents a leaf node in the R-tree, containing entries.
5. **LeaflessNode Class**: Represents a non-leaf node in the R-tree, containing child nodes or leaf nodes.
6. **RTree Class**: Implements the R-tree structure with methods for insertion, bulk loading, and tree statistics.
7. **Bulk Load Function**: Efficiently loads entries into the R-tree using bulk loading techniques.
8. **Tree Stats Function**: Calculates and prints statistics about the R-tree structure, including height and node counts.

### Usage

#### Setting Up and Running

1. **Clone the Repository**:
```bash
git clone https://github.com/KPapantoniou/Rtree.git
```

2. **Run the R-tree Implementation**:
```bash
python3 part1.py data.txt
```
## Output
Upon running the program, the R-tree will be constructed, and statistics about the tree structure (such as height and node counts) will be printed to the console. Additionally, the resulting R-tree structure will be written to a file (Rtree.txt).

## Contributors
Konstatninos Papantoniou


### Part 2: README.md for R-tree Querying


# R-tree Querying for Nearest Neighbors

This repository provides functionalities to query an R-tree structure for nearest neighbors based on a given query point (`q`) and the number of nearest neighbors (`k`).

## Implementation Details

### Components

1. **INNS Function**: Implements the Incremental Nearest Neighbor Search algorithm to find the `k` nearest neighbors to a query point `q`.
2. **mindist Function**: Computes the minimum distance between a query point `q` and a rectangle (`mbr`) representing an entry in the R-tree.

### Usage

#### Running Queries

**Run the Querying Script**:
```python3 part2.py <tree_file_path> <query_x> <query_y> <k>


- `<tree_file_path>`: Path to the file (`Rtree.txt`) containing the serialized R-tree structure.
- `<query_x>` and `<query_y>`: Coordinates of the query point `q`.
- `<k>`: Number of nearest neighbors to retrieve.
```
### Example

To query the R-tree for the 5 nearest neighbors to a query point (40.0, -73.0):

```
python rtree_query.py Rtree.txt 40.0 -73.0 5
```

## Output
The script will output the k nearest neighbors to the query point q, along with their distances. Additionally, execution time for the query will be printed.

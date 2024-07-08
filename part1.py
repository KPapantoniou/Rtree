# Konstatninos Papantoniu, 4769

from sys import argv
from math import ceil, floor,sqrt
import time

start_time = time.time()


class Point:
    def __init__(self,id, x: float, y: float):
        self.id =id
        self.x = x
        self.y = y
    def __str__(self) :
        return f"({self.x}, {self.y})"

class Rect:
    def __init__(self, low: Point, high: Point):
        self.low = low 
        self.high = high
     
    def __str__(self):
        return f"{self.low.x} {self.low.y} {self.high.x} {self.high.y}"

class EntryBlock:
    def __init__(self, id, rect):
        self.id = id
        self.rect = rect
        self.points = []

    def add_point(self, point: Point):
        self.points.append(point)

    def get_points(self):
        return self.points
    
    

class LeafNode:
    def __init__(self, id, entries):
        self.id = id
        self.entries = entries

    def get_entries(self):
        return [(entry.id, entry.rect) for entry in self.entries]
    
    def calculate_mbr(self):
       
        min_x_low = min(entry.rect.low.x for entry in self.entries)
        max_x_high = max(entry.rect.high.x for entry in self.entries)
        min_y_low = min(entry.rect.low.y for entry in self.entries)
        max_y_high = max(entry.rect.high.y for entry in self.entries)
        
       
        mbr_rect = Rect(Point(self.id, min_x_low, min_y_low), Point(self.id, max_x_high, max_y_high))
        

        return mbr_rect
    
    def area(self):
        mbr = self.calculate_mbr()
        return (mbr.high.x - mbr.low.x) * (mbr.high.y - mbr.low.y)
    
    def __str__(self):

        entry_strings = ' , '.join(f"({entry.id}, {point})" for entry in self.entries for point in entry.get_points())
        return f"{self.id}, {len(self.entries)}, 0 , {entry_strings}"
    


class LeaflessNode:
    def __init__(self, id):
        self.id = id
        self.children = []
        self.mbr = Rect(Point(0,float('inf'), float('inf')), Point(0,float('-inf'), float('-inf')))

    def add_child(self, child):
        self.children.append(child)
        if isinstance(child, LeaflessNode):
            self.update_mbr()

    def update_mbr(self):
        if not self.children:
            return
            
        low_x = self.children[0].calculate_mbr().low.x
        low_y = self.children[0].calculate_mbr().low.y
        high_x = self.children[0].calculate_mbr().high.x
        high_y = self.children[0].calculate_mbr().high.y

        for child in self.children[1:]:
            child_mbr = child.calculate_mbr()
            self.mbr.low.x = min(low_x, child_mbr.low.x)
            self.mbr.low.y = min(low_y, child_mbr.low.y)
            self.mbr.high.x = max(high_x, child_mbr.high.x)
            self.mbr.high.y = max(high_y, child_mbr.high.y)      
      


    def calculate_mbr(self):
        if not self.children:
            return None
        
        for child in self.children: 
            child_mbr =  child.calculate_mbr()

            self.mbr.low.x = min(self.mbr.low.x, child_mbr.low.x)
            self.mbr.low.y = min(self.mbr.low.y, child_mbr.low.y)
            self.mbr.high.x = max(self.mbr.high.x, child_mbr.high.x)
            self.mbr.high.y = max(self.mbr.high.y, child_mbr.high.y)

        return self.mbr
    
    def area(self):
        return (self.mbr.high.x - self.mbr.low.x) * (self.mbr.high.y - self.mbr.low.y)
    
   

    def __str__(self):
        children_str = ', '.join(
            f"({child.id},[{child.calculate_mbr().low.x}, {child.calculate_mbr().low.y}, {child.calculate_mbr().high.x}, {child.calculate_mbr().high.y}])" if isinstance(child, LeafNode) 
            else f"({child.id},[{child.mbr.low.x}, {child.mbr.low.y}, {child.mbr.high.x}, {child.mbr.high.y}])" if isinstance(child, LeaflessNode) 
            else f"{child[0]},{child[1]}" for child in self.children
        )
        return f"{self.id} , {len(self.children)} , 1 , {children_str}"




class RTree:
    def __init__(self,max_nodes):
        self.root = None
        self.id=0
        self.max_nodes = max_nodes
        self.children = []
        self.leaf_nodes = []

        
    def create_root(self):
        self.root = LeaflessNode(self.id)
        for i in self.children:
            child = self.leaf_nodes[i]
            self.root.add_child(child)
        self.leaf_nodes.append(self.root)

    def add_starting_nodes(self):
        max_nodes = len(self.children) / self.max_nodes
        nodes_to_add = ceil(max_nodes)
        
        if nodes_to_add == 1:
            self.create_root()
        else:
            self.insert_leafless_node()            
            self.add_starting_nodes()


    def insert_leaf_node(self, entry):
        self.leaf_nodes.append(entry)
        self.children.append(len(self.leaf_nodes) - 1)
        entry.id = self.id
        self.id += 1

   

    def insert_leafless_node(self):
        identifiers = []
        child_indexes = []
        for start_index in range(0, len(self.children), self.max_nodes):
            end_index = start_index + self.max_nodes
            fragment = self.children[start_index:end_index]
            child_indexes.append(fragment)
            
        fragment_index = 0
        while fragment_index < len(child_indexes):
            fragment = child_indexes[fragment_index]
            identifiers.append(self.id)
            node = LeaflessNode(self.id)

            child_index = 0
            while child_index < len(fragment):
                child_id = fragment[child_index]
                if isinstance(child_id, int):
                    child = self.leaf_nodes[child_id]
                else:
                    child = child_id
                node.add_child(child)
                child_index += 1

            node.calculate_mbr()
            self.leaf_nodes.append(node)
            self.id += 1
            fragment_index += 1

        self.children = identifiers

  

    def write_tree(self, filename):
        out = open(filename, "w+")
        out.write(str(self.root.id) + "\n")
        i = 0 
        while i <= len(self.leaf_nodes) - 1:
            node = self.leaf_nodes[i]
            out.write(str(node) + "\n")
            i += 1
        out.close()

        
    def tree_stats(self):
        if not self.root:
            print("Tree is empty")
            return

        level_counts = {}
        level_mean_areas = {}
        height = 0
        queue = [(self.root, 0)]  

        while queue:
            node, level = queue.pop(0)
            
            if level in level_counts:
                level_counts[level] += 1
            else:
                level_counts[level] = 1

            if isinstance(node, LeaflessNode):
                children_areas = 0
                if node.children: 
                    for child in node.children:
                        queue.append((child, level + 1))
                        children_areas += child.area()
                    mean_area = children_areas / len(node.children)
                else:
                    mean_area = 0  
                if level in level_mean_areas:
                    level_mean_areas[level].append(mean_area)
                else:
                    level_mean_areas[level] = [mean_area]

        height = max(level_counts.keys()) + 1
        print(f"Height of the RTree: {height}")
        for level, count in level_counts.items():
            mean_area = sum(level_mean_areas[level]) / len(level_mean_areas[level]) if level in level_mean_areas else 0
           
            if height == 1:
                print(f"Level {level+1}: {count} node, Mean area: {mean_area}")
            else:
                print(f"Level {level+1}: {count} nodes, Mean area: {mean_area}")

                
def bulk_load(entries,block_size):
    
    entries.sort(key=lambda entry:entry.rect.low.x)

    max_nodes = floor(block_size/36)
    max_entries = floor(block_size/20)
    
    leafs = ceil(len(entries)/max_nodes)
    
    vertical = ceil(sqrt(leafs))
    
    slices = [entries[i:i + (vertical*max_entries)] for i in range(0, len(entries), vertical*max_entries)]
    
    for slice in slices:
        slice.sort(key=lambda entry: entry.rect.low.y)

    rtree = RTree(max_nodes=max_nodes)
    
    for  group in slices:
        for i in range(0,len(group),max_entries):
            entry_set = set(group[i:i+max_entries])
            leaf_node = LeafNode(id=i, entries=entry_set)
            rtree.insert_leaf_node(leaf_node)
    return rtree


if not len(argv) == 2:
    print("Need a file to read the data!")
    exit() 

path = argv[1]
file = open(path,"r")

total_objects = int(file.readline())
count = 1

entries = []

for line in file:

    cordinates = line.split()
    x = float(cordinates[0])
    y = float(cordinates[1])

    point = Point(count,x,y)
    rect=Rect(low=point, high=point)
    entry = EntryBlock(id=count, rect=rect )
    entry.points.append(point)
    entries.append(entry)
    count +=1
    

block_size = 1024


rtree = bulk_load(entries,block_size)

rtree.add_starting_nodes()
rtree.tree_stats()
rtree.write_tree("./Rtree.txt")

file.close

end_time = time.time()
elapsed_time = end_time - start_time
print("Execution time:", elapsed_time, "seconds")

# Konstatninos Papantoniu, 4769

from math import sqrt
from sys import argv
import time

start_time = time.time()
tree_path = argv[1]
q = tuple((float(argv[2]),float(argv[3])))
k = int(argv[4])

tree_file = open(tree_path,"r")

data = []
root = tree_file.readline().strip()

for line in tree_file:

   data.append(line.strip().split(','))
   
tree_file.close()

nodes_id = [int(row[0]) for row in data]
nums_children = [int(row[1]) for row in data] 

flags = [int(row[2]) for row in data]

children_data = [row[3:] for row in data]
rtree = {}

for node_id, num_children, flag, child_data in zip(nodes_id, nums_children, flags, children_data):
   data = []
   point = []
   children = []
   entry_id = []
   
   if flag == 0:
      for i in range(0,len(child_data),3):
         entry_id = int(child_data[i].replace('(',''))
         point_x = float(child_data[i+1].replace('(',''))
         point_y = float(child_data[i+2].replace('))',''))
         children.append((entry_id,(point_x,point_y)))
   else:
      for i in range(0,len(child_data),5):
         entry_id = int(child_data[i].replace('(',''))
         min_x = float(child_data[i+1].replace('[',''))
         min_y = float(child_data[i+2])
         max_x = float(child_data[i+3])
         max_y = float(child_data[i+4].replace('])',''))
         children.append((entry_id,(min_x,min_y,max_x,max_y)))
         
         
   rtree[node_id] = {
      'num_children': num_children,
      'flag': flag,
      'children': children
   }    


def INNS(q,rtree,k):
   
   sorted_keys = sorted(rtree.keys(), reverse=True)
   root_key, root_value = next(iter((key, rtree[key]) for key in sorted_keys))
   
   Q = [(mindist(q,root_value['children'][0][1]),root_key,root_value)]
   nearest_neighbors = []
   
   visited = set()
   while Q :

      distance,node_id,node = min(Q,key=lambda x:x[0])    
      flag = node['flag']
      Q.remove((distance,node_id,node))

      if flag == 0:
        for child_name,child_point in node['children']:
           dist_from_point = sqrt((q[0]-child_point[0])**2 + (q[1] - child_point[1])**2)
           nearest_neighbors.append((child_name,dist_from_point))
          
      else:
         if node_id not in visited:
            visited.add(node_id)
            min_distance = float('inf') 
            min_distance_node = None  
            for child_name, child_value in node['children']:
                  distance_to_child = mindist(q, child_value)
                  if distance_to_child < min_distance:
                     min_distance = distance_to_child

                     min_distance_node = rtree[child_name]
            
            Q.append((min_distance, child_name, min_distance_node)) 
   result = sorted(nearest_neighbors, key=lambda x:x[1])
   return result[:k], result[k:k+1] , result[k+1:k+2]

def mindist(q,mbr):
   mbr_min_x = mbr[0]
   mbr_min_y = mbr[1]
   mbr_max_x = mbr[2]
   mbr_max_y = mbr[3]
   qx = q[0]
   qy = q[1]
   if mbr_min_x<=qx<=mbr_max_x and mbr_min_y<=qy<=mbr_max_y:
      return 0
   dx = min(abs(mbr_max_x - qx),abs(mbr_min_x - qx))
   dy = max(abs(mbr_max_y - qy), abs(mbr_min_y - qy))

   return sqrt(dx**2+dy**2)

   
res = INNS(q,rtree,k)

r1,r2,r3 = res

for r in r1:
   print(r)
print('-'*70)
# for r in r2:
print(r2[0])
print('-'*70)
# for r in r3:
print(r3[0])

end_time = time.time()
elapsed_time = end_time - start_time
print("Execution time:", elapsed_time, "seconds")

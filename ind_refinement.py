from graph_io import load_graph, write_dot
import sys

# Print a dot file with filename and graph
def print_dot(filename, G):
    with open(filename, 'w') as f:
        write_dot(G, f)

# Update the partitions dictionary 'partitions'
# Key: the color of the partitions
# Value: the vertex that needs to be added to the partition
def update_partition_dict(partitions, key, value):
     if key in partitions:
        partitions[key].append(value)
     else:
        partitions[key] = [value]

# Get the neighbours of Vertex v as a sorted list of colors
def get_neighbourhood(v: "Vertex") -> list(int):  
    result = []
    for n in v.neighbours:
        result.append(n.colornum)
    result.sort()
    return result

# Check whether a neighbourhood n exists in the list lst
# With lst = [(color, vertex, neighbourhood)]
# Returns the color of -1 if not found
def get_color_of_neighbourhood(n, lst):
    for i in range(len(lst)):
        if lst[i][2] == n:
            return lst[i][0]
    return -1

# Refine and verify all graphs in a graph list
def refine_all(L):
    for i in range(0, len(L[0])):
        for j in range(i + 1, len(L[0])):
            print(i, "=", j, "?")
            refine_colors(L[0][i], L[0][j])
            verify_colors(L[0][i], L[0][j])

# Make a dictionary with partitions of graphs G and H
def get_partitions(G, H):
    result = dict()
    # graph G
    for vG in G.vertices:
        update_partitions_dict(result, vG.colornum, vG)
    # graph H
    for vH in H.vertices:
        update_partitions_dict(result, vH.colornum, vH)
    return result

# Get the smallest color class in the given partitions dict
def get_smallest_colorclass(partitions):
    size = float("inf")
    smallest = None
    for p in partitions.items():
        if len(p) < size:
            size = len(p)
            smallest = p
    return smallest

# Calculate the coarsest stable coloring on graphs G and H
# Returns (int, dict)
# With int: 0: unbalanced, 1: bijection, 2: stable but no bijection
# And dict: resulting partition dict
def coarsest_stable_coloring(G, H):
    # Calculate the number of vertices and check whether the graphs
    # have the same number of vertices
    vertex_count = len(G.vertices)
    if not(vertex_count == len(H.vertices)):
        print("No (vertex count is not the same)")
        return (0, dict())
    # Retrieve the partitions of the graphs
    partitions = get_partitions(G, H)
    last_key = None
    # Number of loops equals number of vertices
    for v in range(vertex_count):
        for p in list(partitions.keys()):
            partition = partitions[p]
            tmp = []  # list of (color, vertex, neighbourhood)-tuples
            n_u = get_neighbourhood(partition[0])
            for i in range(1, len(partition)):
                n_v = get_neighbourhood(partition[i])
                if not n_u == n_v:
                    color = get_color_of_neighbourhood(n_v, tmp)
                    if color >= 0:
                        tmp.append((color, partition[i], n_v))
                    else:
                        tmp.append((last_color, partition[i], n_v))
                        last_color += 1
            # Update the dictionary and the vertices
            for t in tmp:
                partition.remove(t[1])
                if t[0] in partitions:
                    partitions[t[0]].append(t[1])
                else:
                    partitions[t[0]] = [t[1]]
                t[1].colornum = t[0]
            if len(partition) % 2 != 0:
                return (0, partitions) #No
            last_key = p
        if len(partitions) == vertex_count:
            return (1, partitions) #Yes
    for p in range(last_key + 1, len(partitions)):
        if len(partitions[p]) % 2 != 0:
            return (0, partitions) #No
    return (2, partitions) #Maybe

# Count the number of isomorphisms with graphs G and H
def count_isomorphisms(G, H):
    original_G = G.deepcopy()
    original_H = H.deepcopy()
    (result, partitions) = coarsest_stable_coloring(G, H)
    # Coarsest stable coloring is unbalanced or a bijection
    if result = 0: #unbalanced
        G = original_G
        H = original_H
        return 0
    if result = 1:
        return 1
    # Coarsest stable coloring is stable but not a bijection
    else:
        # Get last color
        last_color = 0
        for p in partitions:
            if p > last_color:
                last_color = p
        # Choose a color class C
        C = get_smallest_colorclass(partitions)
        # Choose x in C union V(G)
        x = None
        for vertex in C:
            if (vertex.graph == G):
                x = vertex
                break
        num = 0
        # For all y in C union V(H)
        for y in C:
            if (y.graph == H):
                #   num = num + count_isomorphisms(G + x, H + x)
                old_color = x.colornum
                x.colornum = last_color + 1
                y.colornum = last_color + 1
                num = num + count_isomorphisms(G, H)
                x.colornum = old_color
        return num

def refine_colors(G, H):
    vertex_count = len(G)
    # Create a disjoint union of the first two graphs
    I = G + H

    partitions = {}
    last_color = 0
    # Initially color the vertices based on degree
    for v in I.vertices:
        v.colornum = v.degree
        if last_color < v.degree:
            last_color = v.degree
        if v.degree in partitions:
            partitions[v.degree].append(v)
        else:
            partitions[v.degree] = [v]

    last_color += 1

    # Check first if there already is an unbalanced coloring
    for p in partitions:
        if len(partitions[p]) % 2 != 0:
            print("No")
            return
    
    result = count_isomorphisms(G, H)
    if result == 0:
        print ("No")
        return
    else:
        print ("Yes: " + str(result))
        return
    
    
def verify_colors(G, H):
    for G_v in G.vertices:
        for H_v in H.vertices:
            if G_v.colornum == H_v.colornum:
                if not get_neighbourhood(G_v) == get_neighbourhood(H_v):
                    print (False)
                    return False
    print (True)
    return True

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        graph_list = load_graph(f, read_list=True)
    refine_all(graph_list)

from graph_io import load_graph, write_dot
import sys

# Print a dot file with filename and graph
def print_dot(filename, G):
    with open(filename, 'w') as f:
        write_dot(G, f)


def get_neighbourhood(v):  ### Optimisation: store neighbourhood color list in vertex class ???
    result = []
    for n in v.neighbours:
        result.append(n.colornum)
    result.sort()
    return result


def get_colour_of_neighbourhood(n, lst):
    for i in range(len(lst)):
        if lst[i][2] == n:
            return lst[i][0]
    return -1

def create_partition_dictionary(G): 
    result = dict()
    for v in G.vertices:
        if v.colornum in result:
            result[v.colornum].append(v)
        else:
            result[v.colornum] = [v]
    return result

def get_smallest_partition(partitions):
    size = float("inf")
    smallest = None
    for p in partitions.items():
        if len(p) < size:
            size = len(p)
            smallest = p
    return smallest
            
def refine_all(L):
    for i in range(0, len(L[0])):
        for j in range(i + 1, len(L[0])):
            print(i, "=", j, "?")
            refine_colors(L[0][i], L[0][j])
            verify_colors(L[0][i], L[0][j])


# Initially color the vertices based on degree
def initial_coloring(I, partitions):
    last_colour = 0
    for v in I.vertices:
        v.colornum = v.degree
        if last_colour < v.degree:
            last_colour = v.degree
        if v.degree in partitions:
            partitions[v.degree].append(v)
        else:
            partitions[v.degree] = [v]
    return last_colour

def count_isomorphisms(vertex_count, partitions, last_colour, G):
    last_key = None
    # Number of loops equals number of vertices
    for v in range(vertex_count):
        for p in list(partitions.keys()):
            partition = partitions[p]
            tmp = []  # list of (colour, vertex, neighbourhood)-tuples
            n_u = get_neighbourhood(partition[0])
            for i in range(1, len(partition)):
                n_v = get_neighbourhood(partition[i])
                if not n_u == n_v:
                    colour = get_colour_of_neighbourhood(n_v, tmp)
                    if colour >= 0:
                        tmp.append((colour, partition[i], n_v))
                    else:
                        tmp.append((last_colour, partition[i], n_v))
                        last_colour += 1
            # Update the dictionary and the vertices
            for t in tmp:
                partition.remove(t[1])
                if t[0] in partitions:
                    partitions[t[0]].append(t[1])
                else:
                    partitions[t[0]] = [t[1]]
                t[1].colornum = t[0]
            if len(partition) % 2 != 0:
                return 0
            last_key = p
        if len(partitions) == vertex_count:
            return 1
    for p in range(last_key + 1, len(partitions)):
        if len(partitions[p]) % 2 != 0:
            return 0
    
    H = G.deepcopy()
    new_partitions = create_partition_dictionary(H)
    smallest = get_smallest_partition(new_partitions)
    # Create new colour
    smallest[1][0].colornum = last_colour + 1
    new_partitions[last_colour + 1] = smallest[1][0]
    smallest[1].remove(smallest[1][0])   
    return count_isomorphisms(vertex_count, new_partitions, last_colour + 1, H)

def refine_colors(G, H):
    vertex_count = len(G)
    # Create a disjoint union of the first two graphs
    I = G + H

    partitions = {}
    last_colour = initial_coloring(I, partitions) + 1

    # Check first if there already is an unbalanced coloring
    for p in partitions:
        if len(partitions[p]) % 2 != 0:
            print("No")
            return
    result = count_isomorphisms(vertex_count, partitions, last_colour, I)
    if result == 0:
        print("No")
        return
    else:
        print("Yes: " + str(result))
        return
    
def verify_colors(G, H):
    for G_v in G.vertices:
        for H_v in H.vertices:
            if G_v.colornum == H_v.colornum:
                if not get_neighbourhood(G_v) == get_neighbourhood(H_v):
                    print ("Yes")
                    return False
    print ("No")
    return True

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        graph_list = load_graph(f, read_list=True)
    refine_all(graph_list)

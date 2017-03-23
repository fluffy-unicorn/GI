from graph_io import load_graph, write_dot
import sys, time

# Magic numbers
NO = 0
YES = 1
MAYBE = 2
COLOR = 0
VERTEX = 1
NEIGHBOURS = 2
UNKNOWN = -1
VERTICES = 1

def print_dot(filename, G):
    """
    Print a dot file with filename and graph
    :param filename: The file
    :param G: The graph
    """
    with open(filename, 'w') as f:
        write_dot(G, f)


def update_partitions_dict(partitions, key, value):
    """
    Update the partitions dictionary 'partitions'
    :param partitions: The dictionary 'partitions'
    :param key: The color of the partitions
    :param value: the vertex that needs to be added to the partition
    """
    if key in partitions:
        partitions[key].append(value)
    else:
        partitions[key] = [value]


def get_neighbourhood(v):  
    """
    Get a sorted list of all the colors of all the neighbours
    :param v: The vertex
    :return: The sorted list
    """
    result = []
    for n in v.neighbours:
        result.append(n.colornum)
    result.sort()
    return result


def get_color_of_neighbourhood(n, lst):
    """
    Get the color for which the same colored neighbourhood is already in the list
    :param n: List of neighbour colors
    :param lst: The 'update-list' with the following tuples: (color, vertex, neighbourhood)
    :return: the found color or -1
    """
    for i in range(len(lst)):
        if lst[i][NEIGHBOURS] == n:
            return lst[i][COLOR]
    return UNKNOWN


def refine_all(L):
    """
    Refine and verify all graphs in a list from the .grl file
    :param L: The list of graphs
    """
    alg_time = 0
    for i in range(0, len(L[0])):
        for j in range(i + 1, len(L[0])):
            # Starting the algorithm on (i, j)
            start_alg = time.time()
            isomorphisms = refine_colors(L[0][i], L[0][j])
            end_alg = time.time()
            alg_time += end_alg - start_alg
            # Starting the verifier on (i, j)
            verified = verify_colors(L[0][i], L[0][j])
            if (isomorphisms > 0):
                print("("+str(i)+","+str(j)+") "+str(isomorphisms)+" ["+str(verified)+"]")
    print("Elapsed time (algorithm): " + str(int(alg_time*1000)) + " ms")

            

def get_partitions(G, H):
    """
    Make a dictionary with color classes of graphs G and H
    :param G: The graph G
    :param H: The graph H
    :return: A dictionary with color classes
    """
    result = dict()
    # graph G
    for vG in G.vertices:
        update_partitions_dict(result, vG.colornum, vG)
    # graph H
    for vH in H.vertices:
        update_partitions_dict(result, vH.colornum, vH)
    return result


def get_smallest_colorclass(partitions):
    """
    Returns the smallest color class in the given 'partitions' dictionary
    :param partitions: The dictionary
    :return: The smallest color class
    """
    size = float("inf") # Latest known smallest size of a color class
    smallest = None
    for p in partitions.items():
        if len(p) < size: # Only update if color class size is smaller than known upto now
            size = len(p)
            smallest = p
    return smallest

def get_last_color(partitions):
    """
    Returns the last used color class in the partitions dictionary
    :param partitions: The dictionary
    :return: The last used color class
    """
    last_color = 0
    for p in partitions:
        if p > last_color:
            last_color = p
    return last_color

def initial_coloring(G, partitions):
    """
    Calculates the initial coloring based on the degrees of the vertices on a graph
    :param G: The graph
    :param partitions: The partitions dictionary to be used
    :return: The last color used in the coloring
    """
    last_color = 0
    for v in G.vertices:
        v.colornum = v.degree
        if last_color < v.degree:
            last_color = v.degree
        if v.degree in partitions:
            partitions[v.degree].append(v)
        else:
            partitions[v.degree] = [v]
    return last_color

def coarsest_stable_coloring(G, H):
    """
    Calculates the coarsest stable coloring on graphs G and H
    :param G: The graph G
    :param H: The graph H
    :return: Tuple (int, dict)
    With int -> 0: unbalanced, 1: bijection, 2: stable but no bijection
    and dict: resulting partitions dictionary
    """
    # Calculate the number of vertices and check whether the graphs
    # have the same number of vertices
    vertex_count = len(G.vertices)
    if not(vertex_count == len(H.vertices)):
        return (NO, dict())

    # Retrieve the partitions of the graphs
    partitions = get_partitions(G, H)
    # Last key is the latest color class that is check whether it has
    # an even or and odd number of vertices in it (odd number means unbalanced)
    last_key = None
    last_color = get_last_color(partitions)
    # Number of loops equals number of vertices
    for v in range(vertex_count):
        for p in list(partitions.keys()):
            color_class = partitions[p]
            update_list = []  # list of (color, vertex, neighbourhood)-tuples
            n_u = get_neighbourhood(color_class[0])
            for i in range(1, len(color_class)):
                n_v = get_neighbourhood(color_class[i])
                if not n_u == n_v:
                    color = get_color_of_neighbourhood(n_v, update_list)
                    if color != UNKNOWN:
                        update_list.append((color, color_class[i], n_v))
                    else:
                        update_list.append((last_color, color_class[i], n_v))
                        last_color += 1
            # Update the dictionary and the vertices
            for t in update_list:
                color_class.remove(t[VERTEX])
                if t[COLOR] in partitions:
                    partitions[t[COLOR]].append(t[VERTEX])
                else:
                    partitions[t[COLOR]] = [t[VERTEX]]
                t[VERTEX].colornum = t[COLOR]
            if len(color_class) % 2 != 0: # Check for unbalanced coloring
                return (NO, partitions) 
            last_key = p
        if len(partitions) == vertex_count: # Check for bijection
            return (YES, partitions)
    # Check the resulting color classes for an unbalanced coloring
    for p in range(last_key + 1, len(partitions)):
        if len(partitions[p]) % 2 != 0:
            return (NO, partitions)
    return (MAYBE, partitions)


def count_isomorphisms(G, H):
    """
    Count the number of isomorphisms with graph G and H
    :param G: The graph G
    :param H: The graph H
    :return: The number of isomorphisms
    """
    # Keep a copy of the original graphs (for backtracking reasons)
    # Not used yet...
    original_G = G.deepcopy()
    original_H = H.deepcopy()
    (result, partitions) = coarsest_stable_coloring(G, H)
    # Coarsest stable coloring is unbalanced or a bijection
    if result == NO:
        return NO
    elif result == YES:
        return YES
    # Coarsest stable coloring is stable but not a bijection
    else:
        last_color = get_last_color(partitions)
        # Choose a color class C
        C = get_smallest_colorclass(partitions)[VERTICES]
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
                # num = num + count_isomorphisms(G + x, H + x)
                old_color = x.colornum
                x.colornum = last_color + 1
                y.colornum = last_color + 1
                num += count_isomorphisms(G, H)
                x.colornum = old_color
        return num

def refine_colors(G, H):
    """
    Refine the colors on graphs G and H
    :param G: The graph G
    :param H: The graph H   
    :return: The number of isomorphisms
    """
    partitions = {}
    last_color = initial_coloring(G, partitions)
    last_color = initial_coloring(H, partitions)
    last_color += 1

    # Check first if there already is an unbalanced coloring
    for p in partitions:
        if len(partitions[p]) % 2 != 0:
            return 0
    
    return count_isomorphisms(G, H)
    
    
def verify_colors(G, H):
    """
    Verify the colors of graph G and H
    :param G: The graph G
    :param H: The graph H
    :return: Whether the resulting coloring is a bijection or not
    """
    for G_v in G.vertices:
        for H_v in H.vertices:
            if G_v.colornum == H_v.colornum:
                if not get_neighbourhood(G_v) == get_neighbourhood(H_v):
                    return False
    return True

if __name__ == "__main__":
    """
    Main function
    :param 1: The .grl-file
    """
    start = time.time()
    with open(sys.argv[1]) as f:
        graph_list = load_graph(f, read_list=True)
    refine_all(graph_list)
    end = time.time()
    print("Elapsed time (total): " + str(int((end-start)*1000)) + " ms")

from graph_io import load_graph, write_dot
import random
import sys
import time

# Magic numbers
NO = 0
YES = 1
MAYBE = 2
COLOR = 0
VERTEX = 1
NEIGHBOURS = 2
UNKNOWN = -1
VERTICES = 1
SMALLEST = 0
BIGGEST = 1
RANDOM = 2
DEGREE = 0
FLAT = 1

def add_vertex_to_partitions(partitions, key, value):
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


def get_copied_vertex(original, copy, vertex):
    """
    Get a sorted list of all the colors of all the neighbours
    :param original: The original graph
    :param copy: Copy of the graph
    :return: The sorted list
    """
    index = original.vertices.index(vertex)
    return copy.vertices[index]


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


def refine_all(L, colorclass_choice, coloring_choice, fast):
    """
    Refine and verify all graphs in a list from the .grl file
    :param L: The list of graphs
    """
    alg_time = 0
    for i in range(0, len(L[0])):
        for j in range(i + 1, len(L[0])):
            # Starting the algorithm on (i, j)
            start_alg = time.time()
            G = L[0][i]
            H = L[0][j]
            if coloring_choice == DEGREE:
                initial_coloring(G)
                initial_coloring(H)
            else:
                initial_flat_coloring(G)
                initial_flat_coloring(H)
            isomorphisms = find_isomorphisms(G, H, colorclass_choice, fast)
            end_alg = time.time()
            alg_time += end_alg - start_alg
            #print("("+str(i)+","+str(j)+") "+str(isomorphisms))
    #print("Elapsed time (algorithm): " + str(int(alg_time*1000)) + " ms")


def count_automorphisms(G):
    alg_time = 0
    # Starting the algorithm on (i, j)
    start_alg = time.time()
    initial_coloring(G)
    isomorphisms = find_isomorphisms(G, G)
    end_alg = time.time()
    alg_time += end_alg - start_alg
    #print("G has " + str(isomorphisms) + " automorphisms")
    #print("Elapsed time (algorithm): " + str(int(alg_time * 1000)) + " ms")


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
        add_vertex_to_partitions(result, vG.colornum, vG)
    # graph H
    for vH in H.vertices:
        add_vertex_to_partitions(result, vH.colornum, vH)
    return result


def get_smallest_colorclass(partitions):
    """
    Returns the smallest color class in the given 'partitions' dictionary
    :param partitions: The dictionary
    :return: The smallest color class
    """
    size = float("inf")  # Latest known smallest size of a color class
    smallest = None
    for p in partitions.values():
        if size > len(p) >= 4:  # Only update if color class size is smaller than known upto now
            size = len(p)
            smallest = p
    return smallest

def get_biggest_colorclass(partitions):
    size = 0
    biggest = None
    for p in partitions.values():
        if size < len(p) >= 4:
            size = len(p)
            biggest = p
    return biggest

def get_random_colorclass(partitions):
    partition = random.choice(list(partitions.values()))
    while len(partition) < 4:
        partition = random.choice(list(partitions.values()))
    return partition

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


def initial_coloring(G):
    """
    Calculates the initial coloring based on the degrees of the vertices on a graph
    :param G: The graph
    """
    for v in G.vertices:
        v.colornum = v.degree

def initial_flat_coloring(G):
    for v in G.vertices:
        v.colornum = 0

def coarsest_stable_coloring(G, H, fast):
    """
    Calculates the coarsest stable coloring on graphs G and H
    :param G: The graph G
    :param H: The graph H
    :return: Tuple (int, dict)
    With int -> 0: unbalanced, 1: bijection, 2: stable but no bijection
    and dict: resulting partitions dictionary
    """

    # Retrieve the partitions of the graphs
    partitions = get_partitions(G, H)
    # Last key is the latest color class that is check whether it has
    # an even or and odd number of vertices in it (odd number means unbalanced)
    last_key = None
    last_color = get_last_color(partitions)
    # Number of loops equals number of vertices
    for v in range(len(G.vertices)):
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
            if fast and len(color_class) % 2 != 0: # Check for unbalanced coloring
                return (NO, partitions) 
            last_key = p
        if fast and len(partitions) == len(G.vertices): # Check for bijection
            return (YES, partitions)
    # Check the resulting color classes for an unbalanced coloring
    for p in range(last_key + 1, len(partitions)):
        if len(partitions[p]) % 2 != 0:
            return (NO, partitions)
    if not fast:
        if len(partitions) == len(G.vertices): # Check for bijection
            return (YES, partitions)
    return (MAYBE, partitions)


def find_isomorphisms(G, H, choice, fast):
    """
    Wrapper function to call the recursive count_isomorphisms(). Checks precondition.
    :param G: The graph G
    :param H: The graph H
    :return: The number of isomorphisms
    """
    if fast and len(G.vertices) != len(H.vertices):
        return NO
    return count_isomorphisms(G, H, [], [], choice, fast)


def count_isomorphisms(G, H, D, I, choice, fast):
    """
    Count the number of isomorphisms with graph G and H
    :param G: The graph G
    :param H: The graph H
    :return: The number of isomorphisms
    """

    color = get_last_color(get_partitions(G, H)) + 1

    for vertex in D+I:
        vertex.colornum = color

    (result, partitions) = coarsest_stable_coloring(G, H, fast)

    for p in partitions:
        if len(partitions[p]) % 2 != 0:
            return NO

    # Coarsest stable coloring is unbalanced or a bijection
    if result == NO:
        return NO
    elif result == YES:
        return YES
    # Coarsest stable coloring is stable but not a bijection
    else:
        partitions = get_partitions(G, H)
        # Choose a color class C
        if choice == SMALLEST:
            C = get_smallest_colorclass(partitions)  # C moet >= 4 zijn
        elif choice == BIGGEST:
            C = get_biggest_colorclass(partitions)
        else:
            C = get_random_colorclass(partitions)            
        # Choose x in C union V(G)
        x = None
        for vertex in C:
            if vertex.graph == G:
                x = vertex
                break
        if x == None:
            return NO 
        num = 0
        # For all y in C union V(H)
        for y in C:
            if y.graph == H:
                # num = num + count_isomorphisms(G + x, H + x)
                copy_g = G.deepcopy()
                copy_h = H.deepcopy()
                copy_x = get_copied_vertex(G, copy_g, x)
                copy_y = get_copied_vertex(H, copy_h, y)
                num = num + count_isomorphisms(copy_g, copy_h, [copy_x], [copy_y], choice, fast)
        return num


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
    USAGE = "Usage:\npython3 " + str(sys.argv[0]) + " [filename] [biggest|smallest|random] [flat|degree]"
    start = time.time()
    with open(sys.argv[1]) as f:
        if(str(sys.argv[1]).endswith(".grl")):
            graph_list = load_graph(f, read_list=True)
            if(sys.argv[2] == "biggest"):
                colorclass_choice = BIGGEST
            elif(sys.argv[2] == "random"):
                colorclass_choice = RANDOM
            elif(sys.argv[2] == "smallest"):
                colorclass_choice = SMALLEST
            else:
                print (USAGE)
                exit();
            if(sys.argv[3] == "flat"):
                coloring_choice = FLAT
            elif(sys.argv[3] == "degree"):
                coloring_choice = DEGREE
            else:
                print (USAGE)
                exit();
            if(sys.argv[4] == "fast"):
                fast = True
            elif(sys.argv[4] == "slow"):
                fast = False
            else:
                print (USAGE)
                exit();
            refine_all(graph_list, colorclass_choice, coloring_choice, fast)
        else:
            graph = load_graph(f, read_list=False)
            count_automorphisms(graph)

    end = time.time()
    print(int((end-start)*1000))

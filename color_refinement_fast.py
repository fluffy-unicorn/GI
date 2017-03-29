from collections import deque

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


def get_neighbourhood_colors(v):
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
            G = L[0][i]
            H = L[0][j]
            initial_coloring(G)
            initial_coloring(H)
            isomorphisms = find_isomorphisms(G, H)
            end_alg = time.time()
            alg_time += end_alg - start_alg
            # Starting the verifier on (i, j)
            verified = verify_colors(L[0][i], L[0][j])
            print("("+str(i)+","+str(j)+") "+str(isomorphisms))
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


def coarsest_stable_coloring(G, H):
    """
    Calculates the coarsest stable coloring on graphs G and H
    :param G: The graph G
    :param H: The graph H
    :return: Tuple (int, dict)
    With int -> 0: unbalanced, 1: bijection, 2: stable but no bijection
    and dict: resulting partitions dictionary
    """
    queue = deque()
    visited = []
    partitions = get_partitions(G, H)
    # Kies een partitie
    color_class = list(partitions.keys())[0]
    queue.append(color_class)

    while len(queue) > 0:
        C = queue.popleft()
        visited.append(C)
        no_of_neighbours = dict()
        D = dict()
        for v in partitions[C]:
            for n in v.neighbours:
                if n.colornum == C:
                    break
                elif n in no_of_neighbours.keys():
                    no_of_neighbours[n] += 1
                else:
                    no_of_neighbours[n] = 1
        # Make sets Di with number of vertices with i neighbours in C
        for v in (G + H).vertices:
            if not(v in no_of_neighbours.keys()):
                if 0 in D.keys():
                    D[0].append(v)
                else:
                    D[0] = [v]
            else:
                if no_of_neighbours[v] in D.keys():
                    D[no_of_neighbours[v]].append(v)
                else:
                    D[no_of_neighbours[v]] = [v]
        # Forall C' in partitions\C and len(C_prime) >= 4
        for C_prime in list(partitions.keys()):
            if C_prime != C and len(partitions[C_prime]) >= 4:
                C_prime_i = dict()
                for v in partitions[C_prime]:
                    for i in D.keys():
                        if v in D[i]:
                            if i in C_prime_i.keys():                    
                                C_prime_i[i].append(v)
                            else:
                                C_prime_i[i] = [v]
                last_color = get_last_color(partitions)
                # Add all C_prime_i to partitions
                first = True
                for c in C_prime_i.values():
                    if len(C_prime_i) == 1:
                        if C_prime not in queue and C_prime not in visited:
                            queue.append(C_prime)
                    else:
                        if first:
                            partitions[C_prime] = c
                            first = False
                        else:
                            partitions[last_color + 1] = c
                            queue.append(last_color + 1)
                            last_color += 1

    result = MAYBE
    for p in partitions:
        if len(partitions[p]) % 2 != 0:
            result = NO
    if len(partitions) == len(G.vertices):
        result = YES
    return (result, partitions)          
            

def find_isomorphisms(G, H):
    """
    Wrapper function to call the recursive count_isomorphisms(). Checks precondition.
    :param G: The graph G
    :param H: The graph H
    :return: The number of isomorphisms
    """
    if not (len(G.vertices) == len(H.vertices)):
        return NO
    return count_isomorphisms(G, H, [], [])


def count_isomorphisms(G, H, D, I):
    """
    Count the number of isomorphisms with graph G and H
    :param G: The graph G
    :param H: The graph H
    :return: The number of isomorphisms
    """

    color = get_last_color(get_partitions(G, H)) + 1

    for vertex in D+I:
        vertex.colornum = color

    (result, partitions) = coarsest_stable_coloring(G, H)

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
        return MAYBE


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
                if not get_neighbourhood_colors(G_v) == get_neighbourhood_colors(H_v):
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

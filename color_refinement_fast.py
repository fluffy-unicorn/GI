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
            # verified = verify_colors(L[0][i], L[0][j])
            print("(" + str(i) + "," + str(j) + ") " + str(isomorphisms))
    print("Elapsed time (algorithm): " + str(int(alg_time * 1000)) + " ms")


def get_partition(G, H):
    """
    Make a dictionary with color classes of graphs G and H
    :param G: The graph G
    :param H: The graph H
    :return: A dictionary with color classes
    """
    result = dict()
    # graph G
    for vG in G.vertices:
        insert_into_dictionary(result, vG.colornum, vG)
    # graph H
    for vH in H.vertices:
        insert_into_dictionary(result, vH.colornum, vH)
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
    and dict: resulting partition dictionary
    """
    queue = deque()
    visited_color_class_ids = []
    partition = get_partition(G, H)
    # Kies een partitie
    color_class_id = list(partition.keys())[0]
    queue.append(color_class_id)

    while len(queue) > 0:
        C_id = queue.popleft()
        visited_color_class_ids.append(C_id)
        color_class = partition[C_id]

        # Make sets Di = vertices with i neighbours in C (invert the no_of_neighbours dictionary)
        no_of_neighbours = count_incidents_with_color_class(color_class)
        D = dict()
        for v in G.vertices + H.vertices:
            v_neighbours = no_of_neighbours[v] if v in no_of_neighbours.keys() else 0  # ternary assignment
            insert_into_dictionary(D, v_neighbours, v)

        # Forall C' in partition\C and len(C_prime) >= 4
        for C_prime in list(partition.keys()):
            if C_prime != C_id:
                if len(partition[C_prime]) >= 4:
                    C_prime_i = dict()
                    for i in D.keys():
                        for v in set(partition[C_prime]).intersection(D[i]):
                            insert_into_dictionary(C_prime_i, i, v)

                    if len(C_prime_i) == 1:
                        enqueue_once(C_prime, queue, visited_color_class_ids)
                        continue
                    last_color = get_last_color(partition)
                    # Add all C_prime_i to partition
                    first = True
                    smallest = None
                    smallest_color = None
                    for c in C_prime_i.values():
                        if len(c) & 0x1 == 1:  # Check if last bit is 1 (== number is odd)
                            return NO, partition
                        if C_prime in queue:
                            queue.remove(C_prime)
                        if C_prime in partition.keys():
                            partition.pop(C_prime)
                        last_color += 1
                        partition[last_color] = c
                        if smallest is None or len(c) < len(smallest):
                            smallest_color = last_color
                            smallest = c
                    queue.append(smallest_color)
                else:
                    enqueue_once(C_prime, queue, visited_color_class_ids)
                if len(partition) == len(G.vertices):
                    return YES, partition

    result = MAYBE
    for p in partition:
        if len(partition[p]) % 2 != 0:
            result = NO
    if len(partition) == len(G.vertices):
        result = YES
    return (result, partition)


def count_incidents_with_color_class(color_class):
    no_of_neighbours = dict()
    for v in color_class:
        for n in v.neighbours:
            if n not in color_class:
                increment_dict_value(no_of_neighbours, n)
    return no_of_neighbours


def increment_dict_value(dictionary, key):
    if key in dictionary.keys():
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def insert_into_dictionary(dictionary, key, value):
    if key in dictionary.keys():
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def enqueue_once(color_class, queue, visited):
    if color_class not in queue and color_class not in visited:
        queue.append(color_class)


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

    color = get_last_color(get_partition(G, H)) + 1

    for vertex in D + I:
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
    print("Elapsed time (total): " + str(int((end - start) * 1000)) + " ms")

from graph_io import load_graph, write_dot
import sys
import helper

# Magic numbers
NO = 0
YES = 1
MAYBE = 2
COLOR = 0
VERTEX = 1
NEIGHBOURS = 2
UNKNOWN = -1
VERTICES = 1

# Global variables
count_isomorphism = True

def find_all_isomorphisms(G_list):
    """
    Refine and verify all graphs in a list from the .grl file
    :param G_list: The list of graphs
    """
    global count_isomorphism
    count_isomorphism = False
    for i in range(0, len(G_list[0])):
        for j in range(i + 1, len(G_list[0])):
            G = G_list[0][i]
            H = G_list[0][j]
            initial_coloring(G)
            initial_coloring(H)
            isomorphisms = find_isomorphisms(G, H)
            if isomorphisms == 1:
                print("["+str(i)+","+str(j)+"] ")


def count_all_automorphisms(G_list):
    """
    Count all the automorphisms of the graphs in the graph list
    :param G_list: The list of graphs
    """
    for i in range(0, len(G_list[0])):
        count_automorphisms(G_list[0][i], i)


def count_automorphisms(G, name):
    """
    Count the number of automorphisms of a graph
    :param G: The graph G
    :param name: The name of the graph
    """
    initial_coloring(G)
    isomorphisms = find_isomorphisms(G, G.deepcopy())
    print("(" + str(name) + ") has " + str(isomorphisms) + " automorphisms")


def get_biggest_colorclass(partitions):
    """
    Returns the biggest color class in the given 'partitions' dictionary
    :param partitions: The dictionary
    :return: The biggest color class
    """
    size = 0
    biggest = None
    for p in partitions.values():
        if size < len(p) >= 4:
            size = len(p)
            biggest = p
    return biggest


def initial_coloring(G):
    """
    Calculates the initial coloring based on the degrees of the vertices on a graph
    :param G: The graph
    """
    for v in G.vertices:
        v.colornum = v.degree


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


def coarsest_stable_coloring(G, H):
    """
    Calculates the coarsest stable coloring on graphs G and H
    :param G: The graph G
    :param H: The graph H
    :return: Tuple (int, dict)
    With int -> 0: unbalanced, 1: bijection, 2: stable but no bijection
    and dict: resulting partitions dictionary
    """

    # Retrieve the partitions of the graphs
    partitions = helper.get_partitions(G, H)
    # Last key is the latest color class that is check whether it has
    # an even or and odd number of vertices in it (odd number means unbalanced)
    last_key = None
    last_color = helper.get_last_color(partitions)
    # Number of loops equals number of vertices
    for v in range(len(G.vertices)):
        for p in list(partitions.keys()):
            color_class = partitions[p]
            update_list = []  # list of (color, vertex, neighbourhood)-tuples
            n_u = helper.get_neighbourhood(color_class[0])
            for i in range(1, len(color_class)):
                n_v = helper.get_neighbourhood(color_class[i])
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
        if len(partitions) == len(G.vertices): # Check for bijection
            return (YES, partitions)
    # Check the resulting color classes for an unbalanced coloring
    for p in range(last_key + 1, len(partitions)):
        if len(partitions[p]) % 2 != 0:
            return (NO, partitions)
    return (MAYBE, partitions)


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
    global count_isomorphism
    color = helper.get_last_color(helper.get_partitions(G, H)) + 1

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
        # Choose a color class C
        C = get_biggest_colorclass(helper.get_partitions(G, H))
        # Choose x in C union V(G)
        x = None
        for vertex in C:
            if vertex.graph == G:
                x = vertex
                break
        if x == None: # C has an even sized partitions, but all vertices are in H
            return NO
        num = 0
        # For all y in C union V(H)
        for y in C:
            if y.graph == H:
                # num = num + count_isomorphisms(G + x, H + x)
                copy_g = G.deepcopy()
                copy_h = H.deepcopy()
                copy_x = helper.get_copied_vertex(G, copy_g, x)
                copy_y = helper.get_copied_vertex(H, copy_h, y)
                num = num + count_isomorphisms(copy_g, copy_h, [copy_x], [copy_y])
                if not(count_isomorphism) and num > 0:
                    return 1
        return num

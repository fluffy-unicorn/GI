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

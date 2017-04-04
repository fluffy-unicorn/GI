import sys
from graph_io import load_graph, write_dot

def print_dot(filename, G):
    """
    Print a dot file with filename and graph
    :param filename: The file
    :param G: The graph
    """
    with open(filename, 'w') as f:
        write_dot(G, f)

def print_all(basename, l):
    for i in range(len(l)):
        print_dot(basename + str(i) + ".dot", l[0][i])

if __name__ == "__main__":
    """
    Main function
    :param 1: The .grl-file
    """
    with open(sys.argv[1]) as f:
        if(str(sys.argv[1]).endswith(".grl")):
            graph_list = load_graph(f, read_list=True)
            print_all(str(sys.argv[1]).split('.grl')[0], graph_list)
        else:
            graph = load_graph(f, read_list=False)
            print_dot(str(sys.argv[1]).split('.gr')[0] + ".dot", graph)

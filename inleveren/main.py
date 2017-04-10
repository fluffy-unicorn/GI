import sys
from graph_io import load_graph, write_dot
from ind_refinement import find_all_isomorphisms, count_all_automorphisms, count_automorphisms

if __name__ == "__main__":
    """
    Main function
    :param 1: A .grl or .gr file for computing the isomorphism or automorphism problem
    :param 2: (Only with .grl files) -a for computing automorphisms and -i for computing isomorphisms
    """
    USAGE = "Usage: python3 " + sys.argv[0] + " [filename] <options>"
    OPTIONS = "options:\t-i or isomorphism\n\t\t-a or automorphisms"
    if len(sys.argv) < 2:
        print(USAGE)
        exit(-1)
    if (sys.argv[1].endswith(".grl")):
        # Graph list
        if sys.argv[2] == "-i" or sys.argv[2] == "isomorphism":
            # Find isomorphisms
            with open(sys.argv[1]) as f:
                graph_list = load_graph(f, read_list = True)
                find_all_isomorphisms(graph_list)
        elif sys.argv[2] == "-a" or sys.argv[2] == "automorphism":
            # Count automorphisms
            with open(sys.argv[1]) as f:
                graph_list = load_graph(f, read_list = True)
                count_all_automorphisms(graph_list)
        else:
            print(USAGE)
            print(OPTIONS)
            exit(-1)
    elif (sys.argv[1].endswith(".gr")):
        # Single graph
        with open(sys.argv[1]) as f:
            graph = load_graph(f)
            count_automorphisms(graph, 0)
    else:
        print(USAGE)
        exit(-1)

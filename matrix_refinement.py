import time
import sys
from graph_io import load_graph
def find_all_isomorphims(graph_list):
    for i in range(0, len(graph_list[0])):
        graph_list[0][i].matrix = graph_list[0][i].to_matrix()
    for i in range(0, len(graph_list[0])):
        for j in range(i + 1, len(graph_list[0])):
            print((i,j), find_isomorphisms(graph_list[0][i], graph_list[0][j]))

def find_isomorphisms(G, H):
    count = 0
    matrix_size = len(G.matrix[0])
    for perm in get_permutations(range(matrix_size), matrix_size):
        if are_equal(G.matrix, H.matrix, perm):
            count += 1
    return count

def are_equal(matrixG, matrixH, perm):
    matrix_size = len(matrixG[0])
    for i in range(matrix_size):
        for j in range(i+1, matrix_size):
            if matrixG[i][j] != matrixH[perm[i]][perm[j]]:
                return False
    return True

def get_permutations(list_of_elements, n):
    if n == 0:
        yield []
        return

    for i in list_of_elements:
        tmp = list(list_of_elements)          
        tmp.remove(i)
        for perm in get_permutations(tmp, n-1):
            yield [i] + perm

if __name__ == "__main__":
    """
    Main function
    :param 1: The .grl-file
    """
    start = time.time()
    with open(sys.argv[1]) as f:
        graph_list = load_graph(f, read_list=True)
        find_all_isomorphims(graph_list)

    end = time.time()
    print("Elapsed time (total): " + str(int((end-start)*1000)) + " ms")

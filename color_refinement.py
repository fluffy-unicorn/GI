from graph_io import load_graph, write_dot

# Print a dot file with filename and graph
def print_dot(filename, G):
	with open(filename, 'w') as f:
		write_dot(G, f)

def get_neighbourhood(v): 				### Optimisation: store neighbourhood color list in vertex class ???
	result = []
	for n in v.neighbours:
		result.append(n.colornum)
	result.sort()
	return result

def get_known_neighbourhood(n, lst):
	for i in range(len(lst)):
		if lst[i][2] == n:
			return lst[i][0]
	return -1

def get_index(v, lst):
	for i in range(len(lst)):
		if lst[i][1] == v:
			return i
	return -1

# Load graph from file
with open('colorref_smallexample_6_15.grl') as f:
	L=load_graph(f, read_list=True)

# Rename labels
for v in L[0][0].vertices:
	v.label = "(0: " + str(v.label) + ") "
for v in L[0][1].vertices:
	v.label = "(1: " + str(v.label) + ") "

vertex_count = len(L[0][0])
# Create a disjoint union of the first two graphs
G = L[0][0] + L[0][1]

partitions = {}
last_colour = 0
# Initially color the vertices based on degree
for v in G.vertices:
	v.colornum = v.degree
	if last_colour < v.degree:
		last_colour = v.degree
	if v.degree in partitions:
		partitions[v.degree].append(v)
	else:
		partitions[v.degree] = [v]
print_dot('input.dot', G)

last_colour += 1
# Number of loops equals number of vertices
for v in range(vertex_count):
	for p in partitions.copy():
		part = partitions[p]
		n = len(part)
		tmp = [] # list of (colour, vertex, neighbourhood)-tuples
		i = 0
		for j in range(1, n):
			ni = get_neighbourhood(part[i])
			nj = get_neighbourhood(part[j])
			if not ni == nj:
				colour = get_known_neighbourhood(nj, tmp)
				idx = get_index(part[j], tmp)
				if idx == -1:
					if colour >= 0:
						tmp.append((colour, part[j], nj))
					else:
						tmp.append((last_colour, part[j], nj))
						last_colour += 1
				else:
					if colour >= 0:
						tmp[idx] = (colour, part[j], nj)
					else:
						tmp[idx] = (last_colour, part[j], nj)
						last_colour += 1
		# Update the dictionary and the vertices
		for t in tmp:
			if t[1] in part:
				part.remove(t[1])
			if t[0] in partitions:
				partitions[t[0]].append(t[1])
			else:
				partitions[t[0]] = [t[1]]
			t[1].colornum = t[0]

if len(partitions) == vertex_count:
	print("Yes")
else:
	for p in partitions:
		if len(p) % 2 != 0:
			print("No")
			break
	print("Maybe")
# Write output to .dot files
#for (i, H) in enumerate(L[0]):
#	print_dot('output' + str(i) + '.dot', H)
print_dot('output.dot', G)

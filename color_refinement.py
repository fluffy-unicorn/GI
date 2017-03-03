from graph_io import load_graph, write_dot

def print_dot(filename, G):
	with open(filename, 'w') as f:
		write_dot(G, f)

def have_same_neighbours(v1, v2):
	l1 = []
	l2 = []
	for n in v1.neighbours:
		l1.append(n.colornum)
	for n in v2.neighbours:
		l2.append(n.colornum)
	l1.sort()
	l2.sort()
	return l1 == l2

def is_in_list(value, lst):
	for l in lst:
		if l[1] == value:
			return True
	return False

# Load graph from file
with open('simplest.grl') as f:
	L=load_graph(f, read_list=True)

# Rename labels
for v in L[0][0].vertices:
	v.label = "0: " + str(v.label)
for v in L[0][1].vertices:
	v.label = "1: " + str(v.label)
# Create a disjoint union of the first two graphs
G = L[0][0] + L[0][1]

partitions = {}
last_color = 0
# Initially color the vertices based on degree
for v in G.vertices:
	v.colornum = v.degree
	if last_color < v.degree:
		last_color = v.degree
	if v.degree in partitions:
		partitions[v.degree].append(v)
	else:
		partitions[v.degree] = [v]

last_color += 1
index = 0
# Number of loops equals number of vertices
for v in range(1):
	for p in partitions.copy():
		part = partitions[p]
		n = len(part)
		tmp = []
		for i in range(n):
			for j in range(i+1, n):
				if not have_same_neighbours(part[i], part[j]):
					if is_in_list(part[i], tmp):
						tmp.append((part[i].colornum, part[j]))
					else:
						tmp.append((last_color, part[j]))
					last_color += 1
		# Update the dictionary and the vertices
		print(tmp)
		for t in tmp:
			if t[1] in part:
				part.remove(t[1])
			if t[0] in partitions:
				partitions[t[0]].append(t[1])
			else:
				partitions[t[0]] = [t[1]]
			t[1].colornum = t[0]
		index += 1
				
				
			
# Write output to .dot files
#for (i, H) in enumerate(L[0]):
#	print_dot('output' + str(i) + '.dot', H)
print_dot('output.dot', G)

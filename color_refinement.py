from graph_io import *

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

# Load graph from file
with open('colorref_smallexample_6_15.grl') as f:
	L=load_graph(f, read_list=True)

# Create a disjoint union of the graphs
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
# Number of loops equals number of vertices
for v in G.vertices:
	for p in partitions:
		n = len(p)
		tmp = []
		for i in range(n):
			for j in range(i+1, n):
				if not have_same_neighbours(p[i], (p[j]):
					tmp.append( (last_color, p[j]) );
					last_color += 1
		# Update the dictionary and the vertices
		for t in tmp:
			p.remove(t[1])
			if t[0] in partitions:
				partitions[t[0]].append(t[1])
			else:
				partitions[t[0]] = [t[1]]
			t[1].colornum = t[0]
				
				
			
# Write output to .dot files
for (i, H) in enumerate(L[0]):
	with open('output' + str(i) + '.dot', 'w') as f:
		write_dot(H, f)

with open('output.dot', 'w') as f:
	write_dot(G, f)

from triest_impr import TriestFD

filename = "web-Google.txt"
M = 7000

triangle_counts = 0
actual_triangles = 13391903

model = TriestFD(M)

with open(filename) as f:
    for line in f:
        if line.startswith('#'):
            continue
    
        u,v = list(map(int,line.strip().split()))
        model.run(u,v)

triangle_counts = model.return_counters()['global']
print("Triangle counts",triangle_counts)
print("Triangle counts accuracy",triangle_counts/actual_triangles)
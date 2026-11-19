import itertools
def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
def det4_alt(rows):
    # expansion along last column (index 3), sign (-1)^(i+3)
    t=0
    for i in range(4):
        minor=[rows[j][:3] for j in range(4) if j!=i]
        t += (-1)**(i+3)*det3(minor)
    return t
def det4_alt2(rows):
    t=0
    for i in range(4):
        minor=[rows[j][:3] for j in range(4) if j!=i]
        t += (-1)**(i)*det3(minor)
    return t
def lifted(p):
    x,y=p; return (x,y,x*x+y*y,1)
# sanity: four points on a circle x^2+y^2=25 -> (5,0),(0,5),(-5,0),(0,-5)
rows=[lifted(p) for p in [(5,0),(0,5),(-5,0),(0,-5)]]
print("circle test alt ", det4_alt(rows), " alt2 ", det4_alt2(rows))
# collinear
rows=[lifted(p) for p in [(0,0),(1,1),(2,2),(3,3)]]
print("collinear alt ", det4_alt(rows), " alt2 ", det4_alt2(rows))
# corner family a=2, t=1
a=2;t=1
rows=[lifted(p) for p in [(0,0),(a,0),(t,t),(0,a)]]
print("corner a=2 t=1 alt ", det4_alt(rows), " alt2 ", det4_alt2(rows), " expected -2*a^2*t*(a-t)=", -2*a*a*t*(a-t))

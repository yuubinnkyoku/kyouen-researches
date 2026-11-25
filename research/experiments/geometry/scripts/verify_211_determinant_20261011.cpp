// Independent integer 3x3 lifted determinant enumeration of all 2+1+1 circles.
#include <cassert>
#include <algorithm>
#include <cstdint>
#include <iostream>
struct Point { int x, y; };

static int64_t lifted_det(Point p0, Point p1, Point p2, Point p3) {
    // Translate the four-row [x,y,x^2+y^2,1] determinant to a 3x3.
    const auto z = [](Point p) -> int64_t { return int64_t(p.x)*p.x + int64_t(p.y)*p.y; };
    const int64_t x1=p1.x-p0.x, y1=p1.y-p0.y, z1=z(p1)-z(p0);
    const int64_t x2=p2.x-p0.x, y2=p2.y-p0.y, z2=z(p2)-z(p0);
    const int64_t x3=p3.x-p0.x, y3=p3.y-p0.y, z3=z(p3)-z(p0);
    return x1*(y2*z3-z2*y3)-y1*(x2*z3-z2*x3)+z1*(x2*y3-y2*x3);
}

static int64_t direct_count(int w, int h) {
    int64_t total=0;
    for(int a=0;a<h;a++)
        for(int b=0;b<h;b++) if(b!=a)
            for(int c=b+1;c<h;c++) if(c!=a)
                for(int x0=0;x0<w;x0++)
                    for(int x1=x0+1;x1<w;x1++)
                        for(int u=0;u<w;u++)
                            for(int v=0;v<w;v++)
                                total += (lifted_det({x0,a},{x1,a},{u,b},{v,c})==0);
    return total;
}

int main() {
    std::cout << "width,height,c211,parity\n";
    for(int h=1;h<=11;h++) for(int w=1;w<=11;w++) {
        const int64_t c=direct_count(w,h);
        const int expected=(w%2 && h%2) ? ((std::min(w,h)-1)/2)%2 : 0;
        assert(c%2==expected);
        if(w==11 && h==11) assert(c==39557);
        std::cout << w << ',' << h << ',' << c << ',' << expected << '\n';
    }
}

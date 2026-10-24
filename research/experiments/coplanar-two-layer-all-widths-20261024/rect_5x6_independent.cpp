// Independent direct integer-cross-product audit of oriented 3+2 configurations.
#include <iostream>
#include <vector>
using namespace std;

struct P { int y, z; };
int cross(P a, P b, P c, P d) {
    return (b.y-a.y)*(d.z-c.z) - (b.z-a.z)*(d.y-c.y);
}
void audit(int k, int m, long long expected_safe) {
    vector<P> v;
    for (int y=0; y<k; ++y)
        for (int z=0; z<m; ++z) v.push_back({y,z});
    const int N = static_cast<int>(v.size());
    long long safe=0, terminal=0;
    for (int a=0; a<N; ++a)
    for (int b=a+1; b<N; ++b)
    for (int c=b+1; c<N; ++c) {
        if (cross(v[a],v[b],v[a],v[c])==0) continue;
        for (int d=0; d<N; ++d)
        for (int e=d+1; e<N; ++e) {
            if (cross(v[a],v[b],v[d],v[e])==0 ||
                cross(v[a],v[c],v[d],v[e])==0 ||
                cross(v[b],v[c],v[d],v[e])==0) continue;
            ++safe;
            bool extendible=false;
            for (int f=0; f<N; ++f) {
                if (f==d || f==e || cross(v[d],v[e],v[d],v[f])==0) continue;
                if (cross(v[a],v[b],v[d],v[f])==0 ||
                    cross(v[a],v[c],v[d],v[f])==0 ||
                    cross(v[b],v[c],v[d],v[f])==0) continue;
                if (cross(v[a],v[b],v[e],v[f])==0 ||
                    cross(v[a],v[c],v[e],v[f])==0 ||
                    cross(v[b],v[c],v[e],v[f])==0) continue;
                extendible=true;
                break;
            }
            if (!extendible) ++terminal;
        }
    }
    cout << k << "x" << m << ": oriented_safe=" << safe
         << " oriented_terminal=" << terminal << "\n";
    if (safe!=expected_safe || terminal!=0) std::exit(1);
}
int main() {
    audit(5,5,475400);
    audit(5,6,1278380);
    audit(6,6,3408680);
}

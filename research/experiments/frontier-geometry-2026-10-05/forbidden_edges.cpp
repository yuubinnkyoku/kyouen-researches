// Q_p forbidden edges. Filtering by sum(t)=0 is justified by the
// Vandermonde identity recorded in K0096; determinants are integer exact.
#include <array>
#include <cstdlib>
#include <iostream>
#include <vector>
using I = __int128_t;
I det(const std::array<int,4>& q, const std::vector<long long>& y) {
    I x[3], z[3], n[3];
    for (int k=0;k<3;++k) {
        x[k]=q[k]-q[3]; z[k]=y[q[k]]-y[q[3]];
        n[k]=x[k]*x[k]+z[k]*z[k];
    }
    return x[0]*(z[1]*n[2]-n[1]*z[2])
         - z[0]*(x[1]*n[2]-n[1]*x[2])
         + n[0]*(x[1]*z[2]-z[1]*x[2]);
}
int main(int argc,char**argv) {
    if (argc!=2) return 2;
    int p=std::atoi(argv[1]);
    if (p<3 || p>100000) return 2;
    std::vector<long long> y(p);
    for(int i=0;i<p;++i)y[i]=1LL*i*i%p;
    for(int i=0;i<p;++i)for(int j=i+1;j<p;++j)for(int k=j+1;k<p;++k){
        int l=(-(i+j+k)%p+p)%p;
        if(l>k && det({i,j,k,l},y)==0)
            std::cout<<i<<' '<<j<<' '<<k<<' '<<l<<'\n';
    }
}

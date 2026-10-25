#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

// Coordinate-pattern support enumeration for q ordered cube vertices.
// Every rank test is exact over Q for q<=5: a nonzero 0/1 minor of
// size <=6 has absolute value <=6^3=216 < FIELD_PRIME.
// Rebuild with -DFIELD_PRIME=10007 for an additional prime check.
#ifndef FIELD_PRIME
#define FIELD_PRIME 1009
#endif
constexpr int P=FIELD_PRIME;
int mod(int x) { x%=P; return x<0?x+P:x; }
int inverse(int x) {
    int b=P-2, y=1;
    for(;b;b>>=1,x=x*x%P) if(b&1)y=y*x%P;
    return y;
}

bool good_support(int q, const std::vector<int>& patterns) {
    int k=(int)patterns.size(), cols=k+1;
    if(k==0)return false;
    std::vector<unsigned int> rows(q,0);
    for(int j=0;j<k;++j)
        for(int i=0;i<q;++i)
            if(patterns[j]&(1<<i))rows[i]|=1u<<j;
    for(int i=0;i<q;++i)
        for(int j=0;j<i;++j)
            if(rows[i]==rows[j])return false;

    // Row-reduced augmented matrix: q rows, k coordinates plus constant 1.
    int a[5][17]={};
    for(int i=0;i<q;++i) {
        for(int j=0;j<k;++j)a[i][j]=(rows[i]>>j)&1;
        a[i][k]=1;
    }
    int pivots[5], rank=0;
    for(int col=0;col<cols && rank<q;++col) {
        int pivot=rank;
        while(pivot<q && !a[pivot][col])++pivot;
        if(pivot==q)continue;
        for(int j=0;j<cols;++j)std::swap(a[pivot][j],a[rank][j]);
        int inv=inverse(a[rank][col]);
        for(int j=col;j<cols;++j)a[rank][j]=a[rank][j]*inv%P;
        for(int i=0;i<q;++i)if(i!=rank && a[i][col]) {
            int c=a[i][col];
            for(int j=col;j<cols;++j)a[i][j]=mod(a[i][j]-c*a[rank][j]);
        }
        pivots[rank++]=col;
    }
    bool is_pivot[17]={};
    for(int i=0;i<rank;++i)is_pivot[pivots[i]]=true;
    int nulls[17][17]={}, nn=0;
    for(int j=0;j<cols;++j)if(!is_pivot[j]) {
        nulls[nn][j]=1;
        for(int i=0;i<rank;++i)nulls[nn][pivots[i]]=mod(-a[i][j]);
        ++nn;
    }
    // (z,1) belongs to the affine row span iff it is orthogonal
    // to every nullspace vector.
    int count=0;
    for(unsigned int z=0;z<(1u<<k);++z) {
        bool inside=true;
        for(int i=0;i<nn && inside;++i) {
            int sum=nulls[i][k];
            unsigned int bits=z;
            while(bits) {
                int j=__builtin_ctz(bits);
                sum+=nulls[i][j];
                bits&=bits-1;
            }
            if(sum%P)inside=false;
        }
        count+=inside;
        if(count>q)return false;
    }
    return count==q;
}

void choose(int q,int k,int next,std::vector<int>& patterns,
            std::vector<unsigned long long>& g) {
    if((int)patterns.size()==k) {
        if(good_support(q,patterns))++g[k];
        return;
    }
    int remaining=k-(int)patterns.size();
    for(int v=next;v<=(1<<q)-remaining;++v) {
        patterns.push_back(v);
        choose(q,k,v+1,patterns,g);
        patterns.pop_back();
    }
}
int main(int argc,char**argv) {
    if(argc!=3) {
        std::cerr<<"usage: support_enumerator q max_k\n";
        return 1;
    }
    int q=std::atoi(argv[1]), max_k=std::atoi(argv[2]);
    if(q<2||q>5||max_k<0||max_k>(1<<q)||max_k>16)return 2;
    std::vector<unsigned long long> g(max_k+1,0);
    std::vector<int> patterns;
    for(int k=0;k<=max_k;++k) {
        choose(q,k,0,patterns,g);
        std::cout<<"q="<<q<<" k="<<k<<" good_supports="<<g[k]<<"\n";
    }
    return 0;
}

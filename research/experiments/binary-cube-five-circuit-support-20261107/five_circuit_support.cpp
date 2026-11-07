// Exact enumeration of five-element affine circuits in {0,1}^d, 3<=d<=6.
// Compile: c++ -O3 -std=c++17 five_circuit_support.cpp -o verify && ./verify
#include <iostream>
#include <algorithm>
#include <cstdint>
using namespace std;
int rank_mod101(const int *a, int n, int d) {
    int m[4][6] = {};
    for (int i=1;i<n;i++) for(int j=0;j<d;j++)
        m[i-1][j]=(((a[i]>>j)&1)-((a[0]>>j)&1)+101)%101;
    int r=0;
    for(int c=0;c<d && r<n-1;c++) {
        int p=r; while(p<n-1 && m[p][c]==0) p++;
        if(p==n-1) continue;
        for(int j=c;j<d;j++) swap(m[p][j],m[r][j]);
        int inv=1; while(inv*m[r][c]%101!=1) inv++;
        for(int j=c;j<d;j++) m[r][j]=m[r][j]*inv%101;
        for(int i=r+1;i<n-1;i++) {
            int t=m[i][c];
            for(int j=c;j<d;j++) m[i][j]=(m[i][j]-t*m[r][j]%101+101)%101;
        }
        r++;
    }
    return r;
}
int main() {
    const long long expected[4][7]={
        {0,0,0,8,0,0,0},
        {0,0,0,64,96,0,0},
        {0,0,0,320,960,800,0},
        {0,0,0,1280,5760,9600,5760}
    };
    for(int d=3;d<=6;d++) {
        const int N=1<<d;
        int a[5];
        long long hist[7]={};
        for(a[0]=0;a[0]<N;a[0]++)
        for(a[1]=a[0]+1;a[1]<N;a[1]++)
        for(a[2]=a[1]+1;a[2]<N;a[2]++)
        for(a[3]=a[2]+1;a[3]<N;a[3]++)
        for(a[4]=a[3]+1;a[4]<N;a[4]++) {
            if(rank_mod101(a,5,d)!=3) continue;
            bool minimal=true;
            for(int omit=0;omit<5;omit++) {
                int b[4],k=0;
                for(int j=0;j<5;j++) if(j!=omit) b[k++]=a[j];
                if(rank_mod101(b,4,d)!=3) {minimal=false;break;}
            }
            if(!minimal) continue;
            int mask=0;
            for(int j=1;j<5;j++) mask |= a[0]^a[j];
            hist[__builtin_popcount((unsigned)mask)]++;
        }
        long long sum=0;
        for(int s=0;s<=d;s++) {
            if(hist[s]!=expected[d-3][s]) {
                cerr<<"Mismatch d="<<d<<" s="<<s<<endl; return 1;
            }
            sum+=hist[s];
        }
        cout<<"d="<<d<<" five_circuits="<<sum<<" support:";
        for(int s=3;s<=d;s++) cout<<" "<<s<<":"<<hist[s];
        cout<<endl;
    }
}

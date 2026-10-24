// Independent exhaustive audit for 10-point and 12-point hyperplane sections of {0,1}^5.
// Enumerates all 5-point subsets and uses exact 4x4 determinants;
// no Sperner bound or theoretical normal-form classification is assumed.
#include <array>
#include <algorithm>
#include <map>
#include <set>
#include <iostream>
#include <numeric>
#include <cstdlib>
using namespace std;
using Row = array<int,5>;
using Hyper = array<int,6>; // a_0,...,a_4,b: sum a_i*x_i=b

int det4(int M[4][4]) {
    int p[4]={0,1,2,3}, ans=0;
    do {
        int s=1;
        for(int i=0;i<4;i++)
            for(int j=i+1;j<4;j++)
                if(p[i]>p[j]) s=-s;
        int term=s;
        for(int i=0;i<4;i++) term*=M[i][p[i]];
        ans+=term;
    } while(next_permutation(p,p+4));
    return ans;
}

int main() {
    Row V[32];
    for(int v=0;v<32;v++)
        for(int j=0;j<5;j++) V[v][j]=(v>>j)&1;
    set<Hyper> planes;
    long long subsets=0,rank4=0;
    for(int i=0;i<32;i++)
    for(int j=i+1;j<32;j++)
    for(int k=j+1;k<32;k++)
    for(int l=k+1;l<32;l++)
    for(int m=l+1;m<32;m++) {
        subsets++;
        int inds[5]={i,j,k,l,m};
        int diff[4][5];
        for(int r=0;r<4;r++)
            for(int c=0;c<5;c++)
                diff[r][c]=V[inds[r+1]][c]-V[i][c];
        Hyper h{};
        for(int omit=0;omit<5;omit++) {
            int M[4][4];
            for(int r=0;r<4;r++) {
                int cc=0;
                for(int c=0;c<5;c++)
                    if(c!=omit) M[r][cc++]=diff[r][c];
            }
            h[omit]=((omit%2)?-1:1)*det4(M);
        }
        int g=0;
        for(int c=0;c<5;c++) g=gcd(g,abs(h[c]));
        if(g==0) continue; // the 5 points have affine rank <4
        rank4++;
        for(int c=0;c<5;c++) h[c]/=g;
        for(int c=0;c<5;c++)
            if(h[c]!=0) {
                if(h[c]<0) for(int t=0;t<5;t++) h[t]=-h[t];
                break;
            }
        h[5]=0;
        for(int c=0;c<5;c++) h[5]+=h[c]*V[i][c];
        planes.insert(h);
    }
    map<pair<int,int>,int> types;
    for(const auto &h:planes) {
        int hit=0;
        for(const auto &v:V) {
            int sum=0;
            for(int c=0;c<5;c++) sum+=h[c]*v[c];
            if(sum==h[5]) hit++;
        }
        if(hit>=10) {
            int supp=0;
            for(int c=0;c<5;c++) supp+=(h[c]!=0);
            types[{hit,supp}]++;
        }
    }
    cout<<"subsets="<<subsets
        <<" rank4_subsets="<<rank4
        <<" distinct_hyperplanes="<<planes.size()<<"\n";
    for(auto [key,n]:types)
        cout<<"intersection="<<key.first
            <<" support="<<key.second<<" count="<<n<<"\n";
    if(subsets!=201376 || rank4!=179136 || planes.size()!=3254
       || types[{10,5}]!=32 || types[{12,3}]!=80 || types[{12,4}]!=40
       || types[{16,1}]!=10 || types[{16,2}]!=20
       || types.size()!=5) return 1;
    return 0;
}

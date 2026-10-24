#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
using ll=long long;
ll det(array<array<ll,4>,4> a) {
    ll prev=1,sign=1;
    for(int k=0;k<3;k++) {
        int p=k;while(p<4 && a[p][k]==0)++p;
        if(p==4)return 0;
        if(p!=k){swap(a[p],a[k]);sign=-sign;}
        ll pivot=a[k][k];
        for(int i=k+1;i<4;i++)for(int j=k+1;j<4;j++){
            ll num=a[i][j]*pivot-a[i][k]*a[k][j];
            assert(num%prev==0);a[i][j]=num/prev;
        }
        for(int i=k+1;i<4;i++)a[i][k]=0;
        prev=pivot;
    }
    return sign*a[3][3];
}
bool independent5(const vector<int>& v) {
    array<array<ll,4>,4> gram{};
    for(int i=0;i<4;i++)for(int j=0;j<4;j++)for(int k=0;k<4;k++){
        ll di=((v[i+1]>>k)&1)-((v[0]>>k)&1);
        ll dj=((v[j+1]>>k)&1)-((v[0]>>k)&1);
        gram[i][j]+=di*dj;
    }
    return det(gram)!=0;
}
int mex(const vector<int>& v) {
    int i=0;
    while(true){
        bool present=false;for(int x:v)if(x==i){present=true;break;}
        if(!present)return i;
        ++i;
    }
}
int main() {
    vector<int> bad;
    for(int a=0;a<16;a++)for(int b=a+1;b<16;b++)
    for(int c=b+1;c<16;c++)for(int d=c+1;d<16;d++)
    for(int e=d+1;e<16;e++)if(!independent5({a,b,c,d,e}))
        bad.push_back((1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e));
    vector<unsigned char> safe(1<<16,1);
    map<int,int> sizes,terminal;
    int count=0;
    for(int m=0;m<(1<<16);m++){
        for(int edge:bad)if((m&edge)==edge){safe[m]=0;break;}
        if(safe[m]){++count;++sizes[__builtin_popcount((unsigned)m)];}
    }
    vector<int> g(1<<16,-1),h(1<<16,-1);
    int mismatches=0;
    for(int n=16;n>=0;n--)for(int m=0;m<(1<<16);m++){
        if(!safe[m] || __builtin_popcount((unsigned)m)!=n)continue;
        vector<int> a,b;
        for(int i=0;i<16;i++)if(!(m&(1<<i)) && safe[m|(1<<i)]){
            a.push_back(g[m|(1<<i)]);b.push_back(h[m|(1<<i)]);
        }
        if(a.empty()){g[m]=0;h[m]=1;++terminal[n];}
        else{g[m]=mex(a);h[m]=mex(b);}
        if(g[m]!=n%2 || h[m]!=1-n%2)++mismatches;
    }
    cout<<"forbidden_5 "<<bad.size()<<" safe "<<count<<"\n";
    cout<<"sizes";for(auto [n,c]:sizes)cout<<" "<<n<<":"<<c;
    cout<<"\nmaximal";for(auto [n,c]:terminal)cout<<" "<<n<<":"<<c;
    cout<<"\nroot "<<g[0]<<" "<<h[0]<<" parity_mismatches "<<mismatches<<"\n";
    assert(bad.size()==1360 && count==6613);
    assert(terminal[4]==100 && terminal[6]==1088 && terminal.size()==2);
    assert(mismatches==0);
}

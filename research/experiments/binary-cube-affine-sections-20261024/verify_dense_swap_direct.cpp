// Independent C++17 checker: evaluate every coordinate/diagonal face directly.
// g++ -std=c++17 -O2 -Wall -Wextra -Werror verify_dense_swap_direct.cpp -o /tmp/dense-swap && /tmp/dense-swap
#include <array>
#include <cassert>
#include <iostream>
#include <vector>
using namespace std;
static const array<int,7> A{{1,2,6,7,9,11,16}};
struct Pair { int g, h; };
static int mex(int seen){int k=0;while(seen&(1<<k))++k;return k;}
static bool safe(int mask,int n){
    const int d=5+n;
    vector<int> rows;
    for(int i=0;i<7;i++)if(mask&(1<<i))rows.push_back(A[i]);
    for(int j=0;j<n;j++)rows.push_back(3|(1<<(5+j)));
    for(int i=0;i<d;i++){
        int v=0;
        for(int x:rows)v|=1<<((x>>i)&1);
        if(v!=3)return false;
    }
    for(int i=0;i<d;i++)for(int j=0;j<i;j++){
        int v=0;
        for(int x:rows)v|=1<<(((x>>i)^(x>>j))&1);
        if(v!=3)return false;
    }
    return true;
}
int main(){
    for(int n: {0,1,2,3,4,5,7,10,20}){
        array<Pair,128> p{};
        for(auto &v:p)v={-1,-1};
        int count=0;
        for(int k=0;k<=7;k++)for(int m=0;m<128;m++){
            if(__builtin_popcount(static_cast<unsigned>(m))!=k||!safe(m,n))continue;
            count++;
            int gb=0,hb=0,children=0;
            for(int i=0;i<7;i++)if(m&(1<<i)){
                Pair c=p[m^(1<<i)];
                if(c.g<0)continue;
                children++;gb|=1<<c.g;hb|=1<<c.h;
            }
            p[m]=children?Pair{mex(gb),mex(hb)}:Pair{0,1};
        }
        assert(count==(n==0?18:25));
        assert(p[127].g==0&&p[127].h==0);
        const int child_g[7]={3,3,2,3,2,3,-1};
        for(int i=0;i<7;i++){
            Pair c=p[127^(1<<i)];
            assert(c.g==(n==0&&i<6?2:child_g[i]));
            if(c.g>=0)assert(c.h==c.g);
        }
        cout<<"d="<<5+n<<" safe_subpositions="<<count<<" root=(0,0) OK\n";
    }
}

// Independent exact determinant and impartial-game audit for 3x5 q=6.
// Compile: g++ -O2 -std=c++17 -Wall -Wextra -o verify verify.cpp
#include <bits/stdc++.h>
using namespace std;
using i128=__int128_t;
using ll=long long;
struct Fraction {ll n,d;};
ll gcdll(ll a,ll b){return std::gcd(a,b);}
ll lcmll(ll a,ll b){return a/gcdll(a,b)*b;}
ll determinant4(const array<array<ll,4>,4>& a){
    // Bareiss elimination with exact division; all 4x4 determinants are integers.
    array<array<i128,4>,4> m{};
    for(int i=0;i<4;i++)for(int j=0;j<4;j++)m[i][j]=a[i][j];
    i128 prev=1,sign=1;
    for(int k=0;k<3;k++){
        int pivot=k;
        while(pivot<4 && m[pivot][k]==0)pivot++;
        if(pivot==4)return 0;
        if(pivot!=k){swap(m[pivot],m[k]);sign=-sign;}
        i128 val=m[k][k];
        for(int i=k+1;i<4;i++)for(int j=k+1;j<4;j++){
            i128 numerator=m[i][j]*val-m[i][k]*m[k][j];
            if(numerator%prev){cerr<<"Bareiss nonexact"<<endl;abort();}
            m[i][j]=numerator/prev;
        }
        for(int i=k+1;i<4;i++)m[i][k]=0;
        prev=val;
    }
    i128 det=sign*m[3][3];
    if(det>LLONG_MAX||det<LLONG_MIN){cerr<<"overflow"<<endl;abort();}
    return (ll)det;
}
struct Result {int circles,safe,root,maxg;map<int,int> maximal;};
Result run(Fraction U,Fraction V){
    // u=a(a+b)=1/U, v=b(a+b)=1/V; y_j=z_j/sqrt(D),
    // z=(0,u*L,(u+v)*L), D=(u+v)*L^2.
    Fraction u{U.d,U.n},v{V.d,V.n};
    ll L=lcmll(u.d,v.d),uL=u.n*(L/u.d),vL=v.n*(L/v.d);
    ll z[3]={0,uL,uL+vL},D=(uL+vL)*L;
    array<array<ll,4>,15> lifted{};
    for(int row=0;row<3;row++)for(int x=0;x<5;x++){
        lifted[row*5+x]={x*x*D+z[row]*z[row],x,z[row],1};
    }
    vector<int> edges;
    for(int mask=0;mask<(1<<15);mask++){
        if(__builtin_popcount((unsigned)mask)!=6)continue;
        int cells[6],idx=0;
        for(int k=0;k<15;k++)if(mask>>k&1)cells[idx++]=k;
        bool circle=true;
        for(int i=0;i<6 && circle;i++)for(int j=i+1;j<6 && circle;j++)
          for(int k=j+1;k<6 && circle;k++)for(int l=k+1;l<6;l++){
            array<array<ll,4>,4> mat={lifted[cells[i]],lifted[cells[j]],lifted[cells[k]],lifted[cells[l]]};
            if(determinant4(mat)!=0){circle=false;break;}
          }
        if(circle)edges.push_back(mask);
    }
    vector<unsigned char> safe(1<<15),g(1<<15);
    safe[0]=1;
    for(int mask=1;mask<(1<<15);mask++){
        int parent=mask&(mask-1);
        safe[mask]=safe[parent];
        if(safe[mask])for(int e:edges)if((mask&e)==e){safe[mask]=0;break;}
    }
    map<int,int> maximal;
    int maxg=0;
    for(int mask=(1<<15)-1;mask>=0;mask--){
        if(!safe[mask])continue;
        unsigned seen=0;
        int legal=0;
        for(int k=0;k<15;k++)if(!(mask>>k&1)&&safe[mask|(1<<k)]){
            legal++;seen|=1u<<g[mask|(1<<k)];
        }
        if(!legal)maximal[__builtin_popcount((unsigned)mask)]++;
        while(seen>>g[mask]&1)g[mask]++;
        maxg=max(maxg,(int)g[mask]);
    }
    return {(int)edges.size(),(int)count(safe.begin(),safe.end(),1),g[0],maxg,maximal};
}
int main(int argc,char**argv){
    if(argc!=2){cerr<<"usage: verify cases.tsv"<<endl;return 2;}
    ifstream f(argv[1]);if(!f){cerr<<"missing cases"<<endl;return 2;}
    string line;int checked=0;
    while(getline(f,line)){
        if(line.empty()||line[0]=='#')continue;
        istringstream in(line);string name,term;
        Fraction U,V;int circles,safe,root,maxg;
        in>>name>>U.n>>U.d>>V.n>>V.d>>circles>>safe>>root>>maxg>>term;
        auto res=run(U,V);
        stringstream s;for(auto [n,c]:res.maximal)s<<n<<":"<<c<<",";
        if(res.circles!=circles||res.safe!=safe||res.root!=root||res.maxg!=maxg||s.str()!=term){
            cerr<<"FAIL "<<name<<" got "<<res.circles<<","<<res.safe<<","<<res.root<<","<<res.maxg<<","<<s.str()<<endl;return 1;
        }
        cout<<"PASS "<<name<<" circles="<<circles<<" safe="<<safe<<" root="<<root<<" maxg="<<maxg<<" maximal="<<term<<"\n";
        checked++;
    }
    cout<<"PASS all "<<checked<<" exact determinant/game cases\n";
}

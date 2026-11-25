// Exhaustive k=6 basis for the maximum-missing-degree-three theorem.
// No third-party libraries. Compile: c++ -std=c++17 -O3 verify_k6.cpp -o verify_k6
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
constexpr int K=6, N=1<<K;
using U64=uint64_t;
int edge_id[K][K];
U64 active_mask[N];

int main(){
    int b=0;
    for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)edge_id[i][j]=edge_id[j][i]=b++;
    for(int s=1;s<N;s++)for(int x=1;x<N;x++)if(s&x)active_mask[s]|=U64(1)<<x;
    vector<array<int,15>> maps;
    array<int,K> perm={0,1,2,3,4,5};
    do {
        array<int,15> m{}; int e=0;
        for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)m[e++]=1<<edge_id[perm[i]][perm[j]];
        maps.push_back(m);
    }while(next_permutation(perm.begin(),perm.end()));
    int classes=0; U64 cases_total=0;
    for(int D=0;D<(1<<15);D++){
        int deg[K]={}; int edges=0; bool valid=true;
        for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)if(D>>edge_id[i][j]&1){deg[i]++;deg[j]++;edges++;}
        if(edges<6)continue; // <=5 missing pairs already handled by prior k=6 theorem.
        for(int i=0;i<K;i++)if(deg[i]>3)valid=false;
        if(!valid)continue;
        bool canonical=true;
        for(const auto &m:maps){
            int transformed=0, bits=D;
            while(bits){int e=__builtin_ctz((unsigned)bits);bits&=bits-1;transformed|=m[e];}
            if(transformed<D){canonical=false;break;}
        }
        if(!canonical)continue;
        classes++;
        vector<int> signatures;
        for(int i=0;i<K;i++)signatures.push_back(1<<i);
        for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)
            if(!(D>>edge_id[i][j]&1))signatures.push_back((1<<i)|(1<<j));
        U64 ncases=1;
        for(int i=0;i<K;i++)ncases*=3;
        for(int i=K;i<(int)signatures.size();i++)ncases*=2;
        int g[N]={};
        vector<int> present; present.reserve(signatures.size());
        for(U64 code=0;code<ncases;code++){
            U64 q=code,pbits=0;int u=0,z[K]={};present.clear();
            for(int i=0;i<(int)signatures.size();i++){
                int v;
                if(i<K){v=q%3;q/=3;}
                else{v=1+(q&1);q>>=1;}
                int s=signatures[i];
                if(v)present.push_back(s);
                if(v&1){
                    pbits^=active_mask[s];u^=1;
                    for(int j=0;j<K;j++)if(s>>j&1)z[j]^=1;
                }
            }
            g[0]=0;
            for(int x=1;x<N;x++){
                int px=(pbits>>x)&1, seen=0;
                // Clique move: every other clique vertex is removed.
                for(int i=0;i<K;i++)if(x>>i&1)seen|=1<<(px^z[i]);
                // Independent vertex move: delete its clique neighbors.
                for(int s:present)if(s&x){
                    int y=x&~s;
                    int child=g[y]^px^((pbits>>y)&1)^1;
                    seen|=1<<child;
                }
                int nimber=0;
                while(seen>>nimber&1)nimber++;
                g[x]=nimber;
            }
            bool uniform=true;
            for(int i=1;i<K;i++)if(z[i]!=z[0])uniform=false;
            int formula=uniform?(1^u^z[0]):(2+u);
            if(g[N-1]!=formula){
                cerr<<"FAIL D="<<D<<" code="<<code<<" actual="<<g[N-1]<<" expected="<<formula<<"\n";
                return 1;
            }
        }
        cases_total+=ncases;
        cout<<"class D="<<D<<" missing="<<edges<<" cases="<<ncases<<"\n";
    }
    if(classes!=33 || cases_total!=8211456ULL){
        cerr<<"unexpected coverage: classes="<<classes<<" cases="<<cases_total<<"\n";
        return 2;
    }
    cout<<"PASS: 33 isomorphism classes, 8211456 exhaustive parity representatives, zero mismatches\n";
}

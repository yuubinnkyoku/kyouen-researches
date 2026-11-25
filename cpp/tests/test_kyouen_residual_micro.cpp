#include "kyouen_residual_micro.hpp"
#include <cassert>
#include <iostream>
#include <random>
using namespace kyouen_residual;

static int plain(State s,std::map<Key,int>& memo){
    s.edges=minimal(std::move(s.edges));
    Key k{s.vertices,s.edges}; auto it=memo.find(k); if(it!=memo.end())return it->second;
    std::vector<int> a; Mask x=s.vertices;
    while(x){int v=__builtin_ctzll(x);x&=x-1;a.push_back(plain(play(s,v),memo));}
    std::sort(a.begin(),a.end());a.erase(std::unique(a.begin(),a.end()),a.end());
    int g=0;for(int q:a){if(q==g)++g;else if(q>g)break;}memo.emplace(k,g);return g;
}

// Independent occupied-subset oracle: no kernel play/normalize/compression.
static std::uint64_t check_subsets(int n,std::vector<Mask> edges){
    const Mask full=(Mask{1}<<n)-1;
    std::vector<int> g(Mask{1}<<n,-1);
    std::uint64_t checked=0;
    for(Mask occupied=full;;--occupied){
        bool safe=true;
        for(Mask e:edges) if((occupied&e)==e){safe=false;break;}
        if(safe){
            std::vector<bool> seen(n+1,false);
            for(int v=0;v<n;++v) if(!(occupied&(Mask{1}<<v))){
                int child=g[occupied|(Mask{1}<<v)];
                if(child>=0) seen[child]=true;
            }
            int value=0; while(value<n && seen[value]) ++value;
            g[occupied]=value;
            State s{full&~occupied,{}};
            for(Mask e:edges) s.edges.push_back(e&~occupied);
            s=normalize(std::move(s));
            std::map<Key,int> memo,baseline,local,shared;
            const int fast=closed_grundy(s);
            assert(fast<0 || fast==value);
            assert(grundy(s,memo)==value);
            assert(grundy(s,baseline,nullptr,false)==value);
            assert(grundy_shared(s,local,shared,4)==value);
            std::map<Key,int> pn;
            std::uint64_t quota=100000;
            assert(outcome(s,pn,quota)==(value!=0));
            for(std::uint64_t cap: {0ULL,1ULL,2ULL}){
                std::map<Key,int> limited;
                Stats st;
                auto left=cap;
                int result=outcome(s,limited,left,&st);
                assert(result<0 || result==(value!=0));
                assert(st.calls==cap-left);
                for(const auto& entry:limited) assert(entry.second==0 || entry.second==1);
            }
            ++checked;
        }
        if(!occupied) break;
    }
    return checked;
}
int main(){
    // Target the transition bug first: choosing one endpoint of a forbidden
    // pair must ban the other endpoint immediately.
    {
        State s{0b11,{0b11}};
        auto t=play(s,0);
        assert(t.vertices==0);
    }
    // Exhaust every clutter on <=4 vertices (all nonempty candidate edges of
    // size >=2). Compare the optimized kernel with direct mex recursion.
    std::uint64_t checked=0;
    std::map<Key,int> shared;
    std::uint64_t shared_hits=0;
    for(int n=0;n<=4;++n){
        std::vector<Mask> cand;
        for(Mask e=1;e<(Mask{1}<<n);++e)if(pc(e)>=2)cand.push_back(e);
        std::uint64_t fams=Mask{1}<<cand.size();
        for(std::uint64_t f=0;f<fams;++f){
            State s; s.vertices=(n?((Mask{1}<<n)-1):0);
            for(std::size_t i=0;i<cand.size();++i)if((f>>i)&1)s.edges.push_back(cand[i]);
            s.edges=minimal(std::move(s.edges));
            std::map<Key,int> a,b,c;
            Stats st;
            int ref=plain(s,a),got=grundy(s,b);
            int got_shared=grundy_shared(s,c,shared,4,&st);
            std::map<Key,int> pn,pn_plain;
            std::uint64_t quota=100000,plain_quota=100000;
            assert(outcome(s,pn,quota)==(ref!=0));
            assert(outcome(s,pn_plain,plain_quota,nullptr,false)==(ref!=0));
            shared_hits+=st.shared_hits;
            if(ref!=got || ref!=got_shared){
                std::cerr<<"MISMATCH n="<<n<<" family="<<f<<" ref="<<ref<<" got="<<got
                         <<" shared="<<got_shared
                         <<" vertices="<<s.vertices<<" edges=";
                for(Mask e:s.edges) std::cerr<<e<<":";
                std::cerr<<"\\n";
                return 1;
            }
            // Parity conversion: terminal/P positions flip the fixed first
            // player proposition with side to move; N positions do the reverse.
            int even=first_player_verdict_from_grundy(got,0);
            int odd =first_player_verdict_from_grundy(got,1);
            assert(even!=odd);
            ++checked;
        }
    }
    assert(shared_hits>0);
    std::uint64_t subsets=0;
    // All two-edge families on six labelled vertices, including equal,
    // contained, singleton and disjoint edges, at every safe partial state.
    for(Mask e=1;e<64;++e) for(Mask f=e;f<64;++f)
        subsets+=check_subsets(6,{e,f});
    // Unequal petals, empty/nonempty cores, free points, odd/even edge count.
    for(int h=3;h<=5;++h) for(int c=0;c<=3;++c){
        int n=c;
        Mask core=(Mask{1}<<c)-1;
        std::vector<Mask> edges;
        for(int i=0;i<h;++i){
            Mask e=core|(Mask{1}<<n++);
            if(i==h-1) e|=Mask{1}<<n++;
            edges.push_back(e);
        }
        subsets+=check_subsets(n+1,edges);
    }
    // Every safe state of paths/cycles; child graphs include disconnected
    // pieces and free vertices. Labels are permuted by seeded random cases.
    for(int n=3;n<=11;++n){
        std::vector<Mask> path;
        for(int i=1;i<n;++i) path.push_back((Mask{1}<<(i-1))|(Mask{1}<<i));
        subsets+=check_subsets(n,path);
        path.push_back((Mask{1}<<(n-1))|1);
        subsets+=check_subsets(n,path);
    }
    std::mt19937 rng(20261021);
    for(int i=0;i<120;++i){
        int n=5+rng()%4;
        std::vector<Mask> edges;
        for(int j=0;j<3+int(rng()%6);++j){
            Mask e=Mask(rng())&((Mask{1}<<n)-1);
            if(pc(e)>=2) edges.push_back(e);
        }
        subsets+=check_subsets(n,edges);
    }
    // 64th bit and large paths cannot be covered by a small subset oracle.
    State long_path{~Mask{0},{}};
    for(int i=1;i<64;++i) long_path.edges.push_back((Mask{1}<<(i-1))|(Mask{1}<<i));
    Stats path_stats;
    std::map<Key,int> path_memo;
    assert(grundy(long_path,path_memo,&path_stats)==5); // audited a_64
    assert(path_stats.closed_paths==1 && path_stats.calls==1);
    assert(closed_grundy(State{~Mask{0},{}})==0);
    assert(closed_grundy(State{~Mask{0},{~Mask{0}}})==1);
    Stats forms;
    assert(closed_grundy(State{7,{}},&forms)==1);
    assert(closed_grundy(State{7,{3,5}},&forms)==2);
    assert(closed_grundy(State{63,{3,5,9,49}},&forms)==3);
    assert(closed_grundy(State{15,{3,6,12}},&forms)==0);
    assert(forms.closed_free==1 && forms.closed_two_edges==1
           && forms.closed_sunflower==1 && forms.closed_paths==1);
    // A non-sunflower triple and a degree-three graph must fall back.
    assert(closed_grundy(State{15,{3,5,14}})==-1);
    assert(closed_grundy(State{31,{3,5,9,18}})==-1);
    // Profiling preserves both ordinary and shared-cache evaluations.
    State profiled{31,{3,5,9,18}};
    Stats profiled_stats; profiled_stats.profile=true;
    std::map<Key,int> profiled_memo;
    int profiled_g=grundy(profiled,profiled_memo,&profiled_stats);
    assert(profiled_stats.structure_ns>0);
    Stats shared_profile; shared_profile.profile=true;
    std::map<Key,int> shared_profile_memo;
    assert(grundy_shared(profiled,shared_profile_memo,shared,8,&shared_profile)==profiled_g);
    assert(shared_profile.structure_ns>0);
    // Exhaustion may retain completed descendants, never an unresolved
    // result. Reusing that partial memo with more credit must stay sound.
    std::map<Key,int> partial;
    for(std::uint64_t cap=0;cap<=32;++cap){
        auto left=cap;
        Stats st;
        int result=outcome(profiled,partial,left,&st,false);
        assert(result<0 || result==(profiled_g!=0));
        assert(st.calls==cap-left);
        for(const auto& [key,value]:partial){
            std::map<Key,int> reference;
            assert(value==(plain(State{key.v,key.e},reference)!=0));
        }
    }
    std::uint64_t one=1;
    std::map<Key,int> boundary_pn;
    assert(outcome(long_path,boundary_pn,one)==1 && one==0);
    // Components with SG 2 and SG 1 have nonzero xor despite both being N.
    std::map<Key,int> sum_pn;
    std::uint64_t sum_budget=100;
    assert(outcome(State{15,{3,5}},sum_pn,sum_budget)==1);
    std::cout<<"VERIFIED occupied_oracle_states="<<subsets<<"\n";
    std::cout<<"VERIFIED clutters="<<checked
             <<" shared_keys="<<shared.size()
             <<" shared_hits="<<shared_hits<<"\n";
}

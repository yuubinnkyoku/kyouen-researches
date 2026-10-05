#pragma once
// Exact residual-hypergraph endgame kernel for Kyouen.
//
// The kernel solves the normal-play residual game, independent of board
// geometry.  A state is (live vertices, inclusion-minimal forbidden edges).
// Playing v deletes v and every edge containing v; then supersets are removed.
// This matches the residual-clutter semantics used by K0344.
//
// IMPORTANT: this header does not construct the residual clutter from a board.
// The caller must provide the exact inclusion-minimal clutter.  Keeping the
// builder separate makes it possible to regression-test board->clutter before
// the kernel can influence df-pn verdicts.
#include <algorithm>
#include <cstdint>
#include <map>
#include <stdexcept>
#include <unordered_map>
#include <utility>
#include <vector>

namespace kyouen_residual {

using Mask = std::uint64_t; // micro frontier: at most 64 relabelled live points

inline int pc(Mask x){ return __builtin_popcountll(x); }

inline std::vector<Mask> minimal(std::vector<Mask> e){
    e.erase(std::remove(e.begin(),e.end(),Mask{0}),e.end());
    std::sort(e.begin(),e.end(),[](Mask a,Mask b){
        int pa=pc(a),pb=pc(b); return pa!=pb ? pa<pb : a<b;
    });
    e.erase(std::unique(e.begin(),e.end()),e.end());
    std::vector<Mask> out;
    for(Mask x:e){
        bool dominated=false;
        for(Mask y:out) if((y&x)==y){ dominated=true; break; }
        if(!dominated) out.push_back(x);
    }
    std::sort(out.begin(),out.end());
    return out;
}

struct State {
    Mask vertices=0;
    std::vector<Mask> edges;
};

inline State play(const State& s,int v){
    Mask b=Mask{1}<<v;
    State t; t.vertices=s.vertices&~b;
    for(Mask e:s.edges) if(!(e&b)) t.edges.push_back(e);
    t.edges=minimal(std::move(t.edges));
    return t;
}

inline std::vector<std::vector<int>> exchangeable_classes(const State& s){
    std::vector<std::vector<int>> groups;
    auto contains=[&](Mask e){ return std::binary_search(s.edges.begin(),s.edges.end(),e); };
    for(int v=0;v<64;++v) if((s.vertices>>v)&1ULL){
        bool placed=false;
        for(auto& g:groups){
            int o=g.front(); Mask pair=(Mask{1}<<v)|(Mask{1}<<o);
            bool ok=true;
            for(Mask e:s.edges){
                Mask q=e&pair;
                if(q && q!=pair && !contains(e^pair)){ ok=false; break; }
            }
            if(ok){ g.push_back(v); placed=true; break; }
        }
        if(!placed) groups.push_back({v});
    }
    return groups;
}

inline int class_keep(const std::vector<int>& g,const State& s){
    Mask m=0; for(int v:g)m|=Mask{1}<<v;
    int internal=1000,depth=0;
    for(Mask e:s.edges){
        if((e&~m)==0) internal=std::min(internal,pc(e));
        depth=std::max(depth,pc(e&m));
    }
    if(internal!=1000) return std::min<int>(g.size(),internal-1);
    if(depth==0) return int(g.size())&1;
    int keep=depth+((int(g.size())-depth)&1);
    return std::min<int>(g.size(),keep);
}

inline State compress(State s,std::uint64_t* removed=nullptr){
    for(;;){
        bool changed=false;
        for(auto& g:exchangeable_classes(s)){
            int keep=class_keep(g,s);
            if((int)g.size()<=keep) continue;
            Mask del=0;
            for(std::size_t i=(std::size_t)keep;i<g.size();++i) del|=Mask{1}<<g[i];
            if(removed) *removed+=pc(del);
            s.vertices&=~del;
            std::vector<Mask> ne;
            for(Mask e:s.edges) if(!(e&del)) ne.push_back(e);
            s.edges=minimal(std::move(ne));
            changed=true; break;
        }
        if(!changed) return s;
    }
}

inline std::vector<State> components(const State& s){
    std::vector<State> out;
    Mask unseen=s.vertices;
    while(unseen){
        int seed=__builtin_ctzll(unseen); Mask comp=Mask{1}<<seed,old=0;
        while(comp!=old){
            old=comp;
            for(Mask e:s.edges) if(e&comp) comp|=e;
        }
        State p; p.vertices=comp;
        for(Mask e:s.edges) if(e&comp) p.edges.push_back(e);
        out.push_back(std::move(p)); unseen&=~comp;
    }
    return out;
}

struct Key {
    Mask v; std::vector<Mask> e;
    bool operator<(Key const& o) const {
        if(v!=o.v) return v<o.v; return e<o.e;
    }
};

struct Stats {
    std::uint64_t calls=0,memo_hits=0,module_removed=0,component_splits=0;
};

// Returns Grundy number.  Component xor is exact; K0344 compression preserves
// Grundy, not merely outcome, so composition is sound.
inline int grundy(State s,std::map<Key,int>& memo,Stats* st=nullptr){
    if(st) ++st->calls;
    s.edges=minimal(std::move(s.edges));
    s=compress(std::move(s),st?&st->module_removed:nullptr);
    auto parts=components(s);
    if(parts.size()>1){
        if(st) ++st->component_splits;
        int g=0; for(auto& p:parts) g^=grundy(std::move(p),memo,st);
        return g;
    }
    Key k{s.vertices,s.edges};
    auto it=memo.find(k);
    if(it!=memo.end()){ if(st)++st->memo_hits; return it->second; }
    std::vector<int> vals;
    Mask x=s.vertices;
    while(x){ int v=__builtin_ctzll(x);x&=x-1; vals.push_back(grundy(play(s,v),memo,st)); }
    std::sort(vals.begin(),vals.end()); vals.erase(std::unique(vals.begin(),vals.end()),vals.end());
    int g=0; for(int xg:vals){ if(xg==g)++g; else if(xg>g)break; }
    memo.emplace(std::move(k),g); return g;
}

// Convert residual P/N back to exact_prop's fixed proposition:
// "the original first player eventually wins".
inline int first_player_verdict_from_grundy(int g,int stones){
    bool side_to_move_wins=(g!=0);
    bool first_to_move=(stones%2)==0;
    bool first_wins=side_to_move_wins ? first_to_move : !first_to_move;
    return first_wins ? 1 : 2; // ExactResult numeric convention WIN=1 LOSS=2
}

} // namespace kyouen_residual

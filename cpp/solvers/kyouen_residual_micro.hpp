#pragma once
// Exact residual-hypergraph endgame kernel for Kyouen.
//
// The kernel solves the normal-play residual game, independent of board
// geometry.  A state is (live vertices, inclusion-minimal forbidden edges).
// Playing v removes v from every edge containing it.  A resulting singleton
// bans that last vertex immediately; singleton bans are propagated to a fixed
// point.  This matches the residual-clutter semantics used by K0344.
//
// IMPORTANT: this header does not construct the residual clutter from a board.
// The caller must provide the exact inclusion-minimal clutter.  Keeping the
// builder separate makes it possible to regression-test board->clutter before
// the kernel can influence df-pn verdicts.
#include <algorithm>
#include <cstdint>
#include <map>
#include <numeric>
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

inline State normalize(State t){
    t.edges=minimal(std::move(t.edges));
    for(;;){
        Mask banned=0;
        for(Mask e:t.edges) if(pc(e)==1) banned|=e;
        banned&=t.vertices;
        if(!banned) break;
        t.vertices&=~banned;
        std::vector<Mask> ne;
        for(Mask e:t.edges){
            // An edge touching an illegal vertex can never be completed by
            // future legal play, so the whole constraint disappears.
            if(e&banned) continue;
            ne.push_back(e);
        }
        t.edges=minimal(std::move(ne));
    }
    return t;
}

inline State play(const State& s,int v){
    Mask b=Mask{1}<<v;
    State t; t.vertices=s.vertices&~b;
    for(Mask e:s.edges){
        if(e&b) e&=~b; // chosen point is now already present
        t.edges.push_back(e);
    }
    return normalize(std::move(t));
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
    std::uint64_t shared_hits=0,shared_stores=0,canonicalized=0;
};

// Exact arbitrary-relabeling canonical key for a SMALL residual component.
// This is intentionally factorial and is only for a tiny configurable gate
// (the n=11 transfer experiment uses <=6 vertices, hence at most 720
// permutations).  It is a correctness key, not a hash: isomorphic residual
// clutters receive the same Key and non-isomorphic states are never merged by
// a collision.
inline Key canonical_small(State s){
    s.edges=minimal(std::move(s.edges));
    std::vector<int> live;
    Mask x=s.vertices;
    while(x){ int v=__builtin_ctzll(x); x&=x-1; live.push_back(v); }
    const int n=(int)live.size();
    std::vector<int> perm((std::size_t)n);
    std::iota(perm.begin(),perm.end(),0);
    Key best{}; bool have=false;
    do{
        std::vector<Mask> ee;
        ee.reserve(s.edges.size());
        for(Mask e:s.edges){
            Mask q=0;
            for(int i=0;i<n;++i) if(e&(Mask{1}<<live[(std::size_t)i]))
                q|=Mask{1}<<perm[(std::size_t)i];
            ee.push_back(q);
        }
        ee=minimal(std::move(ee));
        Mask vv=(n==64)?~Mask{0}:((n==0)?Mask{0}:((Mask{1}<<n)-1));
        Key k{vv,std::move(ee)};
        if(!have || k<best){ best=std::move(k); have=true; }
    }while(std::next_permutation(perm.begin(),perm.end()));
    return best;
}

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


/* Shared-component variant for Sprouts-style reuse.

   local memo is per residual solve. shared memo persists across independent
   roots/calls and is keyed by exact arbitrary-relabeling canonical form only
   at <=share_gate live vertices.  The shared table stores only completed
   Grundy values, so a cache miss can cost time but can never affect soundness.
*/
inline int grundy_shared(State s,std::map<Key,int>& local,
                         std::map<Key,int>& shared,int share_gate,
                         Stats* st=nullptr){
    if(st) ++st->calls;
    s.edges=minimal(std::move(s.edges));
    s=compress(std::move(s),st?&st->module_removed:nullptr);
    auto parts=components(s);
    if(parts.size()>1){
        if(st) ++st->component_splits;
        int g=0;
        for(auto& p:parts)
            g^=grundy_shared(std::move(p),local,shared,share_gate,st);
        return g;
    }

    Key raw{s.vertices,s.edges};
    auto li=local.find(raw);
    if(li!=local.end()){ if(st) ++st->memo_hits; return li->second; }

    const bool share=share_gate>0 && pc(s.vertices)<=share_gate;
    Key ck{};
    if(share){
        ck=canonical_small(s);
        if(st) ++st->canonicalized;
        auto si=shared.find(ck);
        if(si!=shared.end()){
            if(st) ++st->shared_hits;
            local.emplace(std::move(raw),si->second);
            return si->second;
        }
    }

    std::vector<int> vals;
    Mask x=s.vertices;
    while(x){
        int v=__builtin_ctzll(x); x&=x-1;
        vals.push_back(grundy_shared(play(s,v),local,shared,share_gate,st));
    }
    std::sort(vals.begin(),vals.end());
    vals.erase(std::unique(vals.begin(),vals.end()),vals.end());
    int g=0;
    for(int xg:vals){ if(xg==g)++g; else if(xg>g)break; }
    local.emplace(std::move(raw),g);
    if(share){
        auto [it,added]=shared.emplace(std::move(ck),g);
        if(!added && it->second!=g)
            throw std::runtime_error("shared residual Grundy contradiction");
        if(added && st) ++st->shared_stores;
    }
    return g;
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

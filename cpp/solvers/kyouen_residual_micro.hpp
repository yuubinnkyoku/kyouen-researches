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
//
// Before enumerating relabelings, run an isomorphism-invariant color refinement
// on the vertex/edge incidence structure.  Any true isomorphism preserves the
// stable colors, so it is sufficient to permute vertices *within* each final
// color cell.  This keeps exactness (no hash collisions, no heuristic merge)
// while avoiding n! work on the overwhelmingly asymmetric small components.
inline Key canonical_small(State s){
    s.edges=minimal(std::move(s.edges));
    std::vector<int> live;
    Mask x=s.vertices;
    while(x){ int v=__builtin_ctzll(x); x&=x-1; live.push_back(v); }
    const int n=(int)live.size();

    // Relabel the incidence structure locally as 0..n-1.
    std::vector<std::vector<int>> ev;
    ev.reserve(s.edges.size());
    std::vector<std::vector<int>> incident((std::size_t)n);
    for(std::size_t ei=0;ei<s.edges.size();++ei){
        std::vector<int> row;
        for(int i=0;i<n;++i)
            if(s.edges[ei]&(Mask{1}<<live[(std::size_t)i])) row.push_back(i);
        for(int i:row) incident[(std::size_t)i].push_back((int)ei);
        ev.push_back(std::move(row));
    }

    auto canonical_ranks=[](const std::vector<std::vector<int>>& sig){
        std::map<std::vector<int>,int> ranks;
        for(const auto& q:sig) ranks.emplace(q,0);
        int r=0; for(auto& kv:ranks) kv.second=r++;
        std::vector<int> out; out.reserve(sig.size());
        for(const auto& q:sig) out.push_back(ranks.find(q)->second);
        return out;
    };

    // Initial color: incidence counts by edge size.
    std::vector<std::vector<int>> init((std::size_t)n,
                                       std::vector<int>((std::size_t)n+1,0));
    for(const auto& e:ev)
        for(int v:e) ++init[(std::size_t)v][e.size()];
    std::vector<int> color=canonical_ranks(init);

    // 1-WL refinement on the bipartite incidence graph, with hyperedge size
    // included in the edge signature.  Keeping the previous vertex color in
    // the new signature guarantees monotone refinement.
    for(;;){
        std::vector<std::vector<int>> esig(ev.size());
        for(std::size_t ei=0;ei<ev.size();++ei){
            auto& q=esig[ei];
            q.push_back((int)ev[ei].size());
            std::vector<int> cs;
            for(int v:ev[ei]) cs.push_back(color[(std::size_t)v]);
            std::sort(cs.begin(),cs.end());
            q.insert(q.end(),cs.begin(),cs.end());
        }
        std::vector<int> ecolor=canonical_ranks(esig);

        std::vector<std::vector<int>> vsig((std::size_t)n);
        for(int v=0;v<n;++v){
            auto& q=vsig[(std::size_t)v];
            q.push_back(color[(std::size_t)v]);
            std::vector<int> cs;
            for(int ei:incident[(std::size_t)v])
                cs.push_back(ecolor[(std::size_t)ei]);
            std::sort(cs.begin(),cs.end());
            q.insert(q.end(),cs.begin(),cs.end());
        }
        std::vector<int> next=canonical_ranks(vsig);
        if(next==color) break;
        color=std::move(next);
    }

    std::map<int,std::vector<int>> by_color;
    for(int i=0;i<n;++i) by_color[color[(std::size_t)i]].push_back(i);
    std::vector<std::vector<int>> cells;
    for(auto& kv:by_color){
        std::sort(kv.second.begin(),kv.second.end());
        cells.push_back(kv.second);
    }

    const Mask vv=(n==64)?~Mask{0}:((n==0)?Mask{0}:((Mask{1}<<n)-1));
    std::vector<int> order((std::size_t)n),pos((std::size_t)n);
    Key best{}; bool have=false;

    // Enumerate the Cartesian product of within-cell permutations.
    auto rec=[&](auto&& self,std::size_t ci,int off)->void{
        if(ci==cells.size()){
            for(int target=0;target<n;++target)
                pos[(std::size_t)order[(std::size_t)target]]=target;
            std::vector<Mask> ee;
            ee.reserve(ev.size());
            for(const auto& e:ev){
                Mask q=0;
                for(int v:e) q|=Mask{1}<<pos[(std::size_t)v];
                ee.push_back(q);
            }
            ee=minimal(std::move(ee));
            Key k{vv,std::move(ee)};
            if(!have || k<best){ best=std::move(k); have=true; }
            return;
        }
        auto p=cells[ci];
        do{
            for(std::size_t j=0;j<p.size();++j)
                order[(std::size_t)off+j]=p[j];
            self(self,ci+1,off+(int)p.size());
        }while(std::next_permutation(p.begin(),p.end()));
    };
    rec(rec,0,0);
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

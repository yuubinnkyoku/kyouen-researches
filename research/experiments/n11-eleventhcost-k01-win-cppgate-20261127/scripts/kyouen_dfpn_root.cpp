// kyouen_dfpn_root.cpp -- df-pn proof-search solver for the Kyouen circle game.
//
// WHY: plain DFS + transposition table hits the same wall on all four 11x11
// first moves (2.5-2.8e8 visited / 15 min, unsolved, exploding at d13-d16;
// see research/experiments/n11-search-methods/reports/N11-PROBE-4WAY.md). df-pn concentrates resources
// on branches that look provable instead of sweeping every layer uniformly.
// This file is 11x11-first but templated on N; the DFS solver stays as the
// comparison baseline.
//
// PROPOSITION (fixed for the whole search): "the player who moved FIRST on
// this line eventually wins". Stone count grows by exactly one per move, so
// the side to move is a function of the position itself:
//   even stones -> first player to move -> OR node (one winning child suffices)
//   odd stones  -> second player to move -> AND node (every reply must stay
//                  winning for the first player).
// The same canonical position always has the same stone count, so its OR/AND
// role never changes.
//
// Terminal (no legal moves): side to move loses.
//   OR node  -> proposition false: (pn, dn) = (INF, 0)
//   AND node -> proposition true:  (pn, dn) = (0, INF)
//
// Aggregation (saturating at INF):
//   OR:  pn = min pn(c),  dn = sum dn(c)
//   AND: pn = sum pn(c),  dn = min dn(c)
//
// Child thresholds (standard df-pn):
//   OR:  tp_c = min(tp, pn2+1);  td_c = td - sum_{c'!=c} dn(c')
//   AND: td_c = min(td, dn2+1);  tp_c = tp - sum_{c'!=c} pn(c')
// (64-bit math, clamped to [1, INF]; INF propagates.)
//
// The TT stores open (pn, dn) bounds AND solved marks, so unsolved-position
// knowledge is shared across the search -- the main advantage over the
// WIN/LOSS-only DFS table. Eviction drops open entries first and never the
// active root; soundness never depends on the table (worst case: recompute).
//
// REGRESSION (solve --empty): n=4 LOSS, n=5 WIN, n=6 WIN, n=7 LOSS.
// First success criterion is NOT solving 11x11: it is pushing root pn/dn
// one-sidedly with clearly fewer expansions than DFS in the same 15 min.
#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include "kyouen_residual_micro.hpp"
#include "n11_s5_quarantine.hpp"

// Thrown when the quantified search's wall allowance expires deep inside
// the exact DFS. Returning UNKNOWN there was wrong: the caller treats
// UNKNOWN as "this branch is inconclusive" and keeps scanning the
// remaining siblings, so an expired deadline did not stop the search,
// it only degraded every later branch. Throwing unwinds to s5_oracle,
// which returns the out-of-time sentinel and ends quant_solve at once.
// Positions the exact DFS already completed and published stay in the
// table; only the unfinished ancestor is abandoned, and an unfinished
// ancestor was never publishable anyway.
struct QuantTimeout : std::runtime_error {
    QuantTimeout() : std::runtime_error("QUANT_TIMEOUT") {}
};

struct Bits {
    std::uint64_t lo = 0, hi = 0;
};
static inline bool operator==(Bits a, Bits b){ return a.lo==b.lo && a.hi==b.hi; }
static inline bool operator<(Bits a, Bits b){ return a.hi<b.hi || (a.hi==b.hi && a.lo<b.lo); }
static inline Bits operator|(Bits a, Bits b){ return {a.lo|b.lo,a.hi|b.hi}; }
static inline Bits operator&(Bits a, Bits b){ return {a.lo&b.lo,a.hi&b.hi}; }
static inline Bits operator~(Bits a){ return {~a.lo,~a.hi}; }
static inline bool any(Bits a){ return a.lo || a.hi; }
static inline int popcount(Bits a){ return std::popcount(a.lo)+std::popcount(a.hi); }
static inline Bits bitof(int p){ return p<64 ? Bits{1ULL<<p,0} : Bits{0,1ULL<<(p-64)}; }
static inline bool has(Bits a,int p){ return p<64 ? ((a.lo>>p)&1) : ((a.hi>>(p-64))&1); }
static inline void setbit(Bits& a,int p){ if(p<64)a.lo|=1ULL<<p;else a.hi|=1ULL<<(p-64); }
static inline int take_lsb(Bits& a){
    if(a.lo){int p=std::countr_zero(a.lo);a.lo&=a.lo-1;return p;}
    int p=std::countr_zero(a.hi);a.hi&=a.hi-1;return p+64;
}

class PnTT {
public:
    enum : std::uint8_t { FREE=0, OPEN=1, WIN=2, LOSS=3 };
    static constexpr int PROBE = 32;
    explicit PnTT(unsigned power=26){
        n_ = std::size_t{1}<<power;
        if(n_==0 || (n_ & (n_-1))) throw std::runtime_error("bad memo power");
        mask_=n_-1;
        lo_.assign(n_,0); hi_.assign(n_,0);
        pn_.assign(n_,0); dn_.assign(n_,0);
        vis_.assign(n_,0); st_.assign(n_,0);
    }
    void set_root(std::uint64_t lo,std::uint64_t hi){ rlo_=lo; rhi_=hi; }
    int find(std::uint64_t klo,std::uint64_t khi) {
        std::size_t i=mix(klo,khi)&mask_;
        for(int j=0;j<PROBE;++j){
            if(!st_[i]){ ++misses_; probe_sum_+=std::uint64_t(j+1); ++probe_n_; return -1; }
            if(lo_[i]==klo && hi_[i]==khi){ ++hits_; probe_sum_+=std::uint64_t(j+1); ++probe_n_; return (int)i; }
            i=(i+1)&mask_;
        }
        ++misses_; probe_sum_+=PROBE; ++probe_n_; return -1;
    }
    int acquire(std::uint64_t klo,std::uint64_t khi){
        std::size_t h=mix(klo,khi)&mask_;
        std::size_t i=h;
        int first_open=-1;
        for(int j=0;j<PROBE;++j){
            if(!st_[i]){
                lo_[i]=klo;hi_[i]=khi;pn_[i]=dn_[i]=vis_[i]=0;st_[i]=OPEN;++used_;++puts_new_;return (int)i;
            }
            if(lo_[i]==klo && hi_[i]==khi) return (int)i;
            if(first_open<0 && st_[i]==OPEN && !(lo_[i]==rlo_ && hi_[i]==rhi_))
                first_open=(int)i;
            i=(i+1)&mask_;
        }
        if(first_open>=0){
            i=(std::size_t)first_open;
            lo_[i]=klo;hi_[i]=khi;pn_[i]=dn_[i]=vis_[i]=0;st_[i]=OPEN;++evictions_;return first_open;
        }
        if(lo_[h]==rlo_ && hi_[h]==rhi_){
            for(int j=0;j<PROBE;++j){
                i=(h+(std::size_t)j)&mask_;
                if(!(lo_[i]==rlo_ && hi_[i]==rhi_)){
                    std::uint8_t old=st_[i];
                    lo_[i]=klo;hi_[i]=khi;pn_[i]=dn_[i]=vis_[i]=0;st_[i]=OPEN;
                    if(old>=WIN){ ++evict_solved_; --solved_; }
                    else ++evictions_;
                    return (int)i;
                }
            }
            return -1;
        }
        std::uint8_t oldh=st_[h];
        lo_[h]=klo;hi_[h]=khi;pn_[h]=dn_[h]=vis_[h]=0;st_[h]=OPEN;
        if(oldh>=WIN){ ++evict_solved_; --solved_; }
        else ++evictions_;
        return (int)h;
    }
    std::size_t used()const{return used_;}
    std::size_t capacity()const{return n_;}
    // Three SEPARATE counters:
    //   solved_now()           = solved entries CURRENTLY in the TT
    //   solved_discoveries()   = total times an entry was marked solved
    //                            (never decremented; re-marking an
    //                            already-solved slot does not count)
    //   evicted_solved()       = solved entries evicted so far
    // Previously solved_ was an effective cumulative count: evicting a
    // solved entry bumped evict_solved_ but not solved_, so
    // used_-solved_ (open) drifted once evict_solved_>0. Splitting
    // the three keeps open exact for every eviction.
    std::uint64_t solved_now()const{return solved_;}
    std::uint64_t solved_discoveries()const{return solved_disc_;}
    std::uint64_t evicted_solved()const{return evict_solved_;}
    void mark_solved(int s,std::uint8_t v){
        if(st_[(std::size_t)s]<WIN){ ++solved_; ++solved_disc_; }
        st_[(std::size_t)s]=v;
    }
    void counters(std::uint64_t& hits,std::uint64_t& misses,
                  std::uint64_t& puts_new,std::uint64_t& puts_update,
                  std::uint64_t& ev,std::uint64_t& evs,double& ap) const {
        hits=hits_; misses=misses_; puts_new=puts_new_; puts_update=0;
        ev=evictions_; evs=evict_solved_; ap=avg_probe();
    }
    double avg_probe() const {
        return probe_n_ ? (double)probe_sum_/(double)probe_n_ : 0.0;
    }
    std::vector<std::uint64_t> lo_,hi_;
    std::vector<std::uint32_t> pn_,dn_,vis_;
    std::vector<std::uint8_t> st_;
    std::uint64_t used_=0;
    std::uint64_t hits_=0, misses_=0, puts_new_=0, evictions_=0, evict_solved_=0, solved_=0, solved_disc_=0;
    std::uint64_t probe_sum_=0, probe_n_=0;
private:
    std::size_t n_,mask_;
    std::uint64_t rlo_=~0ULL, rhi_=~0ULL;
    static inline std::uint64_t mix64(std::uint64_t x){
        x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;
        x^=x>>27;x*=0x94d049bb133111ebULL;
        return x^(x>>31);
    }
    static inline std::uint64_t mix(std::uint64_t a,std::uint64_t b){
        return mix64(a ^ (b*0x9e3779b97f4a7c15ULL));
    }
};

template<int N>
class DfPn {
public:
    static constexpr int V = N*N;
    static constexpr std::uint64_t HI_MASK =
        (V>64) ? (((V-64)>=64) ? ~0ULL : ((1ULL<<(V-64))-1ULL)) : 0ULL;
    static constexpr std::uint32_t INF = 1000000000u;
    using Clock=std::chrono::steady_clock;
    struct TState { std::array<Bits,8> t{}; };
    struct GChild {
        typename DfPn<N>::TState ts; Bits legal,key; int count=0;
        std::uint32_t pn=1,dn=1; std::uint8_t st=0;
        std::uint64_t work=0;      // cumulative expansions under this child
        std::uint32_t last_pn=1,last_dn=1; // for delta tracking
    };
    struct Gen { std::array<GChild,V> ch; int n=0; };
    // sizeof(Gen) sanity per N: GChild=176 B (8x16 B TState + 48 B).
    // n=6: 36*176+4 = 6,340. n=11: 121*176+4 = 21,300. If Gen ever grows
    // past ~64 KB the frame-heap buffers need auditing (not the stack --
    // frames are already heap/box-allocated -- but TT-adjacent RSS).
    static_assert(sizeof(Gen) < 65536,
        "Gen unexpectedly large; audit GChild/TState layout");
    struct Result {
        int outcome=0;
        std::uint64_t expansions=0;
        std::uint32_t root_pn=INF, root_dn=INF;
        double seconds=0;
    };

    explicit DfPn(unsigned memo_power=26)
      : completion_(std::size_t(V)*V*V), tt_(memo_power) {
        build_maps(); build_forbidden_quadruples();
    }

    Result solve_empty(){
        typename DfPn<N>::TState state{};
        Bits occupied{};
        // Empty board: every point is legal. Build the mask directly instead
        // of (~0ULL, HI_MASK): for V<=64 (n<=8) HI_MASK is 0 and hi would be
        // ~0 & 0 = 0 (fine), but writing it via bitof loop is unambiguous
        // for every N and immune to mask typos (the n=4 "bad move index":
        // legal.hi ended up nonzero -> take_lsb on hi=garbage -> v>=V).
        Bits legal{};
        for(int p=0;p<V;++p) setbit(legal,p);
        return solve_common(state, occupied, legal, 0);
    }

    Result solve_root(const std::vector<int>& stones){
        validate_root(stones);
        typename DfPn<N>::TState state{};
        Bits occupied{};
        for(int v:stones){ state=add(state,v); setbit(occupied,v); }
        Bits legal=legal_for(occupied);
        return solve_common(state, occupied, legal, (int)stones.size());
    }

    // ---- STANDALONE EXACT REPLAY (--exact-replay=P) ---------------
    // Re-solve a recorded handoff root with the exact solver alone, free
    // of df-pn, so its true cost can be measured. This is the
    // benchmark that move-ordering work is graded against: unlike a
    // proof number, "nodes to solve this exact position" is a direct,
    // comparable quantity.
    //
    // The position is rebuilt from the CANONICAL occupancy carried in a
    // --exact-record row. Crucially, TState is rebuilt by REPLAYING the
    // occupied points through add() in the canonical orientation, and
    // the legal mask is RE-DERIVED by legal_for() from that same
    // occupancy. It is never inherited from a parent frame and never
    // assumed to match the canonical key's bit pattern. The game is D4
    // invariant, so a canonical-orientation reconstruction is a valid
    // representative of the orbit; using the key as if it were the
    // orientation actually reached by play was a previous bug.
    //
    // Returns: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS.
    // `out_nodes` receives the exact nodes consumed by this call.
    int exact_replay(const Bits& occupied,int stones,std::uint64_t budget,
                    std::uint64_t& out_nodes) {
        if(occupied.hi & ~HI_MASK) throw std::runtime_error("exact_replay: out of board");
        if constexpr(V<64)
            if(occupied.lo >> V) throw std::runtime_error("exact_replay: out of board");
        int verts[V],k=0;
        Bits s=occupied;
        while(any(s)){ if(k>=V) throw std::runtime_error("exact_replay: bad occupancy"); verts[k++]=take_lsb(s); }
        if(k!=stones) throw std::runtime_error("exact_replay: stones mismatch");
        validate_root(std::vector<int>(verts,verts+k));
        typename DfPn<N>::TState state{};
        for(int i=0;i<k;++i) state=add(state,verts[i]);
        // Re-derive legality from the reconstructed occupancy.
        Bits legal=legal_for(occupied);
        // Reset the exact-local memo before every replayed position. The
        // replay driver reuses ONE solver for all rows, and exact_prop
        // consults exact_local_ when the publish mode is not ALL, so
        // without this a position solved by an earlier row would be
        // answered instantly from the cache (observed: one root reported
        // "LOSS" in 1 node at budget 500k after taking 8588 nodes at
        // 200k). That silently contaminates the per-root node counts this
        // benchmark exists to measure.
        exact_local_.reset();
        std::uint64_t b=budget;
        std::uint64_t before=exact_nodes_;
        ExactResult r=exact_prop(state,stones,legal,b);
        out_nodes=exact_nodes_-before;
        return (r==ExactResult::WIN)?1:((r==ExactResult::LOSS)?2:0);
    }
    void reset_exact_counters(){ exact_nodes_=0; }
    std::uint64_t exact_total_nodes() const { return exact_nodes_; }

    // ---- s5 ORACLE with a persistent canonical-key cache ----------
    // The quantified search below leans on this hard, so the oracle is
    // a first-class object with its own memo keyed by the canonical
    // occupancy. Every quantifier level revisits the same s5 positions
    // (different r3 choices can reach the same D4 orbit, and all 20
    // two-stone roots share the same reply set), so a shared cache
    // turns 20 * 121 * 117 * 116 queries into a far smaller number of
    // distinct exact searches.
    //
    // Only WIN/LOSS are cached. UNKNOWN means the node budget ran out
    // and must never be remembered as a result, or a later, better
    // funded query would inherit the earlier failure.
    struct Oracle {
        std::map<Bits,std::uint8_t> memo;  // 0 absent, 1 WIN, 2 LOSS
        std::uint64_t queries=0, hits=0, wins=0, losses=0, unknowns=0;
        std::uint64_t nodes=0;
        std::uint64_t wall=0;   // milliseconds spent inside exact_prop
        // Deep-TT reuse, sampled around each query. With publish=ALL
        // the exact DFS publishes its interior solved states into the
        // main PnTT, so these can be large even when the oracle root
        // cache never hits.
        std::uint64_t tt_hits=0, tt_misses=0, tt_growth=0;
        std::uint64_t aborted_by_time=0;
        std::uint64_t timeouts=0;
        std::uint64_t loaded=0;   // verdicts read from the persistent cache
        std::uint64_t rejected=0; // rows ignored as foreign
        std::uint64_t saved=0;    // new verdicts appended this run
        // Keys this run actually SOLVED, as opposed to loaded from
        // disk. oracle_save appends only these, so repeated runs with an
        // unchanged cache do not grow the file without bound.
        std::set<Bits> touched;
        // Eviction and probe-length growth. A saturated table shows
        // up here as rising evict_open/evict_solved and avgprobe, which
        // is how a full table can be told apart from a hard position.
        std::uint64_t evict_open=0, evict_solved=0;
        double probe_sum=0; std::uint64_t probe_n=0;
    };
    Oracle oracle;
    // The first move of the root, needed by quant_solve to rebuild the
    // two-stone position. Set by quant_root().
    int root_first_move_=-1;
    // Emit a per-third-move progress line in quant_solve. The loop can
    // run for many minutes with no other output, which is
    // indistinguishable from a hang.
    bool quant_progress_=true;
    // Wall-clock guard for the whole quantified search. --quant-timeout
    // used to be checked only after a reply finished, so a single stuck
    // oracle query could never be interrupted; the driver set the
    // solver deadline to 0 as well, which disabled the check inside
    // exact_prop too. quant_wall_stop_ is set by the driver and
    // consulted by the oracle before every query, so a runaway query
    // costs at most one budget rather than the whole time allowance.
    std::chrono::steady_clock::time_point quant_deadline_{};
    bool quant_has_deadline_=false;

    // Branch telemetry, reset per reply by quant_solve.
    // Three-valued per level: SAT (a WIN fifth move was found),
    // REFUTED (every fifth move proven LOSS), UNKNOWN (no WIN but at
    // least one fifth move inconclusive).
    std::uint64_t q_m3_tried_=0, q_m3_refuted_=0, q_m3_unknown_=0;
    std::uint64_t q_m4_sat_=0, q_m4_refuted_=0, q_m4_unknown_=0;
    std::uint64_t q_m4_sat_total_=0;   // every SAT m4 of a proved m3
    std::uint64_t q_queries_at_refute_=0;

    // True once the wall allowance is used up. Queried by the oracle
    // before each query and by quant_solve between third moves.
    bool quant_out_of_time() const {
        if(!quant_has_deadline_) return false;
        return Clock::now()>=quant_deadline_;
    }
    void set_quant_deadline(double seconds){
        quant_has_deadline_=(seconds>0);
        quant_deadline_=Clock::now()+
            std::chrono::duration_cast<Clock::duration>(
                std::chrono::duration<double>(seconds));
    }

    // Solve one 5-stone position exactly, consulting and filling the
    // oracle. Returns 1 WIN, 2 LOSS, 0 UNKNOWN (budget exhausted).
    //
    // `budget` is PER QUERY, not a shared pool: exact_prop receives a
    // fresh copy each call. An earlier note in this file said the
    // opposite, which made the measured run look budget-starved; the
    // per-query reading is the one that matches the code.
    //
    // Per-query tracing is emitted around the exact call so the cost of
    // an individual s5 position is directly observable, and so a stuck
    // query is attributable to a specific canonical key rather than
    // looking like a hang.
    int s5_oracle(const TState& state,Bits occupied,std::uint64_t budget){
        if(quant_out_of_time()) return -1;   // caller treats <0 as "stop"
        Bits key=canonical(state);
        auto it=oracle.memo.find(key);
        if(it!=oracle.memo.end()){
            ++oracle.hits; ++oracle.queries;
            return it->second;
        }
        ++oracle.queries;
        Bits legal=legal_for(occupied);
        std::uint64_t b=budget;
        std::uint64_t before=exact_nodes_;
        // Deep-TT reuse is measured separately from the oracle's own
        // root cache. run_quant() uses publish=ALL, so exact_prop writes
        // its interior solved states into the main PnTT; a later query
        // that overlaps an earlier one can therefore be much cheaper
        // even when the oracle root cache never hits. Tracking the PnTT
        // counters around each call separates "the cache did not help"
        // from "the table did".
        std::uint64_t tth0=0, ttm0=0, ttused0=tt_.used(), ttopen0=tt_open();
        std::uint64_t eo0=0, es0=0; double ap0=0;
        {
            std::uint64_t h,m,pn,d,eo,es; double ap;
            tt_.counters(h,m,pn,d,eo,es,ap);
            tth0=h; ttm0=m; eo0=eo; es0=es; ap0=ap;
        }
        if(quant_progress_){
            *log_<<"[q-start] q="<<oracle.queries
                <<" key="<<key.lo<<","<<key.hi
                <<" legal="<<popcount(legal)
                <<" budget="<<budget<<std::endl;
            log_->flush();
        }
        double t0=std::chrono::duration<double>(
            Clock::now().time_since_epoch()).count();
        ExactResult r=ExactResult::UNKNOWN;
        bool timed_out=false;
        try{
            r=exact_prop(state,5,legal,b);
        }catch(const QuantTimeout&){
            // Wall allowance expired inside the exact DFS. Report the
            // sentinel so quant_solve stops immediately; whatever the
            // exact DFS had already published stays in the table.
            //
            // Fall THROUGH to the accounting below rather than
            // returning early: the nodes, time, table growth, evictions
            // and probe length this query consumed are real cost, and
            // dropping them made the final query of every run vanish
            // from the totals.
            timed_out=true;
        }
        double t1=std::chrono::duration<double>(
            Clock::now().time_since_epoch()).count();
        std::uint64_t tth1=0, ttm1=0, ttused1=tt_.used();
        double ap1=0; std::uint64_t eo1=0, es1=0;
        {
            std::uint64_t h,m,pn,d,eo,es; double ap;
            tt_.counters(h,m,pn,d,eo,es,ap);
            tth1=h; ttm1=m; ap1=ap; eo1=eo; es1=es;
        }
        oracle.nodes+=exact_nodes_-before;
        oracle.wall+=std::uint64_t((t1-t0)*1000.0);
        oracle.tt_hits+=(tth1-tth0);
        oracle.tt_misses+=(ttm1-ttm0);
        oracle.tt_growth+=(ttused1-ttused0);
        oracle.evict_open+=(eo1-eo0);
        oracle.evict_solved+=(es1-es0);
        oracle.probe_sum+=ap1;
        oracle.probe_n++;
        if(quant_progress_){
            *log_<<(timed_out?"[q-timeout]":"[q-done]  ")<<" q="<<oracle.queries
                <<" key="<<key.lo<<","<<key.hi
                <<" result="<<(timed_out?-1:(r==ExactResult::WIN?1:(r==ExactResult::LOSS?2:0)))
                <<" nodes="<<(exact_nodes_-before)
                <<" ms="<<(long long)((t1-t0)*1000.0)
                <<" tth="<<(tth1-tth0)<<" ttm="<<ttm1-ttm0
                <<" ttused="<<ttused1<<"/"<<tt_.capacity()
                <<" eo="<<(eo1-eo0)<<" es="<<(es1-es0)
                <<" ap="<<ap1<<std::endl;
            log_->flush();
        }
        // A timed-out query has no verdict. It must NOT be cached as
        // UNKNOWN, and it must not be counted as one, or the next reply
        // would inherit the failure. Report the out-of-time sentinel
        // after the cost has been recorded.
        if(timed_out){ ++oracle.timeouts; return -1; }
        if(r==ExactResult::WIN){
            oracle.memo[key]=1; oracle.touched.insert(key);
            ++oracle.wins; return 1;
        }
        if(r==ExactResult::LOSS){
            oracle.memo[key]=2; oracle.touched.insert(key);
            ++oracle.losses; return 2;
        }
        ++oracle.unknowns;
        return 0;
    }
    void oracle_clear(){ oracle=Oracle(); }

    // ---- persistent s5 verdict cache -------------------------------
    // Maps a canonical 5-stone key to WIN or LOSS, on disk, so a proof
    // survives process restarts and does not need the 67M-entry PnTT to
    // stay resident. Only decided verdicts are stored: an UNKNOWN means
    // the node budget ran out, and persisting that would make a later,
    // better funded query inherit an earlier failure.
    //
    // This replaces the warm-table dependence. A cold replay of the 103
    // fifth moves of s4={60,0,1,2} closed every one of them as LOSS
    // within 20M nodes, and those are exactly the facts a restartable
    // refutation search needs: with the cache loaded, m4=2 resolves to
    // REFUTED from 103 hits and m3=1 to REFUTED, with no search at all.
    void oracle_load(const std::string& path){
        if(path.empty()) return;
        std::ifstream in(path);
        if(!in) throw std::runtime_error("cannot open s5 cache");
        std::string line;
        bool header_ok=false;
        int conflicts=0, foreign=0;
        while(std::getline(in,line)){
            if(line.empty()) continue;
            if(line[0]=='#'){
                // Header line. It must state the board size and the
                // schema version: the cache has become proof material,
                // so a file written by a different board size or a
                // different rule set must not be loaded silently.
                if(line.find("n=11")!=std::string::npos &&
                   line.find("schema=1")!=std::string::npos)
                    header_ok=true;
                else
                    foreign++;
                continue;
            }
            std::vector<std::string> f;
            std::stringstream ss(line); std::string t;
            while(std::getline(ss,t,',')) f.push_back(t);
            // s5verdict,key_lo,key_hi,stones,result,nodes
            if(f.size()!=6) throw std::runtime_error("malformed s5 cache row");
            if(!f[5].empty() && f[5].back()=='\r') f[5].pop_back();
            auto number=[](const std::string& value){
                if(value.empty() || !std::all_of(value.begin(),value.end(),
                        [](char c){return c>='0' && c<='9';}))
                    throw std::runtime_error("invalid unsigned integer in s5 cache");
                return std::stoull(value);
            };
            if(f[0]!="s5verdict" || number(f[3])!=5)
                throw std::runtime_error("foreign s5 cache row");
            auto code=number(f[4]);
            if(code!=1 && code!=2) throw std::runtime_error("non-exact s5 cache verdict");
            int r=static_cast<int>(code);
            number(f[5]);
            Bits k; k.lo=number(f[1]); k.hi=number(f[2]);
            if constexpr(N!=11) throw std::runtime_error("n=11 s5 cache on another board");
            if((k.hi & ~HI_MASK) || popcount(k)!=5)
                throw std::runtime_error("s5 cache occupancy outside board or wrong stone count");
            std::vector<int> pts;
            Bits remaining=k;
            TState state{};
            while(any(remaining)){
                int p=take_lsb(remaining);
                pts.push_back(p); state=add(state,p);
            }
            validate_root(pts);
            if(!(canonical(state)==k)) throw std::runtime_error("noncanonical s5 cache key");
            bool quarantined=false;
            for(const auto& q:n11_s5_quarantined_keys)
                if(k.lo==q.first && k.hi==q.second) quarantined=true;
            if(quarantined){ foreign++; continue; }
            auto it=oracle.memo.find(k);
            if(it!=oracle.memo.end()){
                // Same key with two different verdicts means the cache
                // is corrupt or the rules changed. This is proof
                // material, so refuse rather than last-wins.
                if(it->second!=(std::uint8_t)r) conflicts++;
                continue;
            }
            oracle.memo[k]=(std::uint8_t)r;
            oracle.touched.erase(k);
            ++oracle.loaded;
        }
        if(!header_ok){
            throw std::runtime_error(
                "s5 cache missing or foreign header (need n=11, schema=1)");
        }
        if(conflicts){
            throw std::runtime_error(
                "s5 cache has " + std::to_string(conflicts) +
                " key(s) with conflicting WIN/LOSS verdicts");
        }
        if(foreign){
            oracle.rejected=(std::uint64_t)foreign;
        }
    }
    // Append only the verdicts proved since the load, so repeated runs
    // do not re-append the same rows forever. `touched` records the
    // keys this run actually solved; everything loaded from disk was
    // erased from it at load time.
    void oracle_save(const std::string& path){
        if(path.empty()) return;
        bool exists=false;
        { std::ifstream probe(path); exists=probe.good(); }
        std::ofstream out(path, std::ios::out | std::ios::app);
        if(!out) return;
        if(!exists){
            // The header is what lets a later load refuse a file written
            // for another board size or rule set.
            out<<"# s5 verdict cache: n=11 schema=1 "
               <<"(canonical key -> WIN/LOSS, UNKNOWN never stored)\n";
        }
        std::uint64_t w=0;
        for(const auto& kv:oracle.memo){
            if(kv.second!=1 && kv.second!=2) continue;
            if(!oracle.touched.count(kv.first)) continue;  // not new
            out<<"s5verdict,"<<kv.first.lo<<","<<kv.first.hi<<",5,"
               <<(int)kv.second<<",0\n";
            ++w;
        }
        out.flush();
        oracle.saved=w;
    }
    std::uint64_t oracle_cache_size() const { return (std::uint64_t)oracle.memo.size(); }

    // ---- persistent s4 verdict cache, with a certificate manifest ---
    // A bare s4 -> LOSS label cannot be checked by anyone else. What
    // makes it verifiable is the manifest it carries:
    //   LOSS  every legal s5 child's canonical key (the reader can
    //         re-check that each is LOSS, and that the list is complete)
    //   WIN   the single s5 WIN witness (one child is enough)
    //
    // One entry describes one CANONICAL s4 CLASS: the class is a set of raw
    // edges naming D4-equivalent four-stone positions, and all its edges
    // share the same verdict because they share the same key. So the
    // manifest lists the union of the s5 children of the class's edges,
    // which is what a verifier must re-check.
    //
    // Written as
    //   s4verdict,first,r2,key_lo,key_hi,result,n_child,cov_size,child_lo,child_hi,...
    // `first` and `r2` are recorded because the canonical s4 key alone does
    // not say WHICH edge class this is: the cover is built for a fixed
    // two-stone root {first,r2}, and a verifier needs the endpoints to
    // recompute the coverage set and to re-derive every legal fifth move.
    // `cov_size` is the number of distinct third moves the class refutes,
    // so the reader can check the coverage it recomputes is the one claimed.
    struct S4Entry {
        std::uint8_t result=0;              // 1 WIN, 2 LOSS
        int first=-1, r2=-1;                // the two-stone root
        std::vector<std::pair<int,int>> edges;   // raw edges (a,b) in the class
        std::size_t cov_size=0;             // distinct third moves refuted
        std::vector<std::pair<std::uint64_t,std::uint64_t>> children;
    };
    std::map<std::pair<std::uint64_t,std::uint64_t>,S4Entry> s4_cache;

    // Record one decided class. `edges` are the raw edges it covers and
    // `children` the s5 keys a verifier must re-check: EVERY legal fifth
    // move for a LOSS class, or the single WIN witness for a WIN class.
    // The caller is responsible for having actually proved those verdicts.
    void s4_cache_record(const std::pair<std::uint64_t,std::uint64_t>& key,
                         int first,int r2,std::uint8_t result,
                         const std::vector<std::pair<int,int>>& edges,
                         std::size_t cov_size,
                         const std::vector<std::pair<std::uint64_t,std::uint64_t>>& children){
        if(result!=1 && result!=2) return;
        S4Entry e;
        e.result=result; e.first=first; e.r2=r2;
        e.edges=edges; e.cov_size=cov_size; e.children=children;
        s4_cache[key]=e;
    }

    // Write the manifest. `std::ios::app` plus a header-if-absent matches
    // the s5 writer: a worker owns its own file, and the coordinator merges.
    void s4_cache_save(const std::string& path) const {
        if(path.empty()) return;
        bool exists=false;
        { std::ifstream probe(path); exists=probe.good(); }
        std::ofstream out(path, std::ios::out | std::ios::app);
        if(!out) return;
        if(!exists)
            out<<"# s4 verdict cache: n=11 schema=1 "
               <<"(canonical s4 key -> WIN/LOSS + certificate manifest)\n";
        for(const auto& kv:s4_cache){
            const auto& e=kv.second;
            if(e.result!=1 && e.result!=2) continue;
            out<<"s4verdict,"<<e.first<<","<<e.r2<<","
               <<kv.first.first<<","<<kv.first.second<<","
               <<(int)e.result<<","<<e.children.size()<<","<<e.cov_size;
            for(const auto& c:e.children) out<<","<<c.first<<","<<c.second;
            out<<"\n";
        }
        out.flush();
    }
    std::uint64_t s4_cache_size() const { return (std::uint64_t)s4_cache.size(); }

    // ---- s4 EDGE classification over the persistent cache -----------
    // For a fixed two-stone root {first,r2}, the legal third moves are
    // vertices and each unordered pair {a,b} of distinct legal moves is
    // an EDGE: the pair names the same four-stone position
    // {first,r2,a,b} regardless of which was played as m3 and which as
    // m4. The edge's value is
    //     WIN  if some legal fifth move reaches a WIN s5
    //     LOSS if every legal fifth move reaches a LOSS s5
    // and a third move a is refuted as soon as ANY incident edge is LOSS.
    // Refuting the whole reply therefore reduces to covering all
    // vertices with LOSS-proved edges, which is a set-cover shaped
    // problem rather than a nested loop over 119 * 117 * 116 queries.
    //
    // The payoff is structural, not just speed: one proved LOSS edge on
    // {a,b} refutes BOTH third moves a and b at once. The single s4
    // proof {60,0,1,2} already covers m3=1 and m3=2.
    //
    // This classifies one edge using ONLY the cache: if any child is a
    // cached WIN the edge is WIN, if all children are cached LOSS the
    // edge is LOSS, and otherwise the verdict is UNKNOWN (the caller
    // then decides whether to spend exact nodes).
    enum class EdgeVerdict : std::uint8_t { UNKNOWN=0, WIN=1, LOSS=2 };
    struct EdgeInfo {
        EdgeVerdict verdict=EdgeVerdict::UNKNOWN;
        int unknown_children=0;   // children with no cached verdict
        int cached_children=0;   // children answered from the cache
        int win_children=0;
        int loss_children=0;
        std::vector<int> win_m5; // witnesses, for a WIN certificate
        std::vector<int> loss_m5;
    };
    EdgeInfo classify_edge(int r2,int a,int b) const {
        if(root_first_move_==a||root_first_move_==b||r2==a||r2==b||a==b)
            throw std::runtime_error("edge repeats a stone");
        TState s2{}; s2=add(s2,root_first_move_); s2=add(s2,r2);
        TState s3=add(s2,a);
        TState s4=add(s3,b);
        Bits occ{}; setbit(occ,root_first_move_); setbit(occ,r2);
        setbit(occ,a); setbit(occ,b);
        EdgeInfo e;
        Bits legal5=legal_for(occ);
        Bits mm=legal5;
        while(any(mm)){
            int z=take_lsb(mm);
            if(z<0) break;
            TState s5=add(s4,z);
            Bits o5=occ; setbit(o5,z);
            Bits k=canonical(s5);
            auto it=oracle.memo.find(k);
            if(it==oracle.memo.end()){ ++e.unknown_children; continue; }
            ++e.cached_children;
            if(it->second==1){ ++e.win_children; e.win_m5.push_back(z); }
            else { ++e.loss_children; e.loss_m5.push_back(z); }
        }
        // Verdict. Note the EMPTY child set: an s4 with no legal fifth
        // move is an OR terminal and therefore LOSS. That is why the
        // test must NOT require loss_children>0, which would leave such
        // an edge permanently UNKNOWN.
        if(e.win_children>0) e.verdict=EdgeVerdict::WIN;
        else if(e.unknown_children>0) e.verdict=EdgeVerdict::UNKNOWN;
        else e.verdict=EdgeVerdict::LOSS;
        return e;
    }

    // Canonical key of the four-stone position an edge names. Two edges
    // with the same key are the SAME position under D4, so a single proof
    // covers both. This is why the cover is counted in canonical s4
    // classes rather than in raw edges.
    Bits edge_class_key(int r2,int a,int b) const {
        TState s2{}; s2=add(s2,root_first_move_); s2=add(s2,r2);
        TState s3=add(s2,a);
        TState s4=add(s3,b);
        return canonical(s4);
    }

    // Legal moves after the given occupied points. Used to enumerate
    // SAFE edges: an edge {a,b} is only meaningful when b is a legal
    // fourth reply to a, which is stricter than "four distinct stones"
    // because the resulting four-stone set must contain no FORBIDDEN
    // quadruple, where "forbidden" is the game's concyclic rule (the
    // 4x4 determinant over [x*x+y*y, x, y, 1]) -- not mere collinearity.
    std::vector<int> legal_moves_from(Bits occ) const {
        std::vector<int> out;
        Bits legal=legal_for(occ);
        Bits mm=legal;
        while(any(mm)){
            int z=take_lsb(mm);
            if(z<0) break;
            out.push_back(z);
        }
        return out;
    }

    // ---- ADAPTIVE COORDINATOR for one two-stone reply ---------------
    // The refutation of reply r2 is a set cover over canonical s4
    // classes: a third move a is refuted as soon as ANY incident class is
    // proved LOSS, so refuting the whole reply means covering all vertices
    // with LOSS-proved classes. The all-available structural instance has
    // OPT=31 (certified offline by ILP). After individual classes become WIN,
    // this in-process coordinator uses a deterministic GREEDY cover; its
    // "min_additional" field is therefore a scheduling estimate, not an
    // exact optimum.
    //
    // The coordinator re-solves the optimistic cover after every verdict:
    //     LOSS class    -> usable, cost 0 (already paid for)
    //     UNKNOWN class -> usable, cost 1 (still to be proved)
    //     WIN class     -> FORBIDDEN (can never refute anything)
    // and hands the UNKNOWN members of that cover to workers. Concentrating
    // on the current cover means effort goes only to classes that can
    // still appear in a certificate, rather than to all 3395 remaining.
    // Greedy largest-coverage-first cover over the usable classes, cost 0
    // for a decided LOSS class and 1 for an UNKNOWN one. Cheap and
    // deterministic; the ILP gives the exact optimum offline, and this
    // is only used to decide what to work on next.
    //
    // It reports TWO cover counts. `covered` is the optimistic cover,
    // which counts UNKNOWN classes as usable and therefore reaches all
    // 119 immediately. `secured` counts only vertices covered by PROVED
    // LOSS classes. Victory requires secured == 119; treating the
    // optimistic count as a refutation would be a soundness bug.
    struct CovMemo { std::vector<int> verts; };
    struct CoordStats {
        std::uint64_t cover_size=0;       // UNKNOWN classes in greedy suffix
        std::uint64_t covered=0;          // secured union + optimistic suffix
        std::uint64_t secured=0;          // union of ALL proved LOSS classes
        std::uint64_t min_additional=0;   // greedy UNKNOWN count, not exact ILP
        std::uint64_t forbidden=0;        // classes WIN has ruled out
        std::vector<int> members;         // slots selected by the greedy cover
    };

    CoordStats coordinate(const std::vector<CovMemo>& cov_memo,
                          const std::vector<EdgeVerdict>& verdicts,
                          const std::vector<int>* preferred=nullptr) const {
        const int M=(int)cov_memo.size();
        std::vector<char> covered((std::size_t)V,0);
        CoordStats st;

        // Every proved LOSS class is unconditional proof material, whether or
        // not a later greedy skeleton would happen to select it. Seed the
        // frontier with the UNION of all such classes. This makes secured a
        // true monotone progress measure and lets a completed certificate
        // terminate immediately even if scheduling would choose a different
        // redundant skeleton.
        std::size_t secured_n=0;
        for(int i=0;i<M;++i){
            if(verdicts[(std::size_t)i]!=EdgeVerdict::LOSS) continue;
            for(int v:cov_memo[(std::size_t)i].verts){
                if(!covered[(std::size_t)v]){
                    covered[(std::size_t)v]=1;
                    ++secured_n;
                }
            }
        }
        st.secured=secured_n;
        std::size_t covered_n=secured_n;

        // If an independently verified frontier is supplied, use its still
        // viable UNKNOWN members first.  This preserves an offline-optimized
        // proof skeleton (e.g. the 31-class direct-union frontier) without
        // making it brittle: any member later proved WIN is skipped and the
        // ordinary greedy suffix below repairs whatever coverage is missing.
        std::vector<char> used((std::size_t)M,0);
        if(preferred){
            for(int i:*preferred){
                if(i<0 || i>=M) throw std::runtime_error("preferred frontier slot out of range");
                if(used[(std::size_t)i]) continue;
                used[(std::size_t)i]=1;
                if(verdicts[(std::size_t)i]!=EdgeVerdict::UNKNOWN) continue;
                std::size_t fresh=0;
                for(int v:cov_memo[(std::size_t)i].verts)
                    if(!covered[(std::size_t)v]) ++fresh;
                if(!fresh) continue;
                for(int v:cov_memo[(std::size_t)i].verts){
                    if(!covered[(std::size_t)v]){
                        covered[(std::size_t)v]=1;
                        ++covered_n;
                    }
                }
                st.members.push_back(i);
                ++st.cover_size;
                ++st.min_additional;
            }
        }

        // Cover only still-unsecured vertices with UNKNOWN classes. WIN
        // classes are impossible certificate members. The suffix makes a
        // preferred frontier adaptive rather than mandatory.
        for(int round=0; round<M && covered_n<(std::size_t)V; ++round){
            int best=-1;
            std::size_t best_fresh=0;
            for(int i=0;i<M;++i){
                if(used[(std::size_t)i]) continue;
                if(verdicts[(std::size_t)i]!=EdgeVerdict::UNKNOWN) continue;
                std::size_t fresh=0;
                for(int v:cov_memo[(std::size_t)i].verts)
                    if(!covered[(std::size_t)v]) ++fresh;
                if(fresh>best_fresh){
                    best=i;
                    best_fresh=fresh;
                }
            }
            if(best<0 || best_fresh==0) break;
            used[(std::size_t)best]=1;
            for(int v:cov_memo[(std::size_t)best].verts){
                if(!covered[(std::size_t)v]){
                    covered[(std::size_t)v]=1;
                    ++covered_n;
                }
            }
            st.members.push_back(best);
            ++st.cover_size;
            ++st.min_additional;
        }
        st.covered=covered_n;
        for(int i=0;i<M;++i)
            if(verdicts[(std::size_t)i]==EdgeVerdict::WIN) ++st.forbidden;
        return st;
    }

    // Certificate for one winning two-stone reply. Filled only when the
    // quantified search returns WIN:
    //   reply r2, one winning third move r3, and for EVERY legal fourth
    //   reply r4 a winning fifth move r5 with that s5's canonical key.
    struct Cert5 {
        int r2=-1, r3=-1;
        struct Q4 { int r4=-1, r5=-1; Bits key{}; };
        std::vector<Q4> q4;
    };

    // Run the quantified search for one two-stone root {first,r2}.
    // Exposed so the driver can loop over replies while KEEPING the
    // oracle cache across them: all 20 replies share most of their s5
    // positions, so a per-reply oracle would redo the exact work.
    int quant_root(int first,int r2,std::uint64_t budget,Cert5* cert){
        root_first_move_=first;
        return quant_solve(r2,budget,cert);
    }
    // Enumerate the fifth moves of a 4-stone position WITHOUT solving
    // any of them, reporting per fifth move: index, canonical s5 key,
//    legal count, and whether the main PnTT already holds a verdict.
    //
    // This is what makes the s4-direct A/B interpretable. The direct
    // exact DFS picks children by count-ASC (decisive ones first), the
    // quant solver picks them in board index order, so if their first
    // choices differ then the two arms were never digging the same s5
    // and a node-for-node comparison means nothing.
    struct M5Info { int m5=-1, legal=0, tt_state=0; Bits key{}; };
    std::vector<M5Info> enum_m5_unresolved(int r2,int m3,int m4){
        // A repeated stone is not a position. The earlier A/B spec used
        // m4=0 while r2 was also 0, which built a four-stone "position"
        // with one stone doubled (popcount 4); every number measured on
        // it described an illegal board. Reject such a spec loudly
        // rather than silently analysing nonsense.
        if(root_first_move_==r2||root_first_move_==m3||root_first_move_==m4||
           r2==m3||r2==m4||m3==m4)
            throw std::runtime_error("s4 spec repeats a stone");
        TState s2{}; s2=add(s2,root_first_move_); s2=add(s2,r2);
        TState s3=add(s2,m3);
        TState s4=add(s3,m4);
        Bits occ{}; setbit(occ,root_first_move_); setbit(occ,r2);
        setbit(occ,m3); setbit(occ,m4);
        Bits legal5=legal_for(occ);
        std::vector<M5Info> out;
        Bits mm=legal5;
        while(any(mm)){
            int z=take_lsb(mm);
            if(z<0) break;
            TState s5=add(s4,z);
            Bits o5=occ; setbit(o5,z);
            M5Info info; info.m5=z;
            info.key=canonical(s5);
            info.legal=popcount(legal_for(o5));
            int slot=tt_.find(info.key.lo,info.key.hi);
            info.tt_state=(slot>=0)?(int)tt_.st_[(std::size_t)slot]:0;
            out.push_back(info);
        }
        return out;
    }

    const Oracle& oracle_stats() const { return oracle; }
    int oracle_cached_pub(Bits key) const {
        auto it=oracle.memo.find(key);
        return it==oracle.memo.end()?0:(int)it->second;
    }
    Bits edge_class_key_pub(int r2,int a,int b) const { return edge_class_key(r2,a,b); }
    EdgeInfo classify_edge_pub(int r2,int a,int b) const { return classify_edge(r2,a,b); }
    Bits canonical_pub(const TState& s) const { return canonical(s); }

    // Board helpers exposed for the s4 A/B driver, which has to rebuild
    // the same 4-stone position the quant solver would have reached.
    void set_first_move(int v){ root_first_move_=v; }
    TState add_pub(TState s,int v) const { return add(s,v); }
    void setbit_pub(Bits& b,int v) const { setbit(b,v); }
    Bits legal_for_pub(Bits occ) const { return legal_for(occ); }
    static int popcount_pub(Bits b){
        int n=0; while(any(b)){ if(take_lsb(b)<0) break; ++n; } return n;
    }
    static int take_lsb_pub(Bits& b){ return take_lsb(b); }
    static bool any_pub(Bits b){ return any(b); }

    // Solve one 4-stone position exactly. This is EQUIVALENT to the
    // quant solver's inner "exists m5 : WIN(s5)" step, because an s4
    // position is an OR node and the exact DFS returns on the first
    // child it proves WIN. So it is a drop-in A/B against enumerating
    // the fifth moves one at a time:
    //   - the exact DFS already has the count-ASC ordering, so a WIN
    //     fifth move is found early rather than in index order;
    //   - transpositions between the s5 children are shared inside one
    //     search instead of across separate oracle calls.
    // Returns 1 WIN, 2 LOSS, 0 UNKNOWN (budget exhausted).
    int exact4_oracle(const TState& state,Bits occupied,std::uint64_t budget){
        Bits key=canonical(state);
        auto it=oracle.memo.find(key);
        if(it!=oracle.memo.end()){
            ++oracle.hits; ++oracle.queries;
            return it->second;
        }
        ++oracle.queries;
        Bits legal=legal_for(occupied);
        std::uint64_t b=budget;
        std::uint64_t before=exact_nodes_;
        double t0=std::chrono::duration<double>(
            Clock::now().time_since_epoch()).count();
        if(quant_progress_){
            *log_<<"[s4-start] q="<<oracle.queries<<" key="<<key.lo<<","<<key.hi
                <<" legal="<<popcount(legal)<<" budget="<<budget<<std::endl;
            log_->flush();
        }
        ExactResult r=exact_prop(state,4,legal,b);
        double t1=std::chrono::duration<double>(
            Clock::now().time_since_epoch()).count();
        oracle.nodes+=exact_nodes_-before;
        oracle.wall+=std::uint64_t((t1-t0)*1000.0);
        if(quant_progress_){
            *log_<<"[s4-done]  q="<<oracle.queries<<" key="<<key.lo<<","<<key.hi
                <<" result="<<(r==ExactResult::WIN?1:(r==ExactResult::LOSS?2:0))
                <<" nodes="<<(exact_nodes_-before)
                <<" ms="<<(long long)((t1-t0)*1000.0)<<std::endl;
            log_->flush();
        }
        if(r==ExactResult::WIN){ oracle.memo[key]=1; ++oracle.wins; return 1; }
        if(r==ExactResult::LOSS){ oracle.memo[key]=2; ++oracle.losses; return 2; }
        ++oracle.unknowns;
        return 0;
    }

    // Reconstruct the 4-stone position reached by first move, second
    // reply, third move and fourth reply, and solve it exactly.
    // Returns the exact verdict (1 WIN, 2 LOSS, 0 UNKNOWN) plus the
    // winning fifth move when there is one.
    int s4_direct(int r2,int m3,int m4,std::uint64_t budget,int* winning_m5){
        if(root_first_move_==r2||root_first_move_==m3||root_first_move_==m4||
           r2==m3||r2==m4||m3==m4)
            throw std::runtime_error("s4 spec repeats a stone");
        typename DfPn<N>::TState s2{}; s2=add(s2,root_first_move_); s2=add(s2,r2);
        typename DfPn<N>::TState s3=add(s2,m3);
        typename DfPn<N>::TState s4=add(s3,m4);
        Bits occ{}; setbit(occ,root_first_move_); setbit(occ,r2);
        setbit(occ,m3); setbit(occ,m4);
        int res=exact4_oracle(s4,occ,budget);
        if(winning_m5) *winning_m5=-1;
        if(res==1){
            // Recover a concrete winning fifth move from the stored
            // table so the certificate stays checkable.
            Bits legal5=legal_for(occ);
            Bits m=legal5;
            while(any(m)){
                int z=take_lsb(m);
                if(z<0) break;
                typename DfPn<N>::TState s5=add(s4,z);
                int slot=tt_.find(canonical(s5).lo,canonical(s5).hi);
                if(slot>=0 && tt_.st_[(std::size_t)slot]==PnTT::WIN){
                    if(winning_m5) *winning_m5=z;
                    break;
                }
            }
        }
        return res;
    }

    // ---- QUANTIFIED s5 SEARCH  (exists m3 forall m4 exists m5) ----
    // A two-stone root {m2,r2} is an OR node: to show the ORIGINAL
    // FIRST PLAYER wins it, ONE winning third move suffices. A
    // three-stone position is an AND node: every legal fourth reply
    // must be held. A four-stone position is an OR node again: one
    // winning fifth move per fourth reply.
    //
    //   two-stone r2  =  exists m3 : forall m4 : exists m5 : s5 WIN
    //
    // Solving it directly with a generic exact DFS would throw away
    // the structure we already paid for: the s5 layer is solved by an
    // exact oracle, so the search only has to decide three levels.
    // Nothing here touches proof numbers or thresholds; each step is a
    // direct evaluation of the quantifier formula.
    //
    // Returns 1 WIN, 2 LOSS, 0 UNKNOWN (a budget ran out somewhere).
    // `cert` is filled only on a WIN.
    int quant_solve(int r2,std::uint64_t budget,Cert5* cert){
        typename DfPn<N>::TState s2{}; s2=add(s2,root_first_move_); s2=add(s2,r2);
        Bits occ2{}; setbit(occ2,root_first_move_); setbit(occ2,r2);
        Bits legal3=legal_for(occ2);
        int n3=popcount(legal3);
        // A third move is refuted as soon as ONE fourth reply is
        // refuted (exists m4, forall m5 LOSS); it is proved only when
        // every fourth reply is SAT (forall m4, exists m5 WIN). If some
        // fourth reply is UNKNOWN the third move is neither proved nor
        // refuted, and the reply as a whole must stay UNKNOWN.
        //
        // Unknowns are tracked by q_m3_unknown_, NOT by a reply-wide
        // flag. The previous code kept a local saw_unknown that nothing
        // ever set, so the final "saw_unknown ? 0 : 2" always chose 2
        // and reported a LOSS even when a third move had been left
        // inconclusive. That is an unsound refutation, and the per-m3
        // counter is what the verdict must consult.
        //
        // Branch-level telemetry. The whole feasibility question turns
        // on how quickly each level short-circuits, so record it rather
        // than inferring it from total query counts.
        q_m3_tried_=0; q_m4_sat_=0; q_m4_refuted_=0; q_m4_unknown_=0;
        q_m3_refuted_=0; q_m3_unknown_=0; q_m4_sat_total_=0;
        q_queries_at_refute_=0;
        for(int i=0;i<n3;++i){
            int v=take_lsb(legal3);
            if(v<0) break;
            if(quant_out_of_time()) return 0;
            ++q_m3_tried_;
            std::uint64_t q_at_m3=oracle.queries;
            typename DfPn<N>::TState s3=add(s2,v);
            Bits occ3=occ2; setbit(occ3,v);
            Bits legal4=legal_for(occ3);
            int n4=popcount(legal4);
            bool all=true;
            std::vector<typename Cert5::Q4> rows;
            rows.reserve((std::size_t)n4);
            // Progress heartbeat. The exists-m3 loop can run for a very
            // long time, and a run that produces NO output until it
            // finishes is indistinguishable from a hang, so report the
            // oracle counters as they move.
            if(quant_progress_){
                const auto& oc=oracle;
                *log_<<"[quant] r2="<<r2<<" m3="<<v<<" ("<<(i+1)<<"/"<<n3
                    <<") queries="<<oc.queries<<" hits="<<oc.hits
                    <<" nodes="<<oc.nodes<<std::endl;
                log_->flush();
            }
            // Per fourth reply, the verdict is three-valued and computed from
            // THAT reply alone:
            //   SAT      some fifth move came back WIN
            //   REFUTED  no WIN, and every legal fifth move a proven LOSS
            //   UNKNOWN  no WIN, but at least one fifth move inconclusive
            // Mixing a reply-wide flag into this was wrong: one
            // inconclusive query bumps oracle.queries, so the previous
            // form counted an UNKNOWN m4 as REFUTED, and an UNKNOWN seen
            // under an earlier m3 leaked into the classification of later
            // ones.
            enum class M4Verdict : std::uint8_t { SAT=0, REFUTED=1, UNKNOWN=2 };
            int m4_sat=0, m4_refuted=0, m4_unknown=0;
            bool m3_refuted=false, m3_unknown=false;
            for(int j=0;j<n4;++j){
                int w=take_lsb(legal4);
                if(w<0) break;
                typename DfPn<N>::TState s4=add(s3,w);
                Bits occ4=occ3; setbit(occ4,w);
                Bits legal5=legal_for(occ4);
                int n5=popcount(legal5);
                bool found=false;
                bool m4_unk=false;
                for(int k=0;k<n5;++k){
                    int z=take_lsb(legal5);
                    if(z<0) break;
                    typename DfPn<N>::TState s5=add(s4,z);
                    Bits occ5=occ4; setbit(occ5,z);
                    int r=s5_oracle(s5,occ5,budget);
                    if(r<0) return 0;             // wall allowance exhausted
                    if(r==1){ typename Cert5::Q4 row; row.r4=w; row.r5=z; row.key=canonical(s5);
                              rows.push_back(row); found=true; break; }
                    // r==2 (this fifth move loses) -> try another
                    if(r==0){ m4_unk=true; break; }
                }
                if(found){ ++m4_sat; ++q_m4_sat_; continue; }
                if(m4_unk){
                    ++m4_unknown; m3_unknown=true;
                    ++q_m4_unknown_;
                    // An m4 that is UNKNOWN cannot be a proof and cannot
                    // refute the m3 either, so keep scanning: a later m4
                    // may still be REFUTED, which is the stronger outcome.
                    continue;
                }
                ++m4_refuted;
                ++q_m4_refuted_;
                m3_refuted=true;
                if(q_queries_at_refute_==0)
                    q_queries_at_refute_=oracle.queries-q_at_m3;
                break;   // exists m4 with forall m5 LOSS: m3 is dead
            }
            if(m3_refuted){ ++q_m3_refuted_; continue; }
            if((int)rows.size()!=n4||m3_unknown){
                // Reaching here with rows.size()==n4 and no unknown
                // would mean the m4 loop ended without either a
                // refutation or a full set of SAT rows, which the loop
                // structure does not allow. If it ever did happen the
                // safe reading is UNKNOWN, so treat it as such rather
                // than as a proof.
                ++q_m3_unknown_;
                if(!m3_unknown) ++q_m4_unknown_;
                continue;                       // not a proof
            }
            // Every fourth reply was SAT: this third move is proved.
            q_m4_sat_total_+=m4_sat;
            if(cert){
                cert->r2=r2; cert->r3=v; cert->q4=rows;
            }
            return 1; // exists m3 satisfied
        }
        // Every third move was examined and none was proved. The reply
        // is REFUTED only if each one was refuted outright, i.e. by a
        // single fourth reply whose every fifth move was a proven LOSS.
        // If any third move was left UNKNOWN the reply is merely
        // unproven. This must consult q_m3_unknown_, which is the only
        // counter that records that; the reply-wide flag this used to
        // use was never set, so it always answered LOSS.
        if(q_m3_unknown_>0) return 0;
        return 2;
    }

    // Branch telemetry accessors, for the driver to report.
    std::uint64_t q_m3_tried() const { return q_m3_tried_; }
    std::uint64_t q_m3_refuted() const { return q_m3_refuted_; }
    std::uint64_t q_m4_sat() const { return q_m4_sat_; }
    std::uint64_t q_m4_refuted() const { return q_m4_refuted_; }
    std::uint64_t q_m4_unknown() const { return q_m4_unknown_; }
    std::uint64_t q_queries_at_refute() const { return q_queries_at_refute_; }
    std::uint64_t q_m3_unknown() const { return q_m3_unknown_; }
    std::uint64_t q_m4_sat_total() const { return q_m4_sat_total_; }

    std::uint64_t forbidden_count() const { return forbidden_count_; }
    std::uint64_t visited() const { return visited_; }
    std::uint64_t expansions() const { return expanded_; }

private:
    std::array<std::array<Bits,V>,8> tbit_{};
    PnTT tt_;
    std::vector<Bits> completion_;
    std::vector<std::array<int,4>> forbidden_quads_;
    std::uint64_t forbidden_count_=0,visited_=0,expanded_=0;
    std::uint64_t exp_hist_[64]={};
    int max_depth_=0;
    double deadline_s_=0;
    Clock::time_point t0_;
    // Heartbeat rate state (per-solver, reset per root in solve_common).
    std::uint64_t hb_last_vis_=0;
    double hb_last_t_=0;
    double hb_prev_t_=0;
    std::uint64_t hb_prev_exp_=0;
    Bits root_key_{};
    int root_stones_=0;
    // Partial-progress fallback: written by the catch in solve_common when
    // mid() throws (TIME_BUDGET), read by the run_one() handler.
    std::uint32_t r_exp_fallback_pn=INF, r_exp_fallback_dn=INF;
    std::uint64_t r_exp_fallback_exp=0, r_exp_fallback_vis=0;

    // CHILD WORK: per direct child of the ROOT, keyed by the
    // child's canonical Bits (NOT a hash -- lo*const+hi collides
    // and produced 970 phantom "children" for a 20-child root).
    // work = number of times the search DESCENDED into this child
    // from the root (b1==this child at a root re-aggregation);
    // pn/dn/st = the child's CURRENT stored bounds; legal/count =
    // its legal-move count. Only populated when track_children_
    // is set (the diagnostic mode), because the per-child
    // bookkeeping would slow the main runs.
    struct ChildStat {
        std::uint64_t work=0;
        std::uint32_t pn=INF, dn=INF;
        std::uint8_t st=0;
        int count=0;
        int move=-1;
    };
    std::map<Bits,ChildStat> child_stat_;
    std::uint64_t child_stat_updates_=0;
    bool track_children_=false;

    // Create-or-update one child observation for the root-child
    // diagnostic. Called from gen_into when track_children_ is
    // set AND the parent is the root (is_root passed explicitly).
    // work is NOT touched here (it is accumulated at descent
    // time by add_child_work); pn/dn/st/count/move are refreshed.
    void note_child(const Bits& key,int move,int count,
                    std::uint32_t pn,std::uint32_t dn,std::uint8_t st){
        if(!track_children_) return;
        auto it=child_stat_.find(key);
        if(it==child_stat_.end()){
            ChildStat cs; cs.pn=pn; cs.dn=dn; cs.st=st;
            cs.count=count; cs.move=move;
            child_stat_[key]=cs;
        }else{
            it->second.pn=pn; it->second.dn=dn; it->second.st=st;
            it->second.count=count;
            if(move>=0) it->second.move=move;
        }
        ++child_stat_updates_;
    }

    // Accumulate one descent into the child with the given key.
    // Called from mid_iter when the search pushes a child frame
    // whose parent is the root.
    void add_child_work(const Bits& key){
        if(!track_children_) return;
        auto it=child_stat_.find(key);
        if(it!=child_stat_.end()) it->second.work += 1;
    }

    // Print the root-child diagnostic: one line per direct child of
    // the root, ranked by work descending. Fields: move, pn, dn,
    // solved status, cumulative work, legal count. The ranking
    // answers "which of the 20 replies dominates the proof search"
    // without waiting for the root to solve. The v=11 one-stone root
    // has 20 D4-distinct children; a larger n child count means the
    // map accumulated children of deeper frames too (should not
    // happen -- the guard is stones_==root_stones_ in note_child).
    void dump_children(){
        if(child_stat_.empty()){ *log_<<"[children] n=0\n"; return; }
        std::vector<std::pair<Bits,ChildStat>> v;
        v.reserve(child_stat_.size());
        for(auto& kv:child_stat_) v.push_back({kv.first,kv.second});
        std::sort(v.begin(),v.end(),
            [](const std::pair<Bits,ChildStat>& a,
               const std::pair<Bits,ChildStat>& b){
                if(a.second.work!=b.second.work)
                    return a.second.work>b.second.work;
                return a.second.pn<b.second.pn;
            });
        *log_ << "[children] t=" << (long long)std::chrono::duration<double>(
            Clock::now()-t0_).count() << "s n=" << v.size()
              << " updates=" << child_stat_updates_ << "\n";
        for(auto& kv:v){
            const ChildStat& cs=kv.second;
            *log_ << "  move=" << cs.move
                  << " pn=" << cs.pn << " dn=" << cs.dn
                  << " st=" << (int)cs.st
                  << " work=" << cs.work
                  << " legal=" << cs.count << "\n";
        }
        log_->flush();
    }

    // TIE-BREAK between children with EQUAL proof number, applied only
    // when the numbers are equal (so it can never change correctness --
    // b1 is only ever a choice of which equally-bounded child to dig
    // first). Ties are extremely common early in a search, which is
    // why the tie-break has outsized influence on the order in which
    // subproofs are visited.
    //
    // Modes (--tiebreak=):
    //   asc  (0, default) legal count ASC,  then canonical key ASC
    //   desc (1)         legal count DESC, then canonical key DESC

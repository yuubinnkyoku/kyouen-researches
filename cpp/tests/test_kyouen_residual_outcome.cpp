// Check the handoff trust boundary, not just the standalone P/N recursion.
#define KYOUEN_DFPN_NO_MAIN
#include "../solvers/kyouen_dfpn_root.cpp"
#include <cassert>
int main(){
    DfPn<4> native(16),limited(16);
    std::uint64_t native_nodes=0,used=0;
    assert(native.exact_replay(Bits{},0,5000,native_nodes)==2);
    limited.set_residual_exact_legal(16);
    limited.set_residual_outcome(true,1);
    // The aborted root must not appear as solved in either board cache.
    assert(limited.exact_replay(Bits{},0,0,used)==0 && used==0);
    std::uint64_t nodes,cutoffs,aborts,remaining;
    limited.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==1 && aborts==1 && remaining==0);
    // Same solver and same root; a fresh quota is available, then fallback
    // must reproduce the native result and visited board-node count.
    assert(limited.exact_replay(Bits{},0,5000,used)==2 && used==native_nodes);
    limited.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==1 && aborts==1 && remaining==0);
    // A genuinely solved TT entry can be reused; P/N counters reset per root.
    assert(limited.exact_replay(Bits{},0,5000,used)==2 && used==0);
    limited.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==0 && aborts==0 && remaining==1);
    DfPn<4> disabled(16);
    disabled.set_residual_exact_legal(16);
    disabled.set_residual_outcome(true,0);
    assert(disabled.exact_replay(Bits{},0,5000,used)==2 && used==native_nodes);
    std::cout<<"VERIFIED outcome quota reset, aborted-root cache safety, native fallback and solved TT reuse\n";
}

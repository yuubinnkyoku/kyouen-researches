#define KYOUEN_DFPN_NO_MAIN
#include "../solvers/kyouen_dfpn_root.cpp"
#include <cassert>

static void silence(DfPn<4>& s,std::ostringstream& out){s.attach_log(out);s.attach_csv(out);}
static void exhaust(DfPn<4>& s){
    bool stopped=false;
    try{s.solve_empty();}catch(const std::runtime_error& e){stopped=std::string(e.what())=="NODE_BUDGET";}
    assert(stopped);
}
int main(){
    std::ostringstream out;
    ResidualOptions options;
    options.exact_legal=16;options.outcome=true;options.outcome_budget=128;options.attempt_budget=1;
    DfPn<4> capped(16);silence(capped,out);capped.configure_residual(options);
    capped.set_search_node_budget(1);exhaust(capped);
    std::uint64_t nodes,cutoffs,aborts,remaining;
    capped.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==1 && aborts==1 && remaining==127 && capped.residual_attempted()==1);
    // A second normal root must not inherit the failed attempt suppression.
    auto before=capped.residual_exact_calls();exhaust(capped);
    capped.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==1 && aborts==1 && remaining==127 && capped.residual_attempted()==1);
    assert(capped.residual_exact_calls()==before+1);
    // UNKNOWN has not solved/poisoned the root. Native fallback completes
    // the independently known n4 empty-board LOSS, with the quota bounded.
    capped.set_search_node_budget(20000);
    assert(capped.solve_empty().outcome==-1);
    capped.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes+remaining==128 && nodes<=128 && aborts>1);
    assert(capped.residual_attempted()==nodes); // each admitted cap1 call costs one
    // Global remainder also truncates a per-attempt cap larger than itself.
    DfPn<4> remainder(16);silence(remainder,out);
    auto small=options;small.outcome_budget=3;small.attempt_budget=8;
    remainder.configure_residual(small);remainder.set_search_node_budget(1);exhaust(remainder);
    remainder.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==3 && remaining==0 && aborts==1 && remainder.residual_attempted()==1);
    // A native exact handoff on the same open board must skip its already
    // attempted residual state rather than consuming a second slice there.
    DfPn<4> hybrid(16);silence(hybrid,out);hybrid.configure_residual(options);
    hybrid.set_exact_handoff(16,1,1,0);hybrid.set_search_node_budget(2);exhaust(hybrid);
    assert(hybrid.residual_attempt_skips()>0);
    assert(hybrid.residual_exact_calls()==hybrid.residual_attempted());
    hybrid.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==hybrid.residual_attempted() && nodes+remaining==128);
    // Both turn parities still publish completed outcomes with a tiny cap.
    for(auto root:{std::vector<int>{0,1,2,4,9},std::vector<int>{0,1,3,5,8,14}}){
        Bits occupied{};for(int v:root)setbit(occupied,v);
        DfPn<4> reference(16),normal(16);silence(reference,out);silence(normal,out);
        std::uint64_t used=0;int expected=reference.exact_replay(occupied,(int)root.size(),5000,used);
        normal.configure_residual(options);normal.set_search_node_budget(1);
        assert(normal.solve_root(root).outcome==(expected==1?1:-1));
        normal.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
        assert(nodes==1 && aborts==0 && remaining==127 && normal.residual_attempted()==1);
        assert(normal.solve_root(root).outcome==(expected==1?1:-1));
        normal.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
        assert(nodes==0 && remaining==128 && normal.residual_attempted()==0 && normal.residual_attempt_skips()==0);
    }
    std::cout<<"VERIFIED per-attempt cap, root quota conservation/reset, UNKNOWN safety, hybrid duplicate suppression and both turn parities\n";
}

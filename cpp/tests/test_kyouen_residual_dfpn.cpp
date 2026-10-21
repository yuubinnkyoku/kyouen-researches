#define KYOUEN_DFPN_NO_MAIN
#include "../solvers/kyouen_dfpn_root.cpp"
#include <cassert>
static void silence(DfPn<4>& solver,std::ostringstream& sink){solver.attach_log(sink);solver.attach_csv(sink);}
static void exhaust(DfPn<4>& solver,const std::vector<int>& root){
    bool stopped=false;
    try{solver.solve_root(root);}catch(const std::runtime_error& e){stopped=std::string(e.what())=="NODE_BUDGET";}
    assert(stopped);
}
int main(){
    std::ostringstream sink;
    ResidualOptions options;options.exact_legal=6;options.outcome=true;options.outcome_budget=128;
    options.audit_legal=options.crosscheck_legal=6;
    // Both original turn parities. Only two legal points remain.
    for(auto root:{std::vector<int>{0,1,2,4,9},std::vector<int>{0,1,3,5,8,14}}){
        Bits occupied{};for(int v:root)setbit(occupied,v);
        DfPn<4> reference(16),normal(16);silence(reference,sink);silence(normal,sink);
        std::uint64_t used=0;
        int expected=reference.exact_replay(occupied,(int)root.size(),5000,used);
        assert(expected==1 || expected==2);
        normal.configure_residual(options);normal.set_search_node_budget(1);
        auto result=normal.solve_root(root);
        assert(result.outcome==(expected==1?1:-1));
        assert(result.expansions==0 && normal.search_nodes_used()==1 && normal.exact_total_nodes()==0);
        std::uint64_t nodes,cutoffs,aborts,remaining;
        normal.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
        assert(nodes==1 && remaining==127 && aborts==0);
        assert(normal.residual_audit_calls()>0);
        result=normal.solve_root(root); // solved TT reuse, quota resets per root
        assert(result.outcome==(expected==1?1:-1) && normal.search_nodes_used()==1);
        normal.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
        assert(nodes==0 && remaining==128);
        DfPn<4> disabled(16);silence(disabled,sink);
        auto zero=options;zero.outcome_budget=0;
        disabled.configure_residual(zero);disabled.set_search_node_budget(20000);
        assert(disabled.solve_root(root).outcome==(expected==1?1:-1));
        assert(disabled.residual_exact_calls()==0);
    }
    // An unresolved P/N root cannot poison PnTT; the next larger-budget
    // normal solve must actually prove the known n4 result.
    DfPn<4> limited(16);silence(limited,sink);
    auto small=options;small.exact_legal=16;small.outcome_budget=1;
    small.audit_legal=small.crosscheck_legal=0;
    limited.configure_residual(small);limited.set_search_node_budget(1);
    exhaust(limited,{});assert(limited.search_nodes_used()==1);
    std::uint64_t nodes,cutoffs,aborts,remaining;
    limited.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
    assert(nodes==1 && aborts==1 && remaining==0);
    limited.set_search_node_budget(20000);
    assert(limited.solve_empty().outcome==-1 && limited.search_nodes_used()>1);
    // Zero is an actual cap. The scope ends after the exception, so an
    // independent exact replay on the same solver retains its own budget.
    DfPn<4> zero(16);silence(zero,sink);zero.set_search_node_budget(0);
    exhaust(zero,{});assert(zero.search_nodes_used()==0);
    std::uint64_t exact_used=0;
    assert(zero.exact_replay(Bits{},0,5000,exact_used)==2 && exact_used>0);
    assert(zero.search_nodes_used()==0);
    // Existing exact handoffs consume the SAME normal-search work budget.
    DfPn<4> hybrid(16);silence(hybrid,sink);
    hybrid.set_exact_handoff(16,100000,1,0);hybrid.set_search_node_budget(7);
    exhaust(hybrid,{});
    assert(hybrid.search_nodes_used()==7);
    assert(hybrid.visited()+hybrid.exact_total_nodes()==7 && hybrid.exact_total_nodes()>0);
    hybrid.clear_search_node_budget();assert(hybrid.solve_empty().outcome==-1);
    std::cout<<"VERIFIED df-pn direct handoff, turn parity, quota reset/fallback, cache safety, zero cap and shared exact-node budget\n";
}

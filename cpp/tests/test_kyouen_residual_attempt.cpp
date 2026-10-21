#define KYOUEN_DFPN_NO_MAIN
#include "../solvers/kyouen_dfpn_root.cpp"
#include <cassert>

static void silence(DfPn<4>& s,std::ostringstream& out){s.attach_log(out);s.attach_csv(out);}
static void exhaust(DfPn<4>& s){
    bool stopped=false;
    try{s.solve_empty();}catch(const std::runtime_error& e){stopped=std::string(e.what())=="NODE_BUDGET";}
    assert(stopped);
}
static bool circle_or_line(const std::array<int,4>& q){
    // Independent integer determinant, no solver completion/residual code.
    std::array<std::array<int,3>,3> rows{};
    const int x=q[0]%4,y=q[0]/4,r=x*x+y*y;
    for(int i=0;i<3;++i){
        int a=q[i+1]%4,b=q[i+1]/4;
        rows[i]={a-x,b-y,a*a+b*b-r};
    }
    auto a=rows[0],b=rows[1],c=rows[2];
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])==0;
}
static std::uint64_t independent_n4_audit(){
    std::vector<unsigned> quads;
    for(int a=0;a<16;++a)for(int b=a+1;b<16;++b)
    for(int c=b+1;c<16;++c)for(int d=c+1;d<16;++d)
        if(circle_or_line({a,b,c,d})) quads.push_back((1u<<a)|(1u<<b)|(1u<<c)|(1u<<d));
    // Direct occupied-subset P/N DP: no kernel reductions or TT.
    std::array<int,1<<16> outcome{};outcome.fill(-1);
    std::uint64_t safe=0,checks=0;
    for(int mask=(1<<16)-1;mask>=0;--mask){
        if(std::any_of(quads.begin(),quads.end(),[&](unsigned q){return (unsigned(mask)&q)==q;})) continue;
        ++safe;outcome[mask]=0;
        for(int v=0;v<16;++v)
            if(!(mask&(1<<v)) && outcome[mask|(1<<v)]==0) outcome[mask]=1;
    }
    assert(safe==5811);
    for(int mask=0;mask<(1<<16);++mask){
        if(outcome[mask]<0) continue;
        std::vector<int> root;for(int v=0;v<16;++v)if(mask&(1<<v))root.push_back(v);
        const int expected=((outcome[mask]!=0)==(root.size()%2==0))?1:-1;
        for(std::uint64_t cap:{1ULL,32ULL}){
            // Fresh solver/TT makes every safe board exercise the policy.
            DfPn<4> solver(12);std::ostringstream quiet;silence(solver,quiet);
            ResidualOptions options;options.exact_legal=16;options.outcome=true;
            options.outcome_budget=128;options.attempt_budget=cap;
            solver.configure_residual(options);solver.set_search_node_budget(20000);
            assert(solver.solve_root(root).outcome==expected);
            std::uint64_t nodes,cutoffs,aborts,remaining;
            solver.residual_outcome_stats(nodes,cutoffs,aborts,remaining);
            assert(nodes+remaining==128 && solver.residual_attempt_max_nodes()<=cap);
            assert(solver.residual_exact_calls()==solver.residual_attempted());
            ++checks;
        }
    }
    return checks;
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
    auto checks=independent_n4_audit();
    assert(checks==11622);
    std::cout<<"VERIFIED per-attempt cap, root quota conservation/reset, UNKNOWN safety, hybrid duplicate suppression, both turn parities; independent_n4="<<checks<<"\n";
}

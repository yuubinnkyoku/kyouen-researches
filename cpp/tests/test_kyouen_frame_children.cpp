#define KYOUEN_DFPN_NO_MAIN
#include "../solvers/kyouen_dfpn_root.cpp"
#include <cassert>

static bool forbidden4(int a,int b,int c,int d){
    auto row=[](int p){int x=p%4,y=p/4;return std::array<int,3>{x,y,x*x+y*y};};
    auto base=row(a),x=row(b),y=row(c),z=row(d);
    for(int i=0;i<3;++i){x[i]-=base[i];y[i]-=base[i];z[i]-=base[i];}
    return x[0]*(y[1]*z[2]-y[2]*z[1])-x[1]*(y[0]*z[2]-y[2]*z[0])+x[2]*(y[0]*z[1]-y[1]*z[0])==0;
}
struct Capture {
    int outcome=0;std::uint32_t pn=0,dn=0;
    std::uint64_t nodes=0,exp=0,exact=0,open_ev=0,solved_ev=0,builds=0,moves=0,refresh=0,audits=0,expand_uses=0;
    std::array<std::uint64_t,6> residual{};
    std::string children;
    auto logical()const{return std::tuple{outcome,pn,dn,nodes,exp,exact,open_ev,solved_ev,residual,children};}
};
static Capture solve(DfPn<4>& s,const std::vector<int>& root,std::uint64_t limit){
    std::ostringstream sink;s.attach_log(sink);s.attach_csv(sink);s.set_search_node_budget(limit);
    Capture a;
    try{auto r=s.solve_root(root);a.outcome=r.outcome;a.pn=r.root_pn;a.dn=r.root_dn;}
    catch(const std::runtime_error& e){
        assert(std::string(e.what())=="NODE_BUDGET");
        std::uint64_t exp,vis;s.partial_progress(a.pn,a.dn,exp,vis);
    }
    a.nodes=s.search_nodes_used();a.exp=s.expansions();a.exact=s.exact_total_nodes();
    s.memo_evictions(a.open_ev,a.solved_ev);
    s.residual_outcome_stats(a.residual[0],a.residual[1],a.residual[2],a.residual[3]);
    a.residual[4]=s.residual_attempted();a.residual[5]=s.residual_attempt_skips();
    s.frame_children_stats(a.builds,a.moves,a.refresh,a.audits);a.expand_uses=s.frame_expand_uses();
    std::istringstream input(sink.str());std::string line;
    while(std::getline(input,line)) if(line.starts_with("  move=")) a.children+=line+'\n';
    return a;
}
int main(){
    std::vector<unsigned> quads;
    for(int a=0;a<16;++a)for(int b=a+1;b<16;++b)for(int c=b+1;c<16;++c)for(int d=c+1;d<16;++d)
        if(forbidden4(a,b,c,d))quads.push_back((1u<<a)|(1u<<b)|(1u<<c)|(1u<<d));
    std::array<int,1<<16> dp;dp.fill(-1);
    for(int mask=(1<<16)-1;mask>=0;--mask){
        if(std::any_of(quads.begin(),quads.end(),[&](unsigned q){return (unsigned(mask)&q)==q;}))continue;
        dp[mask]=0;
        for(int v=0;v<16;++v)if(!(mask&(1<<v)) && dp[mask|(1<<v)]==0)dp[mask]=1;
    }
    std::uint64_t checked=0,audited=0,expanded_audited=0;
    for(int mask=0;mask<(1<<16);++mask){
        if(dp[mask]<0)continue;
        std::vector<int> root;for(int v=0;v<16;++v)if(mask&(1<<v))root.push_back(v);
        DfPn<4> off(12),cached(12),expanded(12);cached.set_frame_children_cache(true,true);
        expanded.set_frame_children_cache(true,true,true);
        auto a=solve(off,root,20000),b=solve(cached,root,20000),c=solve(expanded,root,20000);
        assert(a.logical()==b.logical() && a.logical()==c.logical());
        assert(c.refresh==c.audits);expanded_audited+=c.audits;
        assert(a.outcome==(((dp[mask]!=0)==(root.size()%2==0))?1:-1));
        assert(b.refresh==b.audits);audited+=b.audits;++checked;
    }
    assert(checked==5811 && audited>0);
    std::uint64_t evictions=0;
    for(unsigned memo:{5u,12u})for(bool desc:{false,true})for(bool hybrid:{false,true}){
        DfPn<4> off(memo),cached(memo),expanded(memo);cached.set_frame_children_cache(true);
        expanded.set_frame_children_cache(true,false,true);
        off.set_tiebreak_desc(desc);cached.set_tiebreak_desc(desc);expanded.set_tiebreak_desc(desc);
        off.set_track_children(true);cached.set_track_children(true);expanded.set_track_children(true);
        if(hybrid){off.set_exact_handoff(8,8,1,0);cached.set_exact_handoff(8,8,1,0);expanded.set_exact_handoff(8,8,1,0);}
        auto a=solve(off,{},2000),b=solve(cached,{},2000),c=solve(expanded,{},2000);
        assert(a.logical()==c.logical());
        assert(c.expand_uses>0 && b.builds==c.builds+c.expand_uses);
        assert(c.refresh==b.refresh+c.expand_uses);
        assert(a.logical()==b.logical());assert(b.refresh>0 && b.audits==0);
        assert(b.builds<a.builds && b.moves<a.moves);
        evictions+=b.open_ev+b.solved_ev;
        // Bounds/geometry are root-local even when the table is reused.
        auto again=solve(cached,{0,1,2,4,9},2000);
        assert(again.outcome==1 || again.outcome==-1);
    }
    assert(evictions>0);
    std::uint64_t combinations=0,resumes=0;
    const std::vector<std::vector<int>> roots={{},{0},{0,1,2,4,9},{0,1,3,5,8,14}};
    for(unsigned memo:{5u,12u})for(bool desc:{false,true})for(int publish:{0,1,2})
    for(int residual_mode:{0,1,2,3})for(const auto& root:roots){
        unsigned mask=0;for(int v:root)mask|=1u<<v;
        assert(dp[mask]>=0);
        const int expected=((dp[mask]!=0)==(root.size()%2==0))?1:-1;
        DfPn<4> off(memo),expanded(memo);
        for(auto solver:{&off,&expanded}){
            solver->set_tiebreak_desc(desc);solver->set_track_children(true);
            solver->set_exact_handoff(8,8,2,publish);
            ResidualOptions options;
            options.exact_legal=residual_mode==3?16:(residual_mode?6:0);
            options.outcome=residual_mode>=2;options.outcome_budget=residual_mode==3?23:128;
            options.attempt_budget=residual_mode==3?8:0;
            solver->configure_residual(options);
        }
        expanded.set_frame_children_cache(true,true,true);
        auto a=solve(off,root,7),b=solve(expanded,root,7);
        assert(a.logical()==b.logical());
        assert(a.outcome==0 || a.outcome==expected);
        assert(b.refresh==b.audits);
        // Both local exact caches and root P/N quotas survive/reset according
        // to their own contracts after a partial normal solve.
        a=solve(off,root,2000);b=solve(expanded,root,2000);
        assert(a.logical()==b.logical());
        assert(a.outcome==0 || a.outcome==expected);
        assert(b.refresh==b.audits);
        ++combinations;++resumes;
    }
    assert(combinations==192 && resumes==192);
    std::cout<<"VERIFIED independent_n4="<<checked<<" refreshed_lists="<<audited
             <<" expanded_audits="<<expanded_audited<<" eviction_events="<<evictions<<" combinations="<<combinations<<" resumes="<<resumes<<"; identical bounds, work, diagnostics, both tie orders and hybrid exact\n";
}

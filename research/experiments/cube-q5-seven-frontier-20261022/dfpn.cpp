// Proof-number guided search on the same geometry and exact checkpoint format.
// Unknown proof numbers schedule work; only completed AND/OR nodes enter memo.
#define main q5_dfs_main
#include "solver.cpp"
#undef main

class Dfpn: public Solver {
    using PN=__uint128_t;
    static constexpr PN INF=PN(1)<<124;
    struct Numbers {PN pn=1,dn=1;};
    struct Node {std::vector<Mask> children;Numbers value;};
    std::unordered_map<Mask,Node,Hash> tree;
    Numbers status(const Mask& mask)const {
        auto exact=memo.find(mask);
        if(exact!=memo.end())return exact->second.win?Numbers{0,INF}:Numbers{INF,0};
        auto it=tree.find(mask);
        // Positive cost prior, never a label or a bound on game length.
        // Scaling by remaining depth avoids expanding an entire shallow layer
        // before completing any deeper child. Values remain strictly finite.
        PN cost=1;
        for(int k=mask.count();k<(side==7?17:9);k++) {
            if(cost>=(INF/2)/PN(n+1)){cost=INF/2;break;}
            cost*=PN(n+1);
        }
        return it==tree.end()?Numbers{cost,cost}:it->second.value;
    }
    Numbers update(const Mask& mask,Node& node) {
        PN pn=INF,dn=0;Mask witness;
        for(const auto& child:node.children) {
            Numbers s=status(child);
            if(s.dn<pn){pn=s.dn;witness=child;}
            dn=std::min(INF,dn+s.pn);
        }
        node.value={pn,dn};
        if(pn==0)memo.emplace(mask,Entry{true,witness});
        else if(dn==0)memo.emplace(mask,Entry{false,{}});
        return node.value;
    }
    Numbers descend(const Mask& mask,PN thpn,PN thdn) {
        Numbers current=status(mask);
        if(!current.pn || !current.dn)return current;
        auto it=tree.find(mask);
        if(it==tree.end()) {
            if(tree.size()>=50000)throw Limit{"tree-limit"};
            if(nodes>=budget)throw Limit{"node-limit"};
            ++nodes;
            if(nodes%100000==0)std::cerr<<"dfpn nodes="<<nodes<<" exact="<<memo.size()<<" tree="<<tree.size()<<" geometry="<<completions.size()<<" depth="<<mask.count()<<"\n";
            Node node;
            for(int p:legal(mask)){Mask child=mask;child.set(p);node.children.push_back(canonical(child));}
            std::sort(node.children.begin(),node.children.end());
            node.children.erase(std::unique(node.children.begin(),node.children.end()),node.children.end());
            it=tree.emplace(mask,std::move(node)).first;
        }
        Node& node=it->second;
        current=update(mask,node);
        while(current.pn<thpn && current.dn<thdn && current.pn && current.dn) {
            PN best=INF,second=INF;Mask selected;
            for(const auto& child:node.children) {
                auto value=status(child);
                if(value.dn<best){second=best;best=value.dn;selected=child;}
                else second=std::min(second,value.dn);
            }
            Numbers value=status(selected);
            PN child_pn=std::min(INF,thdn-current.dn+value.pn);
            PN child_dn=std::min(thpn,std::min(INF,second+1));
            descend(selected,child_pn,child_dn);
            current=update(mask,node);
        }
        if(!current.pn || !current.dn)tree.erase(mask);
        return current;
    }
public:
    using Solver::Solver;
    bool prove(Mask root) {
        tree.clear();
        root=canonical(root);Numbers value=descend(root,INF,INF);
        if(value.pn && value.dn)throw std::runtime_error("dfpn stopped unresolved below infinite thresholds");
        return value.pn==0;
    }
};

int main(int argc,char**argv) {
    if(argc!=8){std::cerr<<"usage: dfpn --batch side per_root_nodes geometry_bound prefix roots checkpoint\n";return 2;}
    Dfpn s(std::stoi(argv[2]),0,std::stoull(argv[4]));uint64_t per=std::stoull(argv[3]);s.restore(argv[7]);
    std::ifstream input(argv[6]);if(!input)throw std::runtime_error("cannot read roots");
    std::string line;
    while(std::getline(input,line)) {
        if(line.empty())continue;
        std::istringstream row(line);int p;Mask root;std::string name;
        while(row>>p){if(p<0 || p>=s.n || root.has(p))throw std::runtime_error("invalid root");root.set(p);name+="-"+std::to_string(p);}
        if(root.count()<2)throw std::runtime_error("bad root");
        Mask partial;
        for(int q:root.ids()){auto moves=s.legal(partial);if(std::find(moves.begin(),moves.end(),q)==moves.end())throw std::runtime_error("unsafe root");partial.set(q);}
        uint64_t before=s.nodes;s.budget=before+per;const char* outcome="UNKNOWN";
        const char* reason="";
        try{bool win=s.prove(root);s.certificate(root,std::string(argv[5])+name+".cert");outcome=win?"N":"P";}catch(Limit e){reason=e.reason;}
        s.checkpoint(argv[7]);
        std::cout<<"{\"root\":[";bool first=true;for(int q:root.ids()){if(!first)std::cout<<",";first=false;std::cout<<q;}
        std::cout<<"],\"outcome\":\""<<outcome<<"\",\"reason\":\""<<reason<<"\",\"nodes\":"<<s.nodes-before<<",\"cumulative_nodes\":"<<s.nodes
                 <<",\"memo\":"<<s.memo.size()<<",\"quadruples\":"<<s.completions.size()<<"}"<<std::endl;
    }
}

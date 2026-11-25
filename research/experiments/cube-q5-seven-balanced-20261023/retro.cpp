// Incremental exact legal sets, bounded df-pn and compatible bulk checkpoints.
#define main q5_historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include <chrono>
#include <random>

class Incremental: public Solver {
    using PN=__uint128_t;
    static constexpr PN INF=PN(1)<<124;
    struct Numbers {PN pn=1,dn=1;};
    struct Child {Mask key;int point;size_t symmetry;};
    struct Node {Mask live;std::vector<Child> children;Numbers value;};
    std::unordered_map<Mask,Node,Hash> tree;
    Numbers status(const Mask& mask)const {
        auto exact=memo.find(mask);
        if(exact!=memo.end())return exact->second.win?Numbers{0,INF}:Numbers{INF,0};
        auto it=tree.find(mask);if(it!=tree.end())return it->second.value;
        PN cost=1;
        for(int k=mask.count();k<(side==7?17:9);k++) {
            if(cost>=(INF/2)/PN(prior_base)){cost=INF/2;break;}
            cost*=PN(prior_base);
        }
        return {cost,cost};
    }
    Numbers update(const Mask& mask,Node& node) {
        PN pn=INF,dn=0;Mask witness;
        for(const auto& child:node.children) {
            auto value=status(child.key);
            if(value.dn<pn){pn=value.dn;witness=child.key;}
            // INF is reserved for a proved opposite outcome. Saturated work
            // estimates must stay finite, including on shallow root states.
            dn=std::min(INF-1,dn+value.pn);
        }
        if(pn==0){record(mask,Entry{true,witness});node.value={0,INF};}
        else if(dn==0){record(mask,Entry{false,{}});node.value={INF,0};}
        else node.value={pn,dn};
        return node.value;
    }
    Numbers descend(const Mask& mask,const Mask& live,PN thpn,PN thdn) {
        Numbers current=status(mask);
        if(!current.pn || !current.dn)return current;
        auto it=tree.find(mask);
        if(it==tree.end()) {
            if(tree.size()>=tree_limit)throw Limit{"tree-limit"};
            if(nodes>=budget)throw Limit{"node-limit"};
            ++nodes;
            if(nodes%100000==0)std::cerr<<"nodes="<<nodes<<" exact="<<memo.size()<<" tree="<<tree.size()<<" geometry="<<completions.size()<<" depth="<<mask.count()<<"\n";
            Node node;node.live=live;
            for(int p:live.ids()) {
                Mask child=mask;child.set(p);
                auto [key,index]=image(child);
                node.children.push_back(Child{key,p,index});
            }
            std::sort(node.children.begin(),node.children.end(),[](const Child& a,const Child& b){return a.key<b.key;});
            node.children.erase(std::unique(node.children.begin(),node.children.end(),[](const Child& a,const Child& b){return a.key==b.key;}),node.children.end());
            it=tree.emplace(mask,std::move(node)).first;
            max_tree=std::max(max_tree,tree.size());
        }else if(validate && !(it->second.live==live))throw std::runtime_error("inconsistent live set");
        Node& node=it->second;
        current=update(mask,node);
        while(current.pn<thpn && current.dn<thdn && current.pn && current.dn) {
            PN best=INF,second=INF;const Child* selected=nullptr;
            for(const auto& child:node.children) {
                auto value=status(child.key);
                if(value.dn<best){second=best;best=value.dn;selected=&child;}
                else second=std::min(second,value.dn);
            }
            if(!selected)throw std::runtime_error("missing most-proving child");
            auto value=status(selected->key);
            PN child_pn=std::min(INF,thdn-current.dn+value.pn);
            PN child_dn=std::min(thpn,std::min(INF,second+1));
            auto child_node=tree.find(selected->key);
            Mask child_live;
            if(child_node!=tree.end())child_live=child_node->second.live;
            else child_live=transform(advance(mask,node.live,selected->point),selected->symmetry);
            descend(selected->key,child_live,child_pn,child_dn);
            current=update(mask,node);
        }
        if(!current.pn || !current.dn)tree.erase(mask);
        return current;
    }
public:
    using Solver::Solver;
    bool validate=false,direct=false;
    uint64_t prior_base=4,tree_limit=500000;
    int reverse_max=0;
    uint64_t reverse_added=0;
    void lift_parents(const Mask& child) {
        if(!reverse_max || child.count()>reverse_max)return;
        for(int p:child.ids()) {
            Mask parent=child;parent.w[p/64]&=~(uint64_t(1)<<(p%64));parent=canonical(parent);
            auto [it,added]=memo.emplace(parent,Entry{true,child});
            if(!it->second.win)throw std::runtime_error("reverse parent label conflict");
            reverse_added+=added;
        }
    }
    void record(const Mask& mask,Entry entry) {
        auto [it,added]=memo.emplace(mask,entry);
        if(it->second.win!=entry.win)throw std::runtime_error("exact label conflict");
        if(added && !entry.win)lift_parents(mask);
    }
    void reverse_sweep() {
        std::vector<Mask> children;
        for(const auto& [key,entry]:memo)if(!entry.win && key.count()<=reverse_max)children.push_back(key);
        for(const auto& key:children)lift_parents(key);
        std::cerr<<"reverse parents added="<<reverse_added<<"\n";
    }
    uint64_t advances=0,incremental_quads=0,early_empty=0,full_calls=0,dot_candidates=0;
    size_t max_tree=0;
    static bool empty(const Mask& mask){uint64_t value=0;for(auto x:mask.w)value|=x;return value==0;}
    Mask full_live(const Mask& mask){++full_calls;Mask live;for(int p:legal(mask))live.set(p);return live;}
    std::pair<Mask,size_t> image(const Mask& mask)const {
        auto bits=mask.ids();Mask best=mask;size_t index=0;
        for(size_t j=0;j<sym.size();j++) {
            Mask candidate;for(int p:bits)candidate.set(sym[j][p]);
            if(candidate<best){best=candidate;index=j;}
        }
        // sym[0] is identity (axes 0,1,2 and no flips).
        return {best,index};
    }
    Mask transform(const Mask& mask,size_t index)const {
        Mask result;for(int p:mask.ids())result.set(sym[index][p]);return result;
    }
    Mask advance(const Mask& occupied,const Mask& live,int point) {
        if(!live.has(point))throw std::runtime_error("incremental move is illegal");
        ++advances;Mask result=live;result.w[point/64]&=~(uint64_t(1)<<(point%64));
        auto points_now=occupied.ids();int k=points_now.size();
        for(int a=0;a<k && !empty(result);a++)for(int b=a+1;b<k && !empty(result);b++)
        for(int c=b+1;c<k && !empty(result);c++) {
            std::array<int,4> quad{points_now[a],points_now[b],points_now[c],point};
            std::sort(quad.begin(),quad.end());++incremental_quads;
            if(direct) {
                // Only current legal candidates can survive this move. Testing
                // the entire 343-point board for each new quad is unnecessary.
                Row v{},w{},t{},normal{};
                for(int j=0;j<4;j++){v[j]=points[quad[1]][j]-points[quad[0]][j];w[j]=points[quad[2]][j]-points[quad[0]][j];t[j]=points[quad[3]][j]-points[quad[0]][j];}
                for(int j=0;j<4;j++) {
                    int k[3],at=0;for(int l=0;l<4;l++)if(l!=j)k[at++]=l;
                    int i=k[0],h=k[1],l=k[2];
                    normal[j]=(j%2?-1:1)*(v[i]*(w[h]*t[l]-w[l]*t[h])-v[h]*(w[i]*t[l]-w[l]*t[i])+v[l]*(w[i]*t[h]-w[h]*t[i]));
                }
                for(int word=0;word<6;word++)for(uint64_t bits=result.w[word];bits;bits&=bits-1) {
                    int q=word*64+__builtin_ctzll(bits);
                    ++dot_candidates;int64_t value=0;
                    for(int j=0;j<4;j++)value+=normal[j]*(points[q][j]-points[quad[0]][j]);
                    if(!value)result.w[q/64]&=~(uint64_t(1)<<(q%64));
                }
            }else {
                Mask blocked=completion(quad[0],quad[1],quad[2],quad[3]);
                for(int j=0;j<6;j++)result.w[j]&=~blocked.w[j];
            }
        }
        if(empty(result))++early_empty;
        if(validate){Mask child=occupied;child.set(point);if(!(result==full_live(child)))throw std::runtime_error("incremental/full legal mismatch");}
        return result;
    }
    bool prove(Mask root) {
        tree.clear();root=canonical(root);
        auto value=descend(root,full_live(root),INF,INF);
        if(value.pn && value.dn)throw std::runtime_error("infinite-threshold search stopped unresolved");
        return value.pn==0;
    }
    bool mobility_dfs(const Mask& mask,const Mask& live) {
        auto exact=memo.find(mask);if(exact!=memo.end())return exact->second.win;
        if(nodes>=budget)throw Limit{"node-limit"};
        ++nodes;
        if(nodes%100000==0)std::cerr<<"nodes="<<nodes<<" exact="<<memo.size()<<" geometry="<<completions.size()<<" depth="<<mask.count()<<"\n";
        if(empty(live)){record(mask,Entry{false,{}});return false;}
        struct Move {int mobility;Mask key,live;};
        std::vector<Move> moves;
        for(int p:live.ids()) {
            Mask child=mask;child.set(p);auto [key,index]=image(child);
            auto known=memo.find(key);
            if(known!=memo.end()) {
                if(!known->second.win){record(mask,Entry{true,key});return true;}
                continue;
            }
            Mask next=transform(advance(mask,live,p),index);
            if(empty(next)){record(key,Entry{false,{}});record(mask,Entry{true,key});return true;}
            moves.push_back({next.count(),key,next});
        }
        std::sort(moves.begin(),moves.end(),[](const Move& a,const Move& b){return a.mobility!=b.mobility?a.mobility<b.mobility:a.key<b.key;});
        moves.erase(std::unique(moves.begin(),moves.end(),[](const Move& a,const Move& b){return a.key==b.key;}),moves.end());
        for(const auto& move:moves)if(!mobility_dfs(move.key,move.live)){record(mask,Entry{true,move.key});return true;}
        record(mask,Entry{false,{}});return false;
    }
    bool prove_dfs(Mask root){root=canonical(root);return mobility_dfs(root,full_live(root));}
    void inspect(Mask root) {
        root=canonical(root);Mask live=full_live(root);
        std::cout<<"{\"root\":[";bool first=true;
        for(int p:root.ids()){if(!first)std::cout<<",";first=false;std::cout<<p;}
        std::cout<<"],\"live\":"<<live.count()<<",\"children\":[";first=true;
        for(int p:live.ids()) {
            Mask child=root;child.set(p);auto [key,index]=image(child);
            auto entry=memo.find(key);
            if(!first)std::cout<<",";
            first=false;
            std::cout<<"{\"point\":"<<p<<",\"outcome\":\""<<(entry==memo.end()?"UNKNOWN":entry->second.win?"N":"P")<<"\",\"live\":"<<advance(root,live,p).count()<<",\"canonical\":[";
            bool comma=false;for(int q:key.ids()){if(comma)std::cout<<",";comma=true;std::cout<<q;}
            std::cout<<"]}";
        }
        std::cout<<"]}"<<std::endl;
    }
    void fast_restore(const std::string& path) {
        static_assert(__BYTE_ORDER__==__ORDER_LITTLE_ENDIAN__,"bulk checkpoint IO requires little endian");
        std::ifstream in(path,std::ios::binary);if(!in)return;
        char magic[8];std::array<uint64_t,3> header{};
        if(!in.read(magic,8) || std::string(magic,8)!="Q5MEMO2\n" || !in.read(reinterpret_cast<char*>(header.data()),24) || header[0]!=uint64_t(side))throw std::runtime_error("bad checkpoint header");
        nodes=header[1];uint64_t remaining=header[2];memo.reserve(remaining);
        std::vector<uint64_t> buffer(13*8192);
        while(remaining) {
            size_t rows=std::min<uint64_t>(8192,remaining);
            if(!in.read(reinterpret_cast<char*>(buffer.data()),rows*104))throw std::runtime_error("truncated checkpoint");
            for(size_t i=0;i<rows;i++) {
                auto row=buffer.data()+13*i;Mask mask,witness;
                std::copy(row,row+6,mask.w.begin());std::copy(row+7,row+13,witness.w.begin());
                if(row[6]>1 || (!row[6] && !empty(witness)))throw std::runtime_error("invalid checkpoint label");
                for(int p:mask.ids())if(p>=n)throw std::runtime_error("checkpoint mask outside board");
                for(int p:witness.ids())if(p>=n)throw std::runtime_error("checkpoint witness outside board");
                if(!memo.emplace(mask,Entry{bool(row[6]),witness}).second)throw std::runtime_error("duplicate checkpoint row");
            }
            remaining-=rows;
        }
        if(in.get()!=EOF)throw std::runtime_error("checkpoint trailing data");
        std::cerr<<"restored="<<memo.size()<<" nodes="<<nodes<<"\n";
    }
    void fast_checkpoint(const std::string& path)const {
        static_assert(__BYTE_ORDER__==__ORDER_LITTLE_ENDIAN__,"bulk checkpoint IO requires little endian");
        std::ofstream out(path+".new",std::ios::binary);out.write("Q5MEMO2\n",8);
        std::array<uint64_t,3> header{uint64_t(side),nodes,memo.size()};out.write(reinterpret_cast<const char*>(header.data()),24);
        std::vector<uint64_t> buffer;buffer.reserve(13*8192);
        auto flush=[&](){out.write(reinterpret_cast<const char*>(buffer.data()),buffer.size()*8);buffer.clear();};
        for(const auto& [mask,entry]:memo) {
            buffer.insert(buffer.end(),mask.w.begin(),mask.w.end());buffer.push_back(entry.win);
            buffer.insert(buffer.end(),entry.witness.w.begin(),entry.witness.w.end());
            if(buffer.size()==13*8192)flush();
        }
        if(!buffer.empty())flush();
        out.close();
        if(!out || std::rename((path+".new").c_str(),path.c_str()))throw std::runtime_error("checkpoint write failed");
    }
};

int main(int argc,char**argv) {
    if((argc==4 || argc==5) && std::string(argv[1])=="--audit") {
        Incremental s(std::stoi(argv[2]),0,1000000);s.validate=true;s.direct=argc==5 && std::string(argv[4])=="--direct";std::mt19937_64 rng(20261022);
        int histories=std::stoi(argv[3]);uint64_t checks=0;
        for(int h=0;h<histories;h++) {
            Mask occupied,live=s.full_live(occupied);
            while(!Incremental::empty(live)) {
                auto options=live.ids();
                for(size_t j=0;j<std::min<size_t>(4,options.size());j++){int p=options[rng()%options.size()];s.advance(occupied,live,p);++checks;}
                int p=options[rng()%options.size()];live=s.advance(occupied,live,p);occupied.set(p);++checks;
                auto [canonical,index]=s.image(occupied);
                if(!(s.transform(live,index)==s.full_live(canonical)))throw std::runtime_error("canonical live mismatch");
            }
        }
        std::cout<<"{\"histories\":"<<histories<<",\"incremental_full_comparisons\":"<<checks<<",\"early_empty\":"<<s.early_empty<<"}\n";return 0;
    }
    if(argc<8 || std::string(argv[1])!="--batch"){std::cerr<<"usage: engine --batch side nodes geometry_bound prefix roots checkpoint [--validate] [--dfs] [--direct] [--base N] [--tree N] [--inspect]\n";return 2;}
    using Clock=std::chrono::steady_clock;
    auto start=Clock::now();Incremental s(std::stoi(argv[2]),0,std::stoull(argv[4]));
    bool dfs=false,inspect=false;
    for(int i=8;i<argc;i++) {
        std::string flag=argv[i];
        if(flag=="--validate")s.validate=true;
        else if(flag=="--dfs")dfs=true;
        else if(flag=="--direct")s.direct=true;
        else if(flag=="--inspect")inspect=true;
        else if(flag=="--base" && i+1<argc){s.prior_base=std::stoull(argv[++i]);if(s.prior_base<1 || s.prior_base>1000)throw std::runtime_error("bad prior base");}
        else if(flag=="--tree" && i+1<argc){s.tree_limit=std::stoull(argv[++i]);if(!s.tree_limit)throw std::runtime_error("bad tree limit");}
        else if(flag=="--reverse" && i+1<argc){s.reverse_max=std::stoi(argv[++i]);if(s.reverse_max<0 || s.reverse_max>20)throw std::runtime_error("bad reverse depth");}
        else throw std::runtime_error("unknown option");
    }
    s.fast_restore(argv[7]);if(s.reverse_max)s.reverse_sweep();auto restored=Clock::now();
    std::ifstream in(argv[6]);if(!in)throw std::runtime_error("roots missing");std::string line;
    while(std::getline(in,line)) {
        if(line.empty())continue;
        std::istringstream row(line);int p;Mask root;std::string suffix;
        while(row>>p){if(p<0 || p>=s.n || root.has(p))throw std::runtime_error("invalid root");root.set(p);suffix+="-"+std::to_string(p);}
        Mask partial,live=s.full_live(partial);
        for(int q:root.ids()){if(!live.has(q))throw std::runtime_error("unsafe root");live=s.advance(partial,live,q);partial.set(q);}
        if(inspect){s.inspect(root);continue;}
        uint64_t before=s.nodes;s.budget=before+std::stoull(argv[3]);const char* result="UNKNOWN";const char* reason="";
        auto begin=Clock::now();
        try{bool win=dfs?s.prove_dfs(root):s.prove(root);s.certificate(root,std::string(argv[5])+suffix+".cert");result=win?"N":"P";}catch(Limit e){reason=e.reason;}
        auto searched=Clock::now();s.fast_checkpoint(argv[7]);auto saved=Clock::now();
        auto seconds=[](auto a,auto b){return std::chrono::duration<double>(b-a).count();};
        std::cout<<"{\"root\":[";bool first=true;for(int q:root.ids()){if(!first)std::cout<<",";first=false;std::cout<<q;}
        std::cout<<"],\"algorithm\":\""<<(dfs?"mobility-dfs":"weighted-dfpn")<<"\",\"outcome\":\""<<result<<"\",\"reason\":\""<<reason<<"\",\"nodes\":"<<s.nodes-before<<",\"cumulative_nodes\":"<<s.nodes
                 <<",\"memo\":"<<s.memo.size()<<",\"quadruples\":"<<s.completions.size()<<",\"advances\":"<<s.advances<<",\"incremental_quads\":"<<s.incremental_quads
                 <<",\"early_empty\":"<<s.early_empty<<",\"full_legal_calls\":"<<s.full_calls<<",\"max_tree\":"<<s.max_tree
                 <<",\"direct\":"<<(s.direct?"true":"false")<<",\"dot_candidates\":"<<s.dot_candidates
                 <<",\"prior_base\":"<<s.prior_base<<",\"tree_limit\":"<<s.tree_limit
                 <<",\"reverse_max\":"<<s.reverse_max<<",\"reverse_added\":"<<s.reverse_added
                 <<",\"restore_seconds\":"<<seconds(start,restored)<<",\"search_seconds\":"<<seconds(begin,searched)<<",\"save_seconds\":"<<seconds(searched,saved)<<"}"<<std::endl;
    }
}

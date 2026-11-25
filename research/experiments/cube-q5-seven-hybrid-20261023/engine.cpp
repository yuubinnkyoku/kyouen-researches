// Incremental exact legal sets, bounded df-pn and compatible bulk checkpoints.
#define main q5_historical_main
#include "../cube-q5-seven-frontier-20261022/solver.cpp"
#undef main
#include <chrono>
#include <random>
#include "disk.hpp"
#include <csignal>
#include <malloc.h>
volatile std::sig_atomic_t stop_requested=0;

class Incremental: public Solver {
    using PN=__uint128_t;
    static constexpr PN INF=PN(1)<<124;
    struct Numbers {PN pn=1,dn=1;};
    struct Child {Mask key;int point;size_t symmetry;};
    struct Node {Mask live;std::vector<Child> children;Numbers value;};
    std::unordered_map<Mask,Node,Hash> tree;
    Numbers status(const Mask& mask)const {
        auto exact=lookup(mask);
        if(exact)return exact->win?Numbers{0,INF}:Numbers{INF,0};
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
        if(stop_requested)throw Limit{"interrupted"};
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
            auto known=lookup(parent);
            if(known && !known->win)throw std::runtime_error("reverse parent label conflict");
            if(!known){memo.emplace(parent,Entry{true,child});++reverse_added;}
        }
    }
    void record(const Mask& mask,Entry entry) {
        auto known=lookup(mask);
        if(known){if(known->win!=entry.win)throw std::runtime_error("exact label conflict");return;}
        memo.emplace(mask,entry);if(!entry.win)lift_parents(mask);
    }
    void reverse_sweep() {
        std::vector<Mask> children;
        if(base)base->each([&](const Mask& key,Entry entry){if(!entry.win && key.count()<=reverse_max)children.push_back(key);});
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
        root=canonical(root);
        auto value=descend(root,full_live(root),INF,INF);
        if(value.pn && value.dn)throw std::runtime_error("infinite-threshold search stopped unresolved");
        return value.pn==0;
    }
    std::unique_ptr<DiskBase> base;
    std::optional<Entry> lookup(const Mask& key)const {
        auto found=memo.find(key);if(found!=memo.end())return found->second;
        return base?base->get(key):std::optional<Entry>{};
    }
    size_t unknown_size()const{return tree.size();}
    bool finish(const Mask& key,const Mask& live) {
        auto known=lookup(key);if(known)return known->win;
        if(nodes>=budget)throw Limit{"node-limit"};
        ++nodes;
        if(empty(live)){record(key,Entry{false,{}});return false;}
        struct Move {int mobility;Mask key,live;};std::vector<Move> moves;
        for(int p:live.ids()) {
            Mask child=key;child.set(p);auto [canonical,index]=image(child);
            auto value=lookup(canonical);
            if(value){if(!value->win){record(key,Entry{true,canonical});return true;}continue;}
            Mask next=transform(advance(key,live,p),index);
            if(empty(next)){record(canonical,Entry{false,{}});record(key,Entry{true,canonical});return true;}
            moves.push_back({next.count(),canonical,next});
        }
        std::sort(moves.begin(),moves.end(),[](const Move& a,const Move& b){return a.mobility!=b.mobility?a.mobility<b.mobility:a.key<b.key;});
        for(const auto& move:moves)if(!finish(move.key,move.live)){record(key,Entry{true,move.key});return true;}
        record(key,Entry{false,{}});return false;
    }
    void trim(size_t target) {
        std::vector<std::pair<int,Mask>> keys;keys.reserve(tree.size());
        for(const auto& [key,node]:tree){(void)node;if(!lookup(key))keys.emplace_back(key.count(),key);}
        std::sort(keys.begin(),keys.end());
        // Complete deep work before replacing unknown estimates. Merely keeping
        // shallow nodes can repeatedly recreate the same unfinished layer.
        uint64_t old_budget=budget;budget=std::min(budget,nodes+10000);
        for(auto it=keys.rbegin();it!=keys.rend() && nodes<budget;it++) {
            auto found=tree.find(it->second);if(found==tree.end() || lookup(it->second))continue;
            try{finish(it->second,found->second.live);}catch(Limit){break;}
        }
        budget=old_budget;
        std::unordered_set<Mask,Hash> keep;
        for(size_t i=0;i<std::min(target,keys.size());i++)keep.insert(keys[i].second);
        for(auto it=tree.begin();it!=tree.end();)if(!keep.count(it->first))it=tree.erase(it);else ++it;
        for(auto it=keys.rbegin();it!=keys.rend();++it) {
            auto found=tree.find(it->second);if(found==tree.end())continue;
            if(lookup(it->second)){tree.erase(found);continue;}
            update(it->second,found->second);
            if(lookup(it->second))tree.erase(it->second);
        }
        malloc_trim(0);
        std::cerr<<"trimmed unknown tree to "<<tree.size()<<"\n";
    }
    void open_base(const std::string& file,const std::string& index) {
        base=std::make_unique<DiskBase>(file,index);
        if(base->side!=side)throw std::runtime_error("base side mismatch");
        nodes=base->nodes;
    }
    void certificate(Mask root,const std::string& path) {
        root=canonical(root);std::unordered_set<Mask,Hash> seen;
        auto visit=[&](auto&& self,const Mask& mask)->void {
            if(!seen.insert(mask).second)return;
            auto entry=lookup(mask);if(!entry)throw std::runtime_error("missing exact proof row");
            if(entry->win)self(self,entry->witness);
            else for(int p:legal(mask)){Mask child=mask;child.set(p);self(self,canonical(child));}
        };
        visit(visit,root);std::vector<Mask> ordered(seen.begin(),seen.end());std::sort(ordered.begin(),ordered.end());
        std::ofstream out(path);
        out<<"Q5CUBE2 "<<side<<" 6";for(auto word:root.w)out<<" "<<word;out<<"\n";
        for(const auto& mask:ordered) {
            const auto entry=*lookup(mask);for(auto word:mask.w)out<<word<<" ";out<<entry.win;
            for(auto word:entry.witness.w)out<<" "<<word;
            out<<"\n";
        }
        out.close();if(!out)throw std::runtime_error("certificate write failed");
        std::cerr<<"certificate states="<<ordered.size()<<"\n";
    }
    void save(const std::string& path)const {
        uint64_t unknown=0;for(const auto& [key,node]:tree)if(!lookup(key)){(void)node;++unknown;}
        std::ofstream out(path+".new",std::ios::binary);out.write("Q5HYB1\n\0",8);
        std::array<uint64_t,9> header{uint64_t(side),base->fingerprint,base->rows,base->nodes,prior_base,uint64_t(reverse_max),nodes,memo.size(),unknown};
        auto words=[&](const uint64_t* data,size_t count){out.write(reinterpret_cast<const char*>(data),count*8);};
        words(header.data(),header.size());
        for(const auto& [mask,entry]:memo){words(mask.w.data(),6);uint64_t label=entry.win;words(&label,1);words(entry.witness.w.data(),6);}
        for(const auto& [mask,node]:tree)if(!lookup(mask)) {
            words(mask.w.data(),6);words(node.live.w.data(),6);
            std::array<uint64_t,5> row{uint64_t(node.value.pn),uint64_t(node.value.pn>>64),uint64_t(node.value.dn),uint64_t(node.value.dn>>64),node.children.size()};words(row.data(),5);
            for(const auto& child:node.children){words(child.key.w.data(),6);std::array<uint64_t,2> tail{uint64_t(child.point),child.symmetry};words(tail.data(),2);}
        }
        out.write("Q5END1\n\0",8);out.close();
        if(!out || std::rename((path+".new").c_str(),path.c_str()))throw std::runtime_error("hybrid checkpoint write failed");
    }
    void restore(const std::string& path) {
        std::ifstream in(path,std::ios::binary);if(!in)return;
        auto words=[&](uint64_t* data,size_t count){if(!in.read(reinterpret_cast<char*>(data),count*8))throw std::runtime_error("truncated hybrid checkpoint");};
        char magic[8];std::array<uint64_t,9> header{};
        if(!in.read(magic,8) || std::memcmp(magic,"Q5HYB1\n\0",8))throw std::runtime_error("bad hybrid magic");
        words(header.data(),header.size());
        if(header[0]!=uint64_t(side) || header[1]!=base->fingerprint || header[2]!=base->rows || header[3]!=base->nodes || header[4]!=prior_base || header[5]!=uint64_t(reverse_max))throw std::runtime_error("hybrid/base/config mismatch");
        if(header[8]>tree_limit)throw std::runtime_error("restore needs larger tree limit");
        nodes=header[6];memo.reserve(header[7]);tree.reserve(header[8]);
        for(uint64_t i=0;i<header[7];i++) {
            Mask mask,witness;uint64_t label;words(mask.w.data(),6);words(&label,1);words(witness.w.data(),6);
            if(label>1 || (!label && !empty(witness)) || base->get(mask))throw std::runtime_error("bad/duplicate delta row");
            for(int p:mask.ids())if(p>=n)throw std::runtime_error("delta key outside board");
            for(int p:witness.ids())if(p>=n)throw std::runtime_error("delta witness outside board");
            if(!memo.emplace(mask,Entry{bool(label),witness}).second)throw std::runtime_error("duplicate delta row");
        }
        for(uint64_t i=0;i<header[8];i++) {
            Mask key;Node node;std::array<uint64_t,5> row{};words(key.w.data(),6);words(node.live.w.data(),6);words(row.data(),5);
            node.value={PN(row[0])|(PN(row[1])<<64),PN(row[2])|(PN(row[3])<<64)};
            if(!node.value.pn || !node.value.dn || node.value.pn>=INF || node.value.dn>=INF || row[4]>uint64_t(n) || lookup(key))throw std::runtime_error("bad unknown row");
            for(int p:key.ids())if(p>=n || node.live.has(p))throw std::runtime_error("bad unknown mask");
            for(int p:node.live.ids())if(p>=n)throw std::runtime_error("bad unknown live set");
            for(uint64_t j=0;j<row[4];j++) {
                Child child{};std::array<uint64_t,2> tail{};words(child.key.w.data(),6);words(tail.data(),2);
                if(tail[0]>=uint64_t(n) || tail[1]>=sym.size() || !node.live.has(tail[0]))throw std::runtime_error("bad unknown child");
                child.point=tail[0];child.symmetry=tail[1];
                if(validate){Mask played=key;played.set(child.point);auto expected=image(played);if(!(expected.first==child.key) || expected.second!=child.symmetry)throw std::runtime_error("bad canonical child");}
                node.children.push_back(child);
            }
            if(validate && !(node.live==full_live(key)))throw std::runtime_error("restored legal set mismatch");
            if(!tree.emplace(key,std::move(node)).second)throw std::runtime_error("duplicate unknown row");
        }
        if(!in.read(magic,8) || std::memcmp(magic,"Q5END1\n\0",8) || in.get()!=EOF)throw std::runtime_error("bad hybrid trailer");
        std::cerr<<"restored delta="<<memo.size()<<" unknown="<<tree.size()<<" nodes="<<nodes<<"\n";
    }
};

int main(int argc,char**argv) {
    std::signal(SIGTERM,[](int){stop_requested=1;});
    std::signal(SIGINT,[](int){stop_requested=1;});
    if(argc!=12 && argc!=13){std::cerr<<"usage: hybrid side base index checkpoint roots nodes epochs prior tree reverse [--validate]\n";return 2;}
    using Clock=std::chrono::steady_clock;
    Incremental s(std::stoi(argv[1]),0,1000000);s.direct=true;
    uint64_t per=std::stoull(argv[6]),epochs=std::stoull(argv[7]);s.prior_base=std::stoull(argv[8]);s.tree_limit=std::stoull(argv[9]);s.reverse_max=std::stoi(argv[10]);
    // The final positional field is a certificate prefix, separate from checkpoint.
    if(s.prior_base<1 || s.prior_base>1000 || !s.tree_limit || s.reverse_max<0 || s.reverse_max>20)throw std::runtime_error("bad search parameters");
    s.validate=argc==13 && std::string(argv[12])=="--validate";
    s.open_base(argv[2],argv[3]);s.restore(argv[4]);if(s.reverse_max)s.reverse_sweep();
    std::vector<Mask> roots;std::ifstream input(argv[5]);std::string line;
    if(!input)throw std::runtime_error("missing roots");
    while(std::getline(input,line)) {
        if(line.empty())continue;
        Mask root;int p;std::istringstream row(line);
        while(row>>p){if(p<0 || p>=s.n || root.has(p))throw std::runtime_error("bad root point");root.set(p);}
        Mask partial,live=s.full_live(partial);for(int q:root.ids()){if(!live.has(q))throw std::runtime_error("unsafe root");live=s.advance(partial,live,q);partial.set(q);}
        roots.push_back(root);
    }
    for(uint64_t epoch=0;epoch<epochs;epoch++)for(const auto& root:roots) {
        auto started=Clock::now();auto before=s.nodes;s.budget=before+per;
        const char* result="UNKNOWN";const char* reason="";
        auto exact=s.lookup(s.canonical(root));
        if(exact)result=exact->win?"N":"P";
        else try{result=s.prove(root)?"N":"P";}catch(Limit limit){reason=limit.reason;}
        auto searched=Clock::now();
        if(std::string(reason)=="tree-limit")s.trim(s.tree_limit/2);
        s.save(argv[4]);auto saved=Clock::now();
        if(std::string(result)!="UNKNOWN") {
            std::string suffix;for(int p:root.ids())suffix+="-"+std::to_string(p);
            s.certificate(root,std::string(argv[11])+suffix+".cert");
        }
        std::cout<<"{\"epoch\":"<<epoch<<",\"root\":[";bool first=true;for(int p:root.ids()){if(!first)std::cout<<",";first=false;std::cout<<p;}
        std::cout<<"],\"outcome\":\""<<result<<"\",\"reason\":\""<<reason<<"\",\"nodes\":"<<s.nodes-before<<",\"cumulative_nodes\":"<<s.nodes<<",\"base_rows\":"<<s.base->rows<<",\"delta_rows\":"<<s.memo.size()<<",\"unknown_rows\":"<<s.unknown_size()<<",\"search_seconds\":"<<std::chrono::duration<double>(searched-started).count()<<",\"save_seconds\":"<<std::chrono::duration<double>(saved-searched).count()<<"}"<<std::endl;
        if(std::string(result)!="UNKNOWN" && roots.size()==1)return 0;
        if(stop_requested)return 0;
    }
}

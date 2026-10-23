// A sufficient P strategy search: stabilizer-involution replies, terminal
// replies and previously known P witnesses.
// Failure is UNKNOWN, never an N label. Successful labels have ordinary proofs.
#define Q5_HYBRID_LIBRARY
#include "lazy.cpp"
#undef Q5_HYBRID_LIBRARY
#include <set>
class Policy {
public:
    Incremental& s;
    std::unordered_set<Mask,Hash> failed;
    uint64_t visited=0,budget=0,no_reply=0,cache_hits=0;
    explicit Policy(Incremental& engine,uint64_t limit):s(engine),budget(limit){}
    bool prove(const Mask& key,const Mask& live) {
        auto exact=s.lookup(key);if(exact){++cache_hits;return !exact->win;}
        if(failed.count(key))return false;
        if(visited>=budget)throw Limit{"policy-node-limit"};
        ++visited;
        if(Incremental::empty(live)){s.record(key,Entry{false,{}});return true;}
        std::vector<size_t> symmetries;
        for(size_t g=1;g<s.sym.size();g++) {
            bool involution=true;for(int p=0;p<s.n;p++)if(s.sym[g][s.sym[g][p]]!=p){involution=false;break;}
            if(involution && s.transform(key,g)==key)symmetries.push_back(g);
        }
        struct Move {Mask child;int point;std::vector<int> replies;};
        std::map<Mask,Move> unique;
        for(int p:live.ids()) {
            Mask child=key;child.set(p);auto canonical=s.canonical(child);
            if(unique.count(canonical))continue;
            std::vector<int> replies;
            for(size_t g:symmetries){int q=s.sym[g][p];if(q!=p && live.has(q))replies.push_back(q);}
            std::sort(replies.begin(),replies.end());replies.erase(std::unique(replies.begin(),replies.end()),replies.end());
            unique.emplace(canonical,Move{canonical,p,replies});
        }
        std::vector<Move> moves;for(auto& row:unique)moves.push_back(row.second);
        std::sort(moves.begin(),moves.end(),[](const Move& a,const Move& b){return a.replies.size()!=b.replies.size()?a.replies.size()<b.replies.size():a.child<b.child;});
        for(const auto& move:moves) {
            auto known=s.lookup(move.child);
            if(known){if(known->win)continue;failed.insert(key);return false;}
            Mask child=key;child.set(move.point);Mask next=s.advance(key,live,move.point);
            // Terminal replies and already known P grandchildren are ordinary
            // exact witnesses and do not need to preserve a symmetry.
            bool immediate=false;
            for(int q:next.ids()) {
                Mask grandchild=child;grandchild.set(q);Mask canonical=s.canonical(grandchild);
                auto known_grand=s.lookup(canonical);
                if((known_grand && !known_grand->win) || Incremental::empty(s.advance(child,next,q))) {
                    s.record(canonical,Entry{false,{}});s.record(move.child,Entry{true,canonical});immediate=true;break;
                }
            }
            if(immediate)continue;
            struct Reply {Mask key,live;};std::vector<Reply> replies;std::set<Mask> seen;
            for(int q:move.replies)if(next.has(q)) {
                Mask grandchild=child;grandchild.set(q);auto [canonical,index]=s.image(grandchild);
                if(!seen.insert(canonical).second)continue;
                Mask after=s.transform(s.advance(child,next,q),index);
                replies.push_back({canonical,after});
            }
            std::sort(replies.begin(),replies.end(),[](const Reply& a,const Reply& b){return a.live.count()!=b.live.count()?a.live.count()<b.live.count():a.key<b.key;});
            bool success=false;
            for(const auto& reply:replies)if(prove(reply.key,reply.live)) {
                s.record(move.child,Entry{true,reply.key});success=true;break;
            }
            if(!success){if(replies.empty())++no_reply;failed.insert(key);return false;}
        }
        s.record(key,Entry{false,{}});return true;
    }
};
int main(int argc,char**argv) {
    if(argc!=8){std::cerr<<"usage: policy side bases indices roots nodes certificate-prefix exact-output\n";return 2;}
    Incremental s(std::stoi(argv[1]),0,1000000);s.direct=true;s.open_base(argv[2],argv[3]);
    Policy policy(s,std::stoull(argv[5]));std::ifstream input(argv[4]);std::string line;
    while(std::getline(input,line)) {
        if(line.empty())continue;
        Mask root;std::istringstream row(line);int p;while(row>>p){if(p<0 || p>=s.n || root.has(p))throw std::runtime_error("bad root");root.set(p);}
        Mask partial,live=s.full_live(partial);
        for(int q:root.ids()){if(!live.has(q))throw std::runtime_error("unsafe root");live=s.advance(partial,live,q);partial.set(q);}
        root=s.canonical(root);live=s.full_live(root);
        bool success=false;const char* reason="restricted-policy-failed";
        try{success=policy.prove(root,live);}catch(Limit limit){reason=limit.reason;}
        std::cout<<"{\"root\":[";bool comma=false;std::string suffix;
        for(int q:root.ids()){if(comma)std::cout<<",";comma=true;std::cout<<q;suffix+="-"+std::to_string(q);}
        std::cout<<"],\"outcome\":\""<<(success?"P":"UNKNOWN")<<"\",\"reason\":\""<<(success?"":reason)<<"\",\"visited\":"<<policy.visited<<",\"no_reply\":"<<policy.no_reply<<",\"cached_exact\":"<<policy.cache_hits<<",\"additional_exact_candidates\":"<<s.memo.size()<<"}"<<std::endl;
        if(success)s.certificate(root,std::string(argv[6])+suffix+".cert");
    }
    s.save(argv[7]);
}

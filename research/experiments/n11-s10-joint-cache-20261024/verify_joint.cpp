#define main old_schedule734_main
#include "../n11-four-s8-shared-tt-20261023/adaptive52.cpp"
using Weights=array<long long,4>;
const vector<Weights> menu={
 {100000,1000,0,-1},{100000,1000,0,1},{100000,1000,0,-10},{100000,1000,0,10},
 {100000,1000,1,-1},{100000,1000,-1,-1},{100000,100,0,-1},{100000,10000,0,-1},
 {24,8,-31,9},{100000,0,0,0},{100000,1000,0,-100},{100000,1000,0,100},
 {100000,1000,10,-1},{100000,1000,-10,-1},{100000,1000,0,0},{100000,1000,0,-3},
 {100000,1000,0,3},{100000,1000,0,-30},{100000,1000,0,30},{100000,1000,0,-300}
};
#undef main
#include <sstream>
struct Item {U key;array<long long,4> w;bool expected;};
int main(int argc,char**argv){try{
 need(argc==6,"usage: verify_joint S10_734_KEYS SCHEDULE734 SCHEDULE52 SELECTED52_KEYS MODE");init_d4();
 vector<Item> a,b;{ifstream f(argv[1]);string h;while(f>>h)a.push_back({parse(h),{},true});}
 need(a.size()==734,"734 keys");need(is_sorted(a.begin(),a.end(),[](const Item&x,const Item&y){return x.key<y.key;}),"S10 keys not sorted");
 {ifstream f(argv[2]);string s,v;while(f>>v)s+=v;need(s.size()==1468,"734 schedule");reverse(a.begin(),a.end());for(int i=0;i<734;i++){int j=stoi(s.substr(2*i,2),nullptr,16);need(j>=0&&j<(int)menu.size(),"bad menu");a[i].w=menu[j];}}
 {ifstream f(argv[3]);string h;array<long long,4> w;while(f>>h>>w[0]>>w[1]>>w[2]>>w[3])b.push_back({parse(h),w,false});}
 need(b.size()==52,"52 keys");{ifstream f(argv[4]);need(f.good(),"52 key file missing");vector<U> selected;string h;while(f>>h)selected.push_back(parse(h));need(selected.size()==52,"selected52 size");reverse(selected.begin(),selected.end());for(int i=0;i<52;i++)need(selected[i]==b[i].key,"52 schedule mismatch");}
 set<U> distinct;for(auto&i:a)need(points(i.key).size()==10&&safe(i.key)&&canon(i.key)==i.key&&distinct.insert(i.key).second,"invalid S10 WIN leaf");for(auto&i:b)need(points(i.key).size()==10&&safe(i.key)&&canon(i.key)==i.key&&distinct.insert(i.key).second,"invalid or conflicting S10 LOSS leaf");
 Solver sol;sol.mode=1;sol.memo.reserve(100000);size_t checked=0;
 auto work=[&](const vector<Item>&xs){uint64_t oldhits=sol.hits,oldlooks=sol.lookups;size_t old=sol.memo.size();for(auto&i:xs){for(int j=0;j<4;j++)W[j]=i.w[j];Root r=prepare(i.key,10);need(sol.dfs(r,0,i.key)==i.expected,"conflict");checked++;}cout<<"block leaves="<<xs.size()<<" added="<<sol.memo.size()-old<<" hits="<<sol.hits-oldhits<<" lookups="<<sol.lookups-oldlooks<<"\n";};
 int mode=stoi(argv[5]);need(mode==0||mode==1,"bad mode");if(mode==0){work(b);work(a);}else{work(a);work(b);}
 need(checked==786,"both verdict blocks must be checked");
 cout<<"PASS total="<<sol.memo.size()<<" lookups="<<sol.lookups<<" hits="<<sol.hits<<" edges="<<sol.children<<"\n";
 if(mode==0)need(sol.memo.size()==55289&&sol.lookups==92730&&sol.hits==37441&&sol.children==91944,"metrics mismatch");
 else need(sol.memo.size()==55289&&sol.lookups==92728&&sol.hits==37439&&sol.children==91942,"metrics mismatch");
}catch(exception&e){cerr<<"ERROR "<<e.what()<<"\n";return 1;}}

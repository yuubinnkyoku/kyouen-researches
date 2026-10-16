#define main baseline_s10_main
#include "../n11-targeted-terminal-lift-20261015/scripts/solve_s10_candidates.cpp"
#undef main
struct LocalTT {
 static constexpr size_t CAP=1u<<15,MASK=CAP-1;
 array<uint64_t,CAP> keys{};
 array<uint8_t,CAP> vals{};
 array<uint32_t,CAP> stamp{};
 uint32_t gen=0;size_t used=0;
 void begin(){used=0;if(++gen==0){stamp.fill(0);gen=1;}}
 size_t index(uint64_t x)const{x^=x>>33;x*=0xff51afd7ed558ccdULL;x^=x>>33;return x&MASK;}
 bool get(uint64_t x,bool&v)const{size_t h=index(x);while(stamp[h]==gen){if(keys[h]==x){v=vals[h];return true;}h=(h+1)&MASK;}return false;}
 void set(uint64_t x,bool v){size_t h=index(x);while(stamp[h]==gen&&keys[h]!=x)h=(h+1)&MASK;if(stamp[h]!=gen && ++used>CAP*3/4)throw runtime_error("local TT capacity exceeded");stamp[h]=gen;keys[h]=x;vals[h]=v;}
};
static constexpr int TRIPLES=287980;
static array<U128,TRIPLES> forbidden_triples{};
static int c2[121],c3[121];
static long long forbidden_quad_count=0;
inline int tidx(int a,int b,int c){
 if(a>b)swap(a,b);if(b>c)swap(b,c);if(a>b)swap(a,b);
 return c3[c]+c2[b]+a;
}
void init_forbidden(){
 for(int i=0;i<121;i++){c2[i]=i*(i-1)/2;c3[i]=i*(i-1)*(i-2)/6;}
 for(int a=0;a<121;a++)for(int b=a+1;b<121;b++)for(int c=b+1;c<121;c++){
  int abc=tidx(a,b,c);
  for(int d=c+1;d<121;d++)if(!det4(a,b,c,d)){
   forbidden_quad_count++;
   forbidden_triples[abc]|=(U128)1<<d;
   forbidden_triples[tidx(a,b,d)]|=(U128)1<<c;
   forbidden_triples[tidx(a,c,d)]|=(U128)1<<b;
   forbidden_triples[tidx(b,c,d)]|=(U128)1<<a;
  }
 }
 if(forbidden_quad_count!=95670)throw runtime_error("forbidden geometry count mismatch");
}
bool fast_safe(U128 root,const vector<int>&base){
 for(int a=0;a<(int)base.size();a++)for(int b=a+1;b<(int)base.size();b++)for(int c=b+1;c<(int)base.size();c++)
  if(forbidden_triples[tidx(base[a],base[b],base[c])]&root)return false;
 return true;
}
vector<int> fast_legal(U128 root,const vector<int>&base){
 U128 blocked=root;
 for(int a=0;a<(int)base.size();a++)for(int b=a+1;b<(int)base.size();b++)for(int c=b+1;c<(int)base.size();c++)
  blocked|=forbidden_triples[tidx(base[a],base[b],base[c])];
 vector<int> ans;
 for(int i=0;i<121;i++)if(!((blocked>>i)&1))ans.push_back(i);
 return ans;
}
LocalTT tt;
int order_mode=7;bool audit=false;
Terminal solve_incremental(U128 root){
 if(countbits(root)!=10||canonical(root)!=root)throw runtime_error("invalid S10");
 auto base=points(root);
 if(!fast_safe(root,base))throw runtime_error("unsafe S10");
 auto moves=fast_legal(root,base);int n=moves.size();
 if(n>63)throw runtime_error("unsupported >63 terminal moves");
 vector<uint64_t> bad;
 for(int i=0;i<n;i++){
  U128 blocked=0;
  for(int a=0;a<10;a++)for(int b=a+1;b<10;b++)blocked|=forbidden_triples[tidx(base[a],base[b],moves[i])];
  for(int j=i+1;j<n;j++)if((blocked>>moves[j])&1)bad.push_back((1ULL<<i)|(1ULL<<j));
 }
 auto contains=[&](uint64_t s){for(uint64_t b:bad)if((s&b)==b)return true;return false;};
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
  U128 blocked=0;
  for(int a:base)blocked|=forbidden_triples[tidx(a,moves[i],moves[j])];
  for(int k=j+1;k<n;k++)if((blocked>>moves[k])&1){
   uint64_t s=(1ULL<<i)|(1ULL<<j)|(1ULL<<k);
   if(!contains(s))bad.push_back(s);
  }
 }
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
  U128 blocked=forbidden_triples[tidx(moves[i],moves[j],moves[k])];
  for(int l=k+1;l<n;l++)if((blocked>>moves[l])&1){
   uint64_t s=(1ULL<<i)|(1ULL<<j)|(1ULL<<k)|(1ULL<<l);
   if(!contains(s))bad.push_back(s);
  }
 }
 vector<uint64_t> pair_adj(n,0);
 vector<vector<uint64_t>> extra(n);
 vector<int> pairs(n,0),triples(n,0),quads(n,0);
 for(uint64_t b:bad){
  int count=__builtin_popcountll(b);
  for(uint64_t bits=b;bits;bits&=bits-1){
   int i=__builtin_ctzll(bits);
   if(count==2){pair_adj[i]|=b^(1ULL<<i);pairs[i]++;}
   else{extra[i].push_back(b^(1ULL<<i));if(count==3)triples[i]++;else quads[i]++;}
  }
 }
 vector<int> order(n);iota(order.begin(),order.end(),0);
 auto score=[&](int i){
  if(order_mode==0)return 0LL;
  if(order_mode==1)return 100000LL*pairs[i];
  if(order_mode==7)return 100000LL*pairs[i]+100LL*triples[i];
  if(order_mode==9)return 100000LL*pairs[i]+10000LL*triples[i]+quads[i];
  return 100000LL*pairs[i]+1000LL*triples[i]+quads[i];
 };
 stable_sort(order.begin(),order.end(),[&](int a,int b){return score(a)>score(b);});
 // Move bit positions are permuted into priority order; bit scans preserve the original heuristic.
 vector<int> old_to_new(n);
 for(int i=0;i<n;i++)old_to_new[order[i]]=i;
 vector<uint64_t> permuted_bad;
 permuted_bad.reserve(bad.size());
 for(uint64_t b:bad){uint64_t z=0;for(uint64_t t=b;t;t&=t-1)z|=1ULL<<old_to_new[__builtin_ctzll(t)];permuted_bad.push_back(z);}
 bad.swap(permuted_bad);
 fill(pair_adj.begin(),pair_adj.end(),0);
 for(auto& e:extra)e.clear();
 for(uint64_t b:bad){int cnt=__builtin_popcountll(b);for(uint64_t t=b;t;t&=t-1){int i=__builtin_ctzll(t);if(cnt==2)pair_adj[i]|=b^(1ULL<<i);else extra[i].push_back(b^(1ULL<<i));}}

 tt.begin();uint64_t fresh=0;
 function<bool(uint64_t,uint64_t)> wins=[&](uint64_t s,uint64_t legal_mask){
  bool cached=false;if(tt.get(s,cached))return cached;
  fresh++;
  bool ans=false;
  if(audit){
   uint64_t check=0;
   for(int i=0;i<n;i++)if(!(s&(1ULL<<i))){
    bool ok=true;
    for(uint64_t b:bad)if((b&(1ULL<<i)) && (s&(b^(1ULL<<i)))==(b^(1ULL<<i))){ok=false;break;}
    if(ok)check|=1ULL<<i;
   }
   if(check!=legal_mask)throw runtime_error("incremental legal-mask disagreement");
  }
  for(uint64_t options=legal_mask;options;options&=options-1){
   int i=__builtin_ctzll(options);
   uint64_t bit=1ULL<<i;
   uint64_t child_mask=legal_mask&~(bit|pair_adj[i]);
   for(uint64_t b:extra[i]){
    uint64_t rem=b&~s;
    if(rem && !(rem&(rem-1)))child_mask &= ~rem;
   }
   if(!wins(s|bit,child_mask)){ans=true;break;}
  }
  tt.set(s,ans);return ans;
 };
 bool loss=!wins(0,(1ULL<<n)-1);
 return {loss,fresh,n};
}
void generate_all_candidates(){
 const array<string,4> roots={
  "00000000040004011004000004020001",
  "00000000040004011004200004200000",
  "00000000050004001024000004010000",
  "00000021000000101101000010000400"
 };
 set<U128> candidates;
 for(const string& hex:roots){
  U128 root=parse128(hex);
  if(countbits(root)!=8||!fast_safe(root,points(root)))throw runtime_error("invalid eight-stone certificate root");
  for(int p:fast_legal(root,points(root))){
   U128 s9=root|((U128)1<<p);
   for(int q:fast_legal(s9,points(s9)))candidates.insert(canonical(s9|((U128)1<<q)));
  }
 }
 if(candidates.size()!=2325)throw runtime_error("unexpected candidate count");
 for(U128 s:candidates)cout<<hex128(s)<<'\n';
}
void audit_geometry(){
 // All 8,495,410 four-point subsets, not a sample.
 long long count=0;
 for(int a=0;a<121;a++)for(int b=a+1;b<121;b++)for(int c=b+1;c<121;c++)for(int d=c+1;d<121;d++){
  bool expected=!det4(a,b,c,d);
  if(bool((forbidden_triples[tidx(a,b,c)]>>d)&1)!=expected ||
     bool((forbidden_triples[tidx(a,b,d)]>>c)&1)!=expected ||
     bool((forbidden_triples[tidx(a,c,d)]>>b)&1)!=expected ||
     bool((forbidden_triples[tidx(b,c,d)]>>a)&1)!=expected)
   throw runtime_error("geometry table disagreement");
  count++;
 }
 if(count!=8495410)throw runtime_error("quadruple count mismatch");
 cerr<<"PASS geometry audit "<<count<<" quadruples\n";
}
int main(int argc,char**argv){try{
 if(argc==2 && (string(argv[1])=="--generate"||string(argv[1])=="--audit-geometry")){
  init_forbidden();
  if(string(argv[1])=="--generate")generate_all_candidates();else audit_geometry();
  return 0;
 }

 if(argc!=5)throw runtime_error("usage: terminal_triple_index input output ordering count | --generate | --audit-geometry");
 order_mode=stoi(argv[3]);int expected=stoi(argv[4]);
 if(order_mode!=0&&order_mode!=1&&order_mode!=7&&order_mode!=9)throw runtime_error("unsupported ordering");
 audit=getenv("N11_INCREMENTAL_AUDIT")!=nullptr;
 if(expected<=0)throw runtime_error("invalid expected count");
 auto gstart=chrono::steady_clock::now();init_forbidden();
 cerr<<"geometry_init_seconds="<<chrono::duration<double>(chrono::steady_clock::now()-gstart).count()<<" forbidden="<<forbidden_quad_count<<"\n";
 ifstream in(argv[1]);ofstream out(argv[2]);if(!in||!out)throw runtime_error("IO error");
 string s;int count=0;uint64_t states=0;auto start=chrono::steady_clock::now();
 while(in>>s){auto mask=parse128(s);
  if(getenv("N11_GEOMETRY_ROOT_AUDIT")){auto b=points(mask);if(safe(mask)!=fast_safe(mask,b)||legal(mask)!=fast_legal(mask,b))throw runtime_error("root geometry disagreement");}
  auto t=solve_incremental(mask);
  out<<s<<'\t'<<(t.loss?"LOSS":"WIN")<<'\t'<<t.states<<'\t'<<t.moves<<'\n';
  states+=t.states;count++;
 }
 if(count!=expected)throw runtime_error("input count mismatch");
 cout<<"incremental order="<<order_mode<<" count="<<count<<" states="<<states
 <<" seconds="<<fixed<<setprecision(6)<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<'\n';
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<'\n';return 1;}
}

// Prime-field, independently enumerated rooted six-section support census.
// The 0/1 minors have |det| <= 5^(5/2) < 56, and the Cramer
// numerator/difference bounds are < 1009; mod 1009 is exact here.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <unordered_map>
#include <vector>
using namespace std;
constexpr int P=1009;
int invp[P];
int mod(int x){x%=P;return x<0?x+P:x;}
struct State {
 uint32_t span=0;
 array<uint32_t,32> allowed{};
 bool distinct=false;
 uint8_t rank=0;
};
unordered_map<uint32_t,State> cache;
State makeState(uint32_t bmask){
 State s;vector<int> b;for(int j=0;j<32;j++)if(bmask&(1u<<j))b.push_back(j);
 int r=(int)b.size();s.rank=r;
 if(r==0){s.span=1;s.allowed[0]=1;return s;}
 if(r>5){fprintf(stderr,"rank>5\n");exit(1);}
 int rows[5][5]{};
 for(int i=0;i<5;i++)for(int j=0;j<r;j++)rows[i][j]=(b[j]>>i)&1;
 int rr[5]{},inv[5][5]{};bool found=false;
 for(int subset=0;subset<32 && !found;subset++){
  if(__builtin_popcount((unsigned)subset)!=r)continue;
  int t=0;for(int i=0;i<5;i++)if(subset>>i&1)rr[t++]=i;
  int a[5][10]{};for(int i=0;i<r;i++){
   for(int j=0;j<r;j++)a[i][j]=rows[rr[i]][j];
   a[i][r+i]=1;
  }
  bool ok=true;
  for(int col=0;col<r;col++){
   int p=col;while(p<r && a[p][col]==0)p++;
   if(p==r){ok=false;break;}
   if(p!=col)for(int j=0;j<2*r;j++)swap(a[p][j],a[col][j]);
   int z=invp[a[col][col]];
   for(int j=0;j<2*r;j++)a[col][j]=mod(a[col][j]*z);
   for(int i=0;i<r;i++)if(i!=col){int f=a[i][col];if(f)for(int j=0;j<2*r;j++)a[i][j]=mod(a[i][j]-f*a[col][j]);}
  }
  if(ok){found=true;for(int i=0;i<r;i++)for(int j=0;j<r;j++)inv[i][j]=a[i][r+j];}
 }
 if(!found){fprintf(stderr,"dependent basis %x\n",bmask);exit(2);}
 int seen=1;s.distinct=true;
 for(int i=0;i<5;i++){
  int sig=0;for(int j=0;j<r;j++)sig|=((b[j]>>i)&1)<<j;
  if(seen>>sig&1){s.distinct=false;break;}
  seen|=1<<sig;
 }
 for(int p=0;p<32;p++){
  int c[5]{};
  for(int i=0;i<r;i++)for(int j=0;j<r;j++)c[i]=mod(c[i]+inv[i][j]*((p>>rr[j])&1));
  bool in=true;
  for(int i=0;i<5;i++){
   int z=0;for(int j=0;j<r;j++)z=mod(z+rows[i][j]*c[j]);
   if(z!=((p>>i)&1)){in=false;break;}
  }
  if(!in)continue;
  s.span|=1u<<p;
  uint32_t mask=0;
  for(int t=0;t<(1<<r);t++){
   int z=0;for(int j=0;j<r;j++)if(t>>j&1)z=mod(z+c[j]);
   if(z==0||z==1)mask|=1u<<t;
  }
  s.allowed[p]=mask;
 }
 return s;
}
const State& getState(uint32_t bmask){
 auto it=cache.find(bmask);if(it!=cache.end())return it->second;
 return cache.emplace(bmask,makeState(bmask)).first->second;
}
bool valid(uint32_t subset){
 uint32_t basis=0;
 const State* state=&getState(0);
 uint32_t left=subset;
 while(left){int p=__builtin_ctz(left);left&=left-1;
  if(!(state->span&(1u<<p))){basis|=1u<<p;state=&getState(basis);}
 }
 if(!state->distinct||state->rank<3)return false;
 uint32_t mask=state->rank==5?0xffffffffu:((1u<<(1<<state->rank))-1u);
 left=subset;
 while(left){int p=__builtin_ctz(left);left&=left-1;mask &=state->allowed[p];}
 return __builtin_popcount(mask)==6;
}
int main(int argc,char**argv){
 int maxk=argc>1?atoi(argv[1]):8;
 invp[1]=1;for(int i=2;i<P;i++)invp[i]=P-(P/i)*invp[P%i]%P;
 cache.reserve(300000);
 for(int k=0;k<=maxk;k++){
  uint64_t cnt=0,visited=0;
  if(k==0){visited=1;cnt=valid(0);}else{
   uint64_t x=(1ull<<k)-1;
   while(x<(1ull<<32)){
    visited++;if(valid((uint32_t)x))cnt++;
    uint64_t c=x&-x,r=x+c;
    x=(((r^x)>>2)/c)|r;
   }
  }
  printf("k=%d total=%llu valid=%llu cache=%zu\n",k,(unsigned long long)visited,(unsigned long long)cnt,cache.size());fflush(stdout);
 }
}
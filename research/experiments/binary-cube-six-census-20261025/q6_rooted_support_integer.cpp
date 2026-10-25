// Independent exact-integer Cramer checker of all rooted 6-section supports.
// No modular arithmetic; column coefficients are cofactors/determinants.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <unordered_map>
#include <vector>
using namespace std;
int det(const int a[5][5],int n){
 if(n==0)return 1;
 if(n==1)return a[0][0];
 int ans=0;
 for(int col=0;col<n;col++){
  if(!a[0][col])continue;
  int b[5][5]{};
  for(int i=1;i<n;i++){int j2=0;for(int j=0;j<n;j++)if(j!=col)b[i-1][j2++]=a[i][j];}
  ans+=(col&1?-1:1)*a[0][col]*det(b,n-1);
 }
 return ans;
}
struct Data{uint32_t span=0;array<uint32_t,32> good{};bool distinct=false;int rank=0;};
unordered_map<uint32_t,Data> memo;
Data calc(uint32_t bmask){
 Data s;vector<int> cols;for(int p=0;p<32;p++)if(bmask>>p&1)cols.push_back(p);
 int r=cols.size();s.rank=r;
 if(r==0){s.span=1;s.good[0]=1;return s;}
 if(r>5){fprintf(stderr,"bad basis\n");exit(1);}
 int rows[5][5]{};for(int i=0;i<5;i++)for(int j=0;j<r;j++)rows[i][j]=(cols[j]>>i)&1;
 int selected[5]{},A[5][5]{},denom=0;
 for(int subset=0;subset<32 && !denom;subset++){
  if(__builtin_popcount((unsigned)subset)!=r)continue;
  int n=0;for(int i=0;i<5;i++)if(subset>>i&1)selected[n++]=i;
  for(int i=0;i<r;i++)for(int j=0;j<r;j++)A[i][j]=rows[selected[i]][j];
  denom=det(A,r);
 }
 if(!denom){fprintf(stderr,"dependent basis\n");exit(2);}
 int adj[5][5]{};
 for(int i=0;i<r;i++)for(int j=0;j<r;j++){
  int m[5][5]{};
  for(int x=0,xx=0;x<r;x++)if(x!=j){
   for(int y=0,yy=0;y<r;y++)if(y!=i)m[xx][yy++]=A[x][y];
   xx++;
  }
  adj[i][j]=((i+j)&1?-1:1)*det(m,r-1);
 }
 for(int i=0;i<r;i++)for(int j=0;j<r;j++){
  int x=0;for(int t=0;t<r;t++)x+=A[i][t]*adj[t][j];
  if(x!=(i==j?denom:0)){fprintf(stderr,"adjugate mismatch\n");exit(3);}
 }
 uint32_t sigs=1;s.distinct=true;
 for(int i=0;i<5;i++){
  int z=0;for(int j=0;j<r;j++)z|=rows[i][j]<<j;
  if(sigs>>z&1){s.distinct=false;break;}
  sigs|=1u<<z;
 }
 for(int p=0;p<32;p++){
  int nums[5]{};
  for(int j=0;j<r;j++)for(int i=0;i<r;i++)nums[j]+=adj[j][i]*((p>>selected[i])&1);
  bool in=true;
  for(int i=0;i<5;i++){
   int lhs=0;for(int j=0;j<r;j++)lhs+=rows[i][j]*nums[j];
   if(lhs!=denom*((p>>i)&1)){in=false;break;}
  }
  if(!in)continue;
  s.span|=1u<<p;
  uint32_t good=0;
  for(int t=0;t<(1<<r);t++){
   int z=0;for(int j=0;j<r;j++)if(t>>j&1)z+=nums[j];
   if(z==0||z==denom)good|=1u<<t;
  }
  s.good[p]=good;
 }
 return s;
}
const Data& state(uint32_t key){auto it=memo.find(key);if(it!=memo.end())return it->second;return memo.emplace(key,calc(key)).first->second;}
bool valid(uint32_t S){
 uint32_t b=0;const Data* d=&state(0);
 // Descending order, unlike the modular implementation.
 for(int p=31;p>=0;p--)if(S>>p&1){if(!(d->span>>p&1)){b|=1u<<p;d=&state(b);}}
 if(!d->distinct||d->rank<3)return false;
 uint32_t mask=d->rank==5?0xffffffffu:((1u<<(1<<d->rank))-1);
 for(int p=31;p>=0;p--)if(S>>p&1)mask &=d->good[p];
 return __builtin_popcount(mask)==6;
}
uint64_t count=0,visited=0;
void enumerate(int p,int remaining,uint32_t mask){
 if(!remaining){visited++;if(valid(mask))count++;return;}
 if(p+remaining>32)return;
 for(int i=p;i<=32-remaining;i++)enumerate(i+1,remaining-1,mask|(1u<<i));
}
int main(int argc,char**argv){int maxk=argc>1?atoi(argv[1]):8;memo.reserve(300000);
 for(int k=0;k<=maxk;k++){
  count=visited=0;enumerate(0,k,0);
  printf("k=%d visited=%llu good=%llu cache=%zu\n",k,(unsigned long long)visited,(unsigned long long)count,memo.size());fflush(stdout);
 }
}
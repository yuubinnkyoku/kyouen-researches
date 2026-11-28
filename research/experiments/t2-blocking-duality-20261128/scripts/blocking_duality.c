/* blocking_duality.c — full-scan enumerator for the K1365 complement duality check.
 *
 * For a board (finite point/line incidence structure, uniform line size l) and
 * parameter s, let t = l - s. A subset S is "s-safe" if every line contains
 * fewer than s points of S; it is maximal-safe if no point can be added.
 * A subset C is a "t-fold blocking set" if every line contains at least t
 * points of C; it is minimal if no point can be removed.
 *
 * K1365 (already proved): S is maximal s-safe  <=>  C = P \ S is a minimal
 * t-fold blocking set. This enumerator walks ALL 2^n subsets once with a
 * Gray code and checks BOTH sides with independent per-mask logic, then
 * verifies the complement bijection at element level, both directions.
 *
 * Usage: blocking_duality [-l prefix] board.txt s
 *   board.txt: first line "n L", then L lines "k p0 p1 ... pk-1".
 *   If -l prefix is given, dumps maximal-safe masks to prefix.maximal.txt
 *   and minimal-blocking masks to prefix.minimal.txt (hex masks, one per line).
 * Output (stdout):
 *   board <file> n <n> lines <L> l <l> s <s> t <t>
 *   maximal_safe <size>:<count> ...
 *   minimal_blocking <size>:<count> ...
 *   complement_check_fail <n>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXL 64
#define MAXN 31

static int popcount32(uint32_t x){ return __builtin_popcount(x); }

static int cmp_u32(const void*a,const void*b){
  uint32_t x=*(const uint32_t*)a, y=*(const uint32_t*)b;
  return x<y?-1:(x>y?1:0);
}

int main(int argc,char**argv){
  const char*listprefix=NULL;
  int ai=1;
  if(argc>3 && !strcmp(argv[1],"-l")){ listprefix=argv[2]; ai=3; }
  if(argc<ai+2){ fprintf(stderr,"usage: %s [-l prefix] board.txt s\n",argv[0]); return 2; }
  const char*bf=argv[ai]; int s=atoi(argv[ai+1]);
  FILE*f=fopen(bf,"r");
  if(!f){ fprintf(stderr,"cannot open %s\n",bf); return 2; }
  int n,L;
  if(fscanf(f,"%d %d",&n,&L)!=2 || n<1 || n>MAXN || L<1 || L>MAXL){ fprintf(stderr,"bad board header\n"); fclose(f); return 2; }
  uint32_t linemask[MAXL]; int lsz[MAXL];
  for(int i=0;i<L;i++){
    int k; if(fscanf(f,"%d",&k)!=1 || k<1){ fprintf(stderr,"bad line\n"); fclose(f); return 2; }
    uint32_t m=0;
    for(int j=0;j<k;j++){ int p; if(fscanf(f,"%d",&p)!=1 || p<0 || p>=n){ fprintf(stderr,"bad point\n"); fclose(f); return 2; } m|=1u<<p; }
    if(popcount32(m)!=k){ fprintf(stderr,"duplicate point in line\n"); fclose(f); return 2; }
    linemask[i]=m; lsz[i]=k;
  }
  fclose(f);
  int l=lsz[0];
  for(int i=1;i<L;i++) if(lsz[i]!=l){ fprintf(stderr,"non-uniform line size\n"); return 2; }
  if(s<1 || s>l){ fprintf(stderr,"need 1<=s<=l\n"); return 2; }
  int t=l-s;
  uint32_t full=(n==32)?0xFFFFFFFFu:((1u<<n)-1u);

  /* point -> incident lines (deg <= l+1 for designs; guard anyway) */
  static int ptlines[MAXN][MAXL];
  int deg[MAXN];
  for(int p=0;p<n;p++){
    deg[p]=0;
    for(int i=0;i<L;i++) if(linemask[i]>>p&1){ if(deg[p]>=MAXL){fprintf(stderr,"deg overflow\n");return 2;} ptlines[p][deg[p]++]=i; }
  }

  /* list storage */
  uint32_t *maxlist=NULL,*minlist=NULL;
  size_t maxcap=1024,mincap=1024,maxn_=0,minn_=0;
  if(listprefix){ maxlist=malloc(maxcap*sizeof(uint32_t)); minlist=malloc(mincap*sizeof(uint32_t)); if(!maxlist||!minlist){fprintf(stderr,"oom\n");return 2;} }

  uint64_t maxcnt[MAXN+1]; uint64_t mincnt[MAXN+1];
  memset(maxcnt,0,sizeof maxcnt); memset(mincnt,0,sizeof mincnt);

  int cnt[MAXL];
  memset(cnt,0,sizeof cnt);
  int badS=0;                 /* lines with cnt >= s */
  int badC=0;                 /* lines with cnt <  t */
  for(int i=0;i<L;i++) if(cnt[i]<t) badC++;   /* = L at the empty set (t>=1) */

  uint32_t S=0;
  uint64_t total=1ULL<<n;
  for(uint64_t i=1;i<total;i++){
    int p=__builtin_ctzll(i);
    int bit=(S>>p)&1;
    S^=(1u<<p);
    int *pls=ptlines[p]; int d=deg[p];
    for(int j=0;j<d;j++){
      int li=pls[j]; int c=cnt[li];
      if(bit){ /* point removed from S */
        c--;
        if(c==s) badS--;
        if(c==t-1) badC++;
      }else{    /* point added to S */
        c++;
        if(c==s+1) badS++;
        if(c==t) badC--;
      }
      cnt[li]=c;
    }
    if(badS==0){ /* S is s-safe: check maximality directly */
      int maximal=1;
      for(int q=0;q<n&&maximal;q++){
        if((S>>q)&1) continue;
        int ok=0; int *qls=ptlines[q]; int qd=deg[q];
        for(int j=0;j<qd;j++) if(cnt[qls[j]]==s){ ok=1; break; }
        if(!ok) maximal=0;
      }
      if(maximal){
        int pc=popcount32(S);
        maxcnt[pc]++;
        if(listprefix){ if(maxn_==maxcap){ maxcap*=2; maxlist=realloc(maxlist,maxcap*sizeof(uint32_t)); } maxlist[maxn_++]=S; }
      }
    }
    if(badC==0){ /* S is a t-fold blocking set: check minimality directly */
      int minimal=1;
      for(int q=0;q<n&&minimal;q++){
        if(!((S>>q)&1)) continue;
        int ok=0; int *qls=ptlines[q]; int qd=deg[q];
        for(int j=0;j<qd;j++) if(cnt[qls[j]]==t){ ok=1; break; }
        if(!ok) minimal=0;
      }
      if(minimal){
        int pc=popcount32(S);
        mincnt[pc]++;
        if(listprefix){ if(minn_==mincap){ mincap*=2; minlist=realloc(minlist,mincap*sizeof(uint32_t)); } minlist[minn_++]=S; }
      }
    }
  }

  /* element-level complement bijection, both directions (on private copies) */
  uint64_t fail=0;
  if(listprefix){
    char path[4096];
    FILE*fm; FILE*fn;
    snprintf(path,sizeof path,"%s.maximal.txt",listprefix);
    fm=fopen(path,"w"); if(!fm){fprintf(stderr,"cannot write %s\n",path);return 2;}
    snprintf(path,sizeof path,"%s.minimal.txt",listprefix);
    fn=fopen(path,"w"); if(!fn){fprintf(stderr,"cannot write %s\n",path);return 2;}
    for(size_t i=0;i<maxn_;i++) fprintf(fm,"%x\n",maxlist[i]);
    for(size_t i=0;i<minn_;i++) fprintf(fn,"%x\n",minlist[i]);
    fclose(fm); fclose(fn);
    for(size_t i=0;i<maxn_;i++) maxlist[i]^=full;  /* complements of maximal-safe */
    qsort(minlist,minn_,sizeof(uint32_t),cmp_u32);
    qsort(maxlist,maxn_,sizeof(uint32_t),cmp_u32);
    for(size_t i=0;i<maxn_;i++)
      if(!bsearch(&maxlist[i],minlist,minn_,sizeof(uint32_t),cmp_u32)) fail++;
    for(size_t i=0;i<minn_;i++)
      if(!bsearch(&minlist[i],maxlist,maxn_,sizeof(uint32_t),cmp_u32)) fail++;
  }
  if(maxn_!=minn_) fail++;

  printf("board %s n %d lines %d l %d s %d t %d\n",bf,n,L,l,s,t);
  printf("maximal_safe");
  for(int i=0;i<=n;i++) if(maxcnt[i]) printf(" %d:%llu",i,(unsigned long long)maxcnt[i]);
  printf("\n");
  printf("minimal_blocking");
  for(int i=0;i<=n;i++) if(mincnt[i]) printf(" %d:%llu",i,(unsigned long long)mincnt[i]);
  printf("\n");
  printf("complement_check_fail %llu\n",(unsigned long long)fail);
  printf("counts_total maximal %llu minimal %llu\n",(unsigned long long)maxn_,(unsigned long long)minn_);
  return 0;
}

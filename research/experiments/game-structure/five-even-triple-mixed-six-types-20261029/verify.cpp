// Complete finite-base check for five-center split Node Kayles.
// Target triple {0,1,2} is initially absent. At most six other
// non-private support types have multiplicity one or two.
// Each center has exactly one private leaf.
// c++ -std=c++17 -O3 -Wall -Wextra -pedantic verify.cpp -o /tmp/verify && /tmp/verify
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
constexpr int K=5, FULL=(1<<K)-1, TARGET=7, MAX_EXTRA=6;
vector<int> types;
uint64_t cases=0, cases_by_size[MAX_EXTRA+1]={}, mismatches=0, hist[16]={};
int a[32]={};

// R is the surviving center mask. Isolated leaves are split off as xor parity.
// Every independent-vertex move strictly reduces R, so a 2^K DP is exact.
int grundy(){
    int dp[32]={}, parity[32]={}, degree_parity[5]={};
    int supports[32], size=0;
    for(int s=1;s<=FULL;++s)if(a[s]){
        supports[size++]=s;
        if(a[s]&1)
            for(int c=0;c<K;++c)if(s&(1<<c))degree_parity[c]^=1;
    }
    for(int R=1;R<=FULL;++R){
        int p=0;
        for(int j=0;j<size;++j){
            int s=supports[j];
            if((s&R)&&(a[s]&1))p^=1;
        }
        parity[R]=p;
    }
    for(int R=1;R<=FULL;++R){
        unsigned int opts=0;
        for(int c=0;c<K;++c)if(R&(1<<c)){
            int child=parity[R]^degree_parity[c];
            opts|=1u<<child;
        }
        for(int j=0;j<size;++j){
            int s=supports[j];
            if(!(s&R))continue;
            int RR=R&~s;
            int child=dp[RR]^(parity[R]^parity[RR]^1);
            if(child>=31){fprintf(stderr,"grundy overflow\n");exit(3);}
            opts|=1u<<child;
        }
        dp[R]=__builtin_ctz(~opts);
    }
    return dp[FULL];
}

void evaluate(int n){
    int g0=grundy();
    a[TARGET]=2;
    int g2=grundy();
    a[TARGET]=0;
    ++cases;
    ++cases_by_size[n];
    if(g0>=16){fprintf(stderr,"hist overflow\n");exit(6);}
    ++hist[g0];
    if(g0!=g2){
        ++mismatches;
        fprintf(stderr,"counterexample n=%d g0=%d g2=%d supports:",n,g0,g2);
        for(int s:types)if(a[s])fprintf(stderr," %d:%d",s,a[s]);
        fprintf(stderr,"\n");
        exit(2);
    }
}
void enumerate(int next,int n){
    evaluate(n);
    if(n==MAX_EXTRA)return;
    for(int j=next;j<(int)types.size();++j){
        int s=types[j];
        for(int multiplicity=1;multiplicity<=2;++multiplicity){
            a[s]=multiplicity;
            enumerate(j+1,n+1);
        }
        a[s]=0;
    }
}
int main(){
    for(int i=0;i<K;++i)a[1<<i]=1;
    for(int s=1;s<=FULL;++s)
        if(__builtin_popcount((unsigned)s)>=2&&s!=TARGET)types.push_back(s);
    if(types.size()!=25)return 1;
    enumerate(0,0);
    uint64_t expected=0, choose=1, power=1;
    for(int i=0;i<=MAX_EXTRA;++i){
        if(i){choose=choose*(25-(i-1))/i;power*=2;}
        uint64_t want=choose*power;
        if(cases_by_size[i]!=want){
            fprintf(stderr,"bad count at %d: %llu vs %llu\n",i,
                (unsigned long long)cases_by_size[i],(unsigned long long)want);
            return 4;
        }
        expected+=want;
        printf("extra_types=%d cases=%llu\n",i,(unsigned long long)want);
    }
    printf("TOTAL=%llu mismatches=%llu\n",
        (unsigned long long)cases,(unsigned long long)mismatches);
    for(int i=0;i<16;++i)
        if(hist[i])printf("grundy_%d=%llu\n",i,(unsigned long long)hist[i]);
    return (cases==expected&&mismatches==0)?0:5;
}

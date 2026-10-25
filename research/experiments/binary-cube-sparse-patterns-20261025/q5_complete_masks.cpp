// Exact interpolation certificate for five binary-cube rows.
// All relevant 0/1 minors have |det| <= 6^3=216 < 1009.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
constexpr int P=1009;
int mod(int a){a%=P;return a<0?a+P:a;}
int inv(int a){int r=1,e=P-2;while(e){if(e&1)r=(int)((long long)r*a%P);a=(int)((long long)a*a%P);e>>=1;}return r;}
bool invert(const int in[5][5],int out[5][5]){
    int a[5][10]={};
    for(int i=0;i<5;++i){for(int j=0;j<5;++j)a[i][j]=in[i][j];a[i][i+5]=1;}
    for(int j=0;j<5;++j){
        int r=j;while(r<5&&!a[r][j])++r;if(r==5)return false;
        for(int c=0;c<10;++c)swap(a[r][c],a[j][c]);
        int f=inv(a[j][j]);
        for(int c=j;c<10;++c)a[j][c]=(int)((long long)a[j][c]*f%P);
        for(int i=0;i<5;++i)if(i!=j){
            int x=a[i][j];
            for(int c=j;c<10;++c)a[i][c]=mod(a[i][c]-x*a[j][c]);
        }
    }
    for(int i=0;i<5;++i)for(int j=0;j<5;++j)out[i][j]=a[i][j+5];
    return true;
}
int main(){
    vector<uint32_t> masks;int bases=0;
    for(int a=0;a<32;++a)for(int b=a+1;b<32;++b)
    for(int c=b+1;c<32;++c)for(int d=c+1;d<32;++d){
        int pat[4]={a,b,c,d},m[5][5]={},im[5][5]={};
        for(int j=0;j<5;++j)m[0][j]=1;
        for(int i=1;i<5;++i)for(int j=0;j<5;++j)m[i][j]=(pat[i-1]>>j)&1;
        if(!invert(m,im))continue;
        ++bases;int nonunit=0;
        for(int z=0;z<16;++z){
            int rhs[5]={1,z&1,(z>>1)&1,(z>>2)&1,(z>>3)&1},w[5]={};
            for(int i=0;i<5;++i)for(int j=0;j<5;++j)w[i]=mod(w[i]+im[i][j]*rhs[j]);
            bool unit=false;
            for(int i=0;i<5;++i){
                bool same=true;
                for(int j=0;j<5;++j)if(w[j]!=(i==j))same=false;
                if(same)unit=true;
            }
            if(unit)continue;
            ++nonunit;
            uint32_t mask=0;
            for(int v=0;v<32;++v){
                int t=0;for(int j=0;j<5;++j)if((v>>j)&1)t+=w[j];
                t%=P;if(t==0||t==1)mask|=uint32_t(1)<<v;
            }
            masks.push_back(mask);
        }
        assert(nonunit==11);
    }
    assert(bases==15040);
    sort(masks.begin(),masks.end());
    masks.erase(unique(masks.begin(),masks.end()),masks.end());
    assert(masks.size()==510);
    array<int,33> hist{};
    for(uint32_t m:masks)++hist[__builtin_popcount(m)];
    assert(hist[10]==280&&hist[14]==105&&hist[16]==85&&hist[20]==10&&hist[24]==30);
    for(uint32_t m:masks)cout<<m<<'\n';
}

// Exact exhaustive audit of four-vertex hyperplane sections in {0,1}^d.
// No floating point or previously classified affine-flat types are used.
// For each four-set, test the affine closure with integer Cramer's rule.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
using namespace std;

int d2(int a,int b,int c,int d){return a*d-b*c;}
int d3(array<int,3> a,array<int,3> b,array<int,3> c){
    return a[0]*d2(b[1],b[2],c[1],c[2])
         - a[1]*d2(b[0],b[2],c[0],c[2])
         + a[2]*d2(b[0],b[1],c[0],c[1]);
}
struct Span {
    int d,u,r=2,i=-1,j=-1,k=-1,det=0;
    array<int,8>a{},b{},c{};
    Span(int dim,int p,int q,int s,int t):d(dim),u(p){
        for(int x=0;x<d;++x){
            a[x]=((q>>x)&1)-((p>>x)&1);
            b[x]=((s>>x)&1)-((p>>x)&1);
            c[x]=((t>>x)&1)-((p>>x)&1);
        }
        for(int x=0;x<d && i<0;++x)for(int y=x+1;y<d;++y){
            int v=d2(a[x],a[y],b[x],b[y]);
            if(v){i=x;j=y;det=v;break;}
        }
        assert(i>=0); // three distinct cube vertices are not collinear
        for(int x=0;x<d && r==2;++x)
            for(int y=x+1;y<d && r==2;++y)
                for(int z=y+1;z<d;++z){
                    int v=d3({a[x],a[y],a[z]},
                             {b[x],b[y],b[z]},
                             {c[x],c[y],c[z]});
                    if(v){r=3;i=x;j=y;k=z;det=v;break;}
                }
    }
    bool contains(int v)const{
        array<int,8>w{};
        for(int x=0;x<d;++x)w[x]=((v>>x)&1)-((u>>x)&1);
        if(r==2){
            int aa=d2(w[i],w[j],b[i],b[j]);
            int bb=d2(a[i],a[j],w[i],w[j]);
            for(int x=0;x<d;++x)
                if(det*w[x]!=aa*a[x]+bb*b[x])return false;
            return true;
        }
        array<int,3>A{a[i],a[j],a[k]},B{b[i],b[j],b[k]};
        array<int,3>C{c[i],c[j],c[k]},W{w[i],w[j],w[k]};
        int aa=d3(W,B,C),bb=d3(A,W,C),cc=d3(A,B,W);
        for(int x=0;x<d;++x)
            if(det*w[x]!=aa*a[x]+bb*b[x]+cc*c[x])return false;
        return true;
    }
};
uint64_t choose(int n,int k){
    uint64_t v=1;
    for(int i=1;i<=k;++i)v=v*(n-i+1)/i;
    return v;
}
int64_t power(int64_t a,int n){int64_t r=1;while(n--)r*=a;return r;}
int64_t expected(int d){
    return (power(16,d)-12*power(12,d)+30*power(10,d)
           -35*power(8,d)+27*power(6,d)-16*power(4,d)
           +5*power(2,d))/24;
}
int main(){
    for(int d=3;d<=6;++d){
        int n=1<<d;
        uint64_t plane4=0,flat4=0,rejected=0,full=0;
        for(int u=0;u<n;++u)for(int v=u+1;v<n;++v)
            for(int w=v+1;w<n;++w)for(int z=w+1;z<n;++z){
                Span s(d,u,v,w,z);
                if(s.r==d){++full;continue;}
                int count=0;
                for(int x=0;x<n;++x)
                    if(s.contains(x) && ++count>4)break;
                if(count==4){
                    if(s.r==2)++plane4;else ++flat4;
                }else ++rejected;
            }
        uint64_t got=plane4+flat4;
        cout<<"d="<<d<<" total="<<choose(n,4)
            <<" rank2="<<plane4<<" rank3="<<flat4
            <<" rejected="<<rejected<<" full="<<full
            <<" E4="<<got<<" expected="<<expected(d)<<"\n";
        if(got!=static_cast<uint64_t>(expected(d)))return 1;
    }
}

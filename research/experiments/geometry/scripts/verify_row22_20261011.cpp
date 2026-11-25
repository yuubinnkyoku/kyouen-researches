#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
struct P {int x,y;};
long long det3(long long a,long long b,long long c,long long d,long long e,long long f,long long g,long long h,long long i){return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g);}
long long circle_det(const P &a,const P &b,const P &c,const P &d){
    auto sq=[](P p)->long long{return (long long)p.x*p.x+(long long)p.y*p.y;};
    return det3(b.x-a.x,b.y-a.y,sq(b)-sq(a),c.x-a.x,c.y-a.y,sq(c)-sq(a),d.x-a.x,d.y-a.y,sq(d)-sq(a));
}
long long cross(const P &a,const P &b,const P &c){return (long long)(b.x-a.x)*(c.y-a.y)-(long long)(b.y-a.y)*(c.x-a.x);}
long long formula(int m){long long v=m;return (2*v*v*v-3*v*v+4*v-3*(m%2))/12;}
long long pair_count(int m){long long ans=0;vector<int> count(2*m,0);for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)count[a+b]++;for(int n:count)ans+=(long long)n*n;return ans;}
int main(){
    for(int m=1;m<=300;m++)assert(formula(m)==pair_count(m));
    long long cases=0;
    for(int w=1;w<=11;w++)for(int h=1;h<=11;h++){
        if(w*h>121)continue;
        vector<P> ps;for(int y=0;y<h;y++)for(int x=0;x<w;x++)ps.push_back({x,y});
        long long c22=0,c211=0,c1111=0,cline=0;
        int n=ps.size();
        for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++){
            if(circle_det(ps[a],ps[b],ps[c],ps[d])!=0)continue;
            if(cross(ps[a],ps[b],ps[c])==0 && cross(ps[a],ps[b],ps[d])==0){cline++;continue;}
            int cnt[11]={};for(int j:{a,b,c,d})cnt[ps[j].y]++;
            int rowtypes=0,maxrow=0;for(int j=0;j<h;j++)if(cnt[j]){rowtypes++;maxrow=max(maxrow,cnt[j]);}
            if(rowtypes==2 && maxrow==2)c22++;
            else if(rowtypes==3 && maxrow==2)c211++;
            else if(rowtypes==4)c1111++;
            else {cerr<<"unexpected row pattern";return 2;}
        }
        long long predicted=(long long)h*(h-1)/2*formula(w);
        if(c22!=predicted){cerr<<"FAIL "<<w<<"x"<<h<<" observed "<<c22<<" predicted "<<predicted<<"\n";return 1;}
        cases++;
        if(w==h && (w==5||w==6||w==11))cout<<"square "<<w<<" circle22="<<c22<<" circle211="<<c211<<" circle1111="<<c1111<<" totalcircle="<<(c22+c211+c1111)<<" line="<<cline<<"\n";
    }
    cout<<"verified rectangular boards="<<cases<<", pair_sum_m=1..300\n";
}

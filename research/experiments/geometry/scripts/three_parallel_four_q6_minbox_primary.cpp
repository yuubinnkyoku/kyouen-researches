// Exhaustive classification of three 4-point rows in small integer rectangles.
// A 6-point circle must take exactly two points from each of the three rows.
#include <array>
#include <iostream>
#include <vector>
using namespace std;
struct Row {array<int,4> x;};
struct Pair {int sum,product;};
vector<Row> rows(int W){vector<Row> v;for(int a=0;a<W;a++)for(int b=a+1;b<W;b++)for(int c=b+1;c<W;c++)for(int d=c+1;d<W;d++)v.push_back({{a,b,c,d}});return v;}
int count_circles(const Row&A,const Row&B,const Row&C,int y0,int y1,int y2){
    int count=0;
    for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){
      int s=A.x[a]+A.x[b],p0=A.x[a]*A.x[b]-y0*y0;
      for(int c=0;c<4;c++)for(int d=c+1;d<4;d++){
        if(B.x[c]+B.x[d]!=s)continue;
        int p1=B.x[c]*B.x[d]-y1*y1;
        for(int e=0;e<4;e++)for(int f=e+1;f<4;f++){
          if(C.x[e]+C.x[f]!=s)continue;
          int p2=C.x[e]*C.x[f]-y2*y2;
          if((p1-p0)*(y2-y0)==(p2-p0)*(y1-y0))++count;
        }
      }
    }
    return count;
}
void run(int W,int H){
    auto v=rows(W);long long hist[4]={},total=0;
    for(int y0=0;y0<H;y0++)for(int y1=y0+1;y1<H;y1++)for(int y2=y1+1;y2<H;y2++)
    for(auto&A:v)for(auto&B:v)for(auto&C:v){
        int c=count_circles(A,B,C,y0,y1,y2);
        if(c<0||c>3){cerr<<"UNEXPECTED "<<c<<"\n";exit(2);}
        ++hist[c];++total;
        if(c==3){
            cout<<"WITNESS "<<W<<' '<<H<<" y="<<y0<<','<<y1<<','<<y2<<" x=";
            for(auto&R:{A,B,C}){cout<<'[';for(int x:R.x)cout<<x<<',';cout<<']';}cout<<'\n';
        }
    }
    cout<<"RESULT "<<W<<' '<<H<<" total="<<total<<" c0="<<hist[0]<<" c1="<<hist[1]<<" c2="<<hist[2]<<" c3="<<hist[3]<<'\n';
}
int main(){for(auto [W,H]:{pair<int,int>{9,3},{6,4},{5,5},{4,7},{7,4}})run(W,H);}

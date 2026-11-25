// C++17: exhaustive finite-field Gale-minor certificate checker.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std;
using i64=int64_t;
i64 power(i64 a,i64 e,i64 p){
    i64 r=1;
    while(e){if(e&1)r=r*a%p;a=a*a%p;e>>=1;}
    return r;
}
i64 determinant(vector<vector<i64>> a,int k,i64 p){
    i64 out=1;
    for(int j=0;j<k;++j){
        int t=j;
        while(t<k && !a[t][j])++t;
        if(t==k)return 0;
        if(t!=j){swap(a[t],a[j]);out=(p-out)%p;}
        i64 z=a[j][j];out=out*z%p;
        i64 inv=power(z,p-2,p);
        for(int i=j+1;i<k;++i){
            i64 f=a[i][j]*inv%p;
            for(int h=j+1;h<k;++h)
                a[i][h]=(a[i][h]-f*a[j][h]%p+p)%p;
            a[i][j]=0;
        }
    }
    return out;
}
void verify(int d,const vector<i64>& points,i64 p){
    int n=(int)points.size(),k=n-d-1;
    if(d<1 || d>30 || k<1 || k>8 || n!=d+7)
        throw runtime_error("unexpected dimensions");
    set<i64> seen(points.begin(),points.end());
    if((int)seen.size()!=n)throw runtime_error("duplicate vertices");
    for(i64 x:points)if(x<0 || x>=(1LL<<d))
        throw runtime_error("vertex outside cube");
    vector<vector<i64>> a(d+1,vector<i64>(n));
    for(int j=0;j<n;++j){
        a[0][j]=1;
        for(int i=0;i<d;++i)a[i+1][j]=(points[j]>>i)&1;
    }
    vector<int> pivot;
    int r=0;
    for(int j=0;j<n && r<d+1;++j){
        int t=r;
        while(t<d+1 && !a[t][j])++t;
        if(t==d+1)continue;
        swap(a[t],a[r]);
        i64 inv=power(a[r][j],p-2,p);
        for(int h=j;h<n;++h)a[r][h]=a[r][h]*inv%p;
        for(int i=0;i<d+1;++i)if(i!=r){
            i64 f=a[i][j];
            for(int h=j;h<n;++h)a[i][h]=(a[i][h]-f*a[r][h]%p+p)%p;
        }
        pivot.push_back(j);++r;
    }
    if(r!=d+1)throw runtime_error("augmented matrix lacks full rank");
    vector<int> free;
    for(int j=0;j<n;++j)
        if(find(pivot.begin(),pivot.end(),j)==pivot.end())free.push_back(j);
    if((int)free.size()!=k)throw runtime_error("kernel dimension mismatch");
    vector<vector<i64>> gale(n,vector<i64>(k));
    for(int z=0;z<k;++z){
        gale[free[z]][z]=1;
        for(int i=0;i<r;++i)gale[pivot[i]][z]=(p-a[i][free[z]])%p;
    }
    vector<int> choose(k);
    for(int i=0;i<k;++i)choose[i]=i;
    int64_t tested=0;
    while(true){
        vector<vector<i64>> minor(k);
        for(int i=0;i<k;++i)minor[i]=gale[choose[i]];
        if(!determinant(minor,k,p))throw runtime_error("singular Gale minor");
        ++tested;
        int i=k-1;
        while(i>=0 && choose[i]==n-k+i)--i;
        if(i<0)break;
        ++choose[i];
        for(int j=i+1;j<k;++j)choose[j]=choose[j-1]+1;
    }
    cout<<"d="<<d<<" n="<<n<<" prime="<<p<<" Gale minors="<<tested<<" PASS\n";
}
int main(int argc,char** argv){
    if(argc!=2){cerr<<"usage: verify_gale_mod witnesses.txt\n";return 2;}
    ifstream f(argv[1]);
    if(!f){cerr<<"cannot open witness file\n";return 2;}
    string line;int count=0;
    try{
        while(getline(f,line)){
            if(line.empty() || line[0]=='#')continue;
            istringstream ss(line);
            int d;
            if(!(ss>>d))throw runtime_error("bad witness line");
            vector<i64> p; i64 x;
            while(ss>>x)p.push_back(x);
            if(ss.fail() && !ss.eof())throw runtime_error("bad vertex");
            for(i64 prime:{1000000007LL,1000000009LL})verify(d,p,prime);
            ++count;
        }
        if(count!=6)throw runtime_error("expected six dimensions");
    }catch(const exception& e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}

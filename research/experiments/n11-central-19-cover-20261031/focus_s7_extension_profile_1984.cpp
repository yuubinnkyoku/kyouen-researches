// Exhaustive, cache-free 11x11 extension profile for the selected six-stone witness.
// All safe supersets are enumerated once (in increasing added-point order).
// 3x3 difference determinants and independent 4x4 Bareiss determinants must agree.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
using U = unsigned __int128;
constexpr int N = 121;
constexpr U BOARD = ((U)1 << N) - 1;
int xs[N], ys[N];
vector<U> blocked;
int index3(int a, int b, int c) { return (a*N+b)*N+c; }
vector<int> points(U mask) {
    vector<int> out;
    while (mask) {
        int p = ((uint64_t)mask != 0)
            ? __builtin_ctzll((uint64_t)mask)
            : 64 + __builtin_ctzll((uint64_t)(mask >> 64));
        out.push_back(p);
        mask &= mask - 1;
    }
    return out;
}
long long det3(int a, int b, int c, int d) {
    long long x = xs[a], y = ys[a];
    long long u0=xs[b]*xs[b]+ys[b]*ys[b]-x*x-y*y, u1=xs[b]-x, u2=ys[b]-y;
    long long v0=xs[c]*xs[c]+ys[c]*ys[c]-x*x-y*y, v1=xs[c]-x, v2=ys[c]-y;
    long long w0=xs[d]*xs[d]+ys[d]*ys[d]-x*x-y*y, w1=xs[d]-x, w2=ys[d]-y;
    return u0*(v1*w2-v2*w1)-u1*(v0*w2-v2*w0)+u2*(v0*w1-v1*w0);
}
long long det4(int a, int b, int c, int d) {
    int p[4]={a,b,c,d};
    long long A[4][4];
    for (int i=0;i<4;i++) {
        int x=xs[p[i]], y=ys[p[i]];
        A[i][0]=x*x+y*y; A[i][1]=x; A[i][2]=y; A[i][3]=1;
    }
    long long prev=1, sign=1;
    for (int k=0;k<3;k++) {
        if (!A[k][k]) {
            int j=k+1;
            while (j<4 && !A[j][k]) ++j;
            if (j==4) return 0;
            for (int t=0;t<4;t++) swap(A[k][t],A[j][t]);
            sign=-sign;
        }
        long long pivot=A[k][k];
        for (int i=k+1;i<4;i++) {
            for (int j=k+1;j<4;j++) {
                long long num=A[i][j]*pivot-A[i][k]*A[k][j];
                if (num%prev) throw runtime_error("non-integral Bareiss step");
                A[i][j]=num/prev;
            }
            A[i][k]=0;
        }
        prev=pivot;
    }
    return sign*A[3][3];
}
void initialize() {
    for (int p=0;p<N;p++) { xs[p]=p%11; ys[p]=p/11; }
    blocked.resize(N*N*N);
    for (int a=0;a<N;a++) for (int b=a+1;b<N;b++)
        for (int c=b+1;c<N;c++) {
            U bad=0;
            for (int d=0;d<N;d++) {
                bool v3=(det3(a,b,c,d)==0);
                bool v4=(det4(a,b,c,d)==0);
                if (v3!=v4) throw runtime_error("3x3/4x4 determinant conflict");
                if (v4) bad |= (U)1 << d;
            }
            blocked[index3(a,b,c)]=bad;
        }
}
U legal(U mask) {
    auto ps=points(mask);
    U forbidden=mask;
    for (int i=0;i<(int)ps.size();i++)
        for (int j=i+1;j<(int)ps.size();j++)
            for (int k=j+1;k<(int)ps.size();k++)
                forbidden |= blocked[index3(ps[i],ps[j],ps[k])];
    return BOARD & ~forbidden;
}
U parse(const char *s) {
    U mask=0;
    for (int i=0;s[i];i++) {
        char c=s[i];
        int n=c>='0'&&c<='9'?c-'0':c-'a'+10;
        if (n<0 || n>15) throw runtime_error("bad hex");
        mask=(mask<<4)|(U)n;
    }
    return mask;
}
int main() {
    try {
        initialize();
        U root=parse("00000000000000603800000000008000");
        if (points(root).size()!=6 || root!= (root&BOARD))
            throw runtime_error("invalid frozen S6 root");
        array<long long,5> count{};
        array<int,5> minimum{9999,9999,9999,9999,9999}, maximum{};
        auto visit = [&](auto&& self, U mask, int last, int depth) -> void {
            U moves=legal(mask);
            int n=(int)points(moves).size();
            count[depth]++;
            minimum[depth]=min(minimum[depth],n);
            maximum[depth]=max(maximum[depth],n);
            if (depth==4) return;
            for (int p:points(moves))
                if (p>last) self(self,mask|((U)1<<p),p,depth+1);
        };
        visit(visit,root,-1,0);
        const array<long long,5> expected_count={1,57,1283,14854,96024};
        const array<int,5> expected_min={57,32,17,10,4};
        const array<int,5> expected_max={57,51,46,41,35};
        if (count!=expected_count || minimum!=expected_min || maximum!=expected_max)
            throw runtime_error("extension profile disagrees with frozen counts");
        cout << "{\"schema\":\"n11-central49-focus57-extension-depth10-v1\","
             << "\"focused_s6\":\"00000000000000603800000000008000\","
             << "\"unique_safe_supersets_s6_to_s10\":[1,57,1283,14854,96024],"
             << "\"minimum_legal_next_moves\":[57,32,17,10,4],"
             << "\"maximum_legal_next_moves\":[57,51,46,41,35],"
             << "\"raw_four_move_paths\":2304576,"
             << "\"terminal_s10\":0,"
             << "\"geometry_cross_checks\":34845580,"
             << "\"evidence_level\":\"EXHAUSTIVE_FINITE_GEOMETRY_ONLY\","
             << "\"s7_outcome\":\"UNKNOWN\","
             << "\"s6_outcome\":\"UNKNOWN\","
             << "\"empty_board_outcome\":\"UNKNOWN\"}\n";
    } catch (const exception& e) {
        cerr << "FOCUS_EXTENSION_REFUSED: " << e.what() << '\n';
        return 1;
    }
}

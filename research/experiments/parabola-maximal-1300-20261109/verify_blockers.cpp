// Independently check an explicit forbidden quadruple for every missing point.
#define main unused_subset_main
#include "../parabola-local-repair-20261109/verify_subset.cpp"
#undef main
#include <fstream>
#include <string>
int main(int argc, char** argv) {
    if (argc != 3) return 2;
    std::ifstream candidate(argv[1]), certificate(argv[2]);
    int p, n, cp, m;
    if (!(candidate >> p >> n) || !prime(p) || p > 100000 || n < 0 || n > p) return 2;
    std::vector<bool> selected(p), seen(p);
    int previous = -1;
    for (int i=0; i<n; ++i) {
        int t;
        if (!(candidate >> t) || t < 0 || t >= p || t <= previous) return 3;
        selected[t] = true;
        previous = t;
    }
    std::string extra;
    if (candidate >> extra) return 2;
    if (!(certificate >> cp >> m) || cp != p || m != p-n) return 2;
    for (int i=0; i<m; ++i) {
        int t;
        std::array<int,4> q;
        if (!(certificate >> t)) return 2;
        for (int& v : q) if (!(certificate >> v)) return 2;
        if (t < 0 || t >= p || selected[t] || seen[t]) return 3;
        seen[t] = true;
        if (q[0] < 0 || q[3] >= p || !(q[0]<q[1] && q[1]<q[2] && q[2]<q[3])) return 3;
        int occurrences = 0;
        for (int v : q) {
            if (v == t) ++occurrences;
            else if (!selected[v]) return 3;
        }
        if (occurrences != 1 || determinant(q, p) != 0) return 4;
    }
    if (certificate >> extra) return 2;
    for (int t=0; t<p; ++t) if (!selected[t] && !seen[t]) return 3;
    std::cout << "VERIFIED_BLOCKERS " << p << ' ' << n << ' ' << m << '\n';
    return 0;
}

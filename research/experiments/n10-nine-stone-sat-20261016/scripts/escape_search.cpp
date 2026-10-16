// Targeted escape search for a nine-stone maximal safe set on 10x10.
//
// Phase 1: simulated annealing restarts until a state with covered=90 (all
//          but one outside point blocked) and unsafe=0 is reached.
// Phase 2: exhaustive enumeration of all 1-swap and 2-swap moves from that
//          state (optionally all 3-swap moves) to reach covered=91, unsafe=0.
// Repeat from fresh restarts.
//
// Usage: escape_search <seed> <radius:1|2|3> [max_plateaus]
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <random>
#include <vector>

using u64 = uint64_t;
using u128 = unsigned __int128;

static const int N = 10;
static const int V = 100;
static const int K = 9;
static const int NUM_TRIPLES = 161700;

struct Curve {
    long long A, B, C, D;
    u128 mask;
    int size;
};

static std::vector<Curve> g_curves;
static std::vector<int> g_rank;
static std::vector<int> g_triple_curve;

static long long gcdll(long long a, long long b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

static void canonical(long long c[4]) {
    if (c[0] < 0 || (c[0] == 0 && c[1] < 0) ||
        (c[0] == 0 && c[1] == 0 && c[2] < 0)) {
        for (int i = 0; i < 4; ++i) c[i] = -c[i];
    }
    long long g = 0;
    for (int i = 0; i < 4; ++i) g = gcdll(g, c[i]);
    if (g > 1) {
        for (int i = 0; i < 4; ++i) c[i] /= g;
    }
}

static void curve_through(int i, int j, int k, long long out[4]) {
    long long x1 = i % N, y1 = i / N;
    long long x2 = j % N, y2 = j / N;
    long long x3 = k % N, y3 = k / N;
    long long dx2 = x2 - x1, dy2 = y2 - y1;
    long long dx3 = x3 - x1, dy3 = y3 - y1;
    long long cross = dx2 * dy3 - dy2 * dx3;
    long long A, B, C;
    if (cross == 0) {
        A = 0;
        B = -dy2;
        C = dx2;
    } else {
        long long f2 = dx2 * dx2 + dy2 * dy2;
        long long f3 = dx3 * dx3 + dy3 * dy3;
        A = cross;
        B = f3 * dy2 - f2 * dy3;
        C = f2 * dx3 - f3 * dx2;
        B -= 2 * A * x1;
        C -= 2 * A * y1;
    }
    long long D = -(A * (x1 * x1 + y1 * y1) + B * x1 + C * y1);
    out[0] = A;
    out[1] = B;
    out[2] = C;
    out[3] = D;
    canonical(out);
}

static void build_geometry() {
    g_rank.assign(100 * 100 * 100, 0);
    g_triple_curve.assign(NUM_TRIPLES, 0);
    std::map<std::array<long long, 4>, int> ids;
    int r = 0;
    for (int i = 0; i < V; ++i) {
        for (int j = i + 1; j < V; ++j) {
            for (int k = j + 1; k < V; ++k) {
                g_rank[(i * 100 + j) * 100 + k] = r;
                long long sig[4];
                curve_through(i, j, k, sig);
                std::array<long long, 4> key = {sig[0], sig[1], sig[2], sig[3]};
                auto it = ids.find(key);
                int id;
                if (it == ids.end()) {
                    id = (int)g_curves.size();
                    ids[key] = id;
                    Curve c;
                    c.A = sig[0];
                    c.B = sig[1];
                    c.C = sig[2];
                    c.D = sig[3];
                    c.mask = 0;
                    c.size = 0;
                    g_curves.push_back(c);
                } else {
                    id = it->second;
                }
                g_triple_curve[r] = id;
                ++r;
            }
        }
    }
    for (size_t ci = 0; ci < g_curves.size(); ++ci) {
        Curve& c = g_curves[ci];
        u128 m = 0;
        for (int p = 0; p < V; ++p) {
            long long x = p % N, y = p / N;
            if (c.A * (x * x + y * y) + c.B * x + c.C * y + c.D == 0) {
                m |= (u128(1) << p);
            }
        }
        c.mask = m;
        c.size = __builtin_popcountll((u64)m) +
                 __builtin_popcountll((u64)(m >> 64));
    }
}

static inline int pc128(u128 v) {
    return __builtin_popcountll((u64)v) + __builtin_popcountll((u64)(v >> 64));
}

static int evaluate(const std::vector<int>& pts, u128 s, int* unsafe) {
    int un = 0;
    u128 blocked = 0;
    const int k = (int)pts.size();
    for (int a = 0; a < k; ++a) {
        for (int b = a + 1; b < k; ++b) {
            for (int c = b + 1; c < k; ++c) {
                int rk = g_rank[(pts[a] * 100 + pts[b]) * 100 + pts[c]];
                int id = g_triple_curve[rk];
                const Curve& cv = g_curves[id];
                int cnt = pc128(cv.mask & s);
                if (cnt > 3) ++un;
                else if (cnt == 3) blocked |= cv.mask & ~s;
            }
        }
    }
    *unsafe = un;
    return pc128(blocked);
}

static bool report_found(const std::vector<int>& pts) {
    std::printf("FOUND maximal safe set:");
    for (int v : pts) std::printf(" %d", v);
    std::printf("\n");
    std::fflush(stdout);
    return true;
}

int main(int argc, char** argv) {
    unsigned seed = argc > 1 ? (unsigned)std::atoi(argv[1]) : 1;
    int radius = argc > 2 ? std::atoi(argv[2]) : 2;
    long long max_plateaus = argc > 3 ? std::atoll(argv[3]) : 1000000;
    build_geometry();
    std::printf("curves=%zu triples=%d radius=%d seed=%u\n",
                g_curves.size(), NUM_TRIPLES, radius, seed);
    std::fflush(stdout);

    std::mt19937_64 rng(seed);
    long long plateaus = 0;
    long long sa_evals = 0, escape_evals = 0;

    for (long long outer = 0; plateaus < max_plateaus; ++outer) {
        std::vector<int> pts;
        u128 S = 0;
        while ((int)pts.size() < K) {
            int p = (int)(rng() % V);
            if (!((S >> p) & 1)) {
                S |= (u128(1) << p);
                pts.push_back(p);
            }
        }
        std::sort(pts.begin(), pts.end());
        int unsafe = 0;
        int covered = evaluate(pts, S, &unsafe);
        long long cur = (long long)covered - 10000LL * unsafe;
        double T = 3.0;
        const long long steps = 12000;
        for (long long it = 0; it < steps; ++it) {
            int drop = pts[rng() % K];
            int add = (int)(rng() % V);
            if ((S >> add) & 1) continue;
            u128 S2 = (S & ~(u128(1) << drop)) | (u128(1) << add);
            std::vector<int> pts2 = pts;
            for (auto& v : pts2) {
                if (v == drop) v = add;
            }
            std::sort(pts2.begin(), pts2.end());
            int u2 = 0;
            int c2 = evaluate(pts2, S2, &u2);
            ++sa_evals;
            long long sc = (long long)c2 - 10000LL * u2;
            bool accept = sc >= cur;
            if (!accept) {
                double ph = std::exp((double)(sc - cur) / T);
                accept = std::uniform_real_distribution<double>(0, 1)(rng) < ph;
            }
            if (accept) {
                pts.swap(pts2);
                S = S2;
                cur = sc;
                covered = c2;
                unsafe = u2;
            }
            T *= 0.9998;
            if (T < 0.05) T = 0.05;
            if (covered == 91 && unsafe == 0) {
                report_found(pts);
                return 0;
            }
        }
        if (!(covered == 90 && unsafe == 0)) continue;
        ++plateaus;

        // exhaustive 1-swap
        for (int di = 0; di < K; ++di) {
            for (int add = 0; add < V; ++add) {
                if ((S >> add) & 1) continue;
                u128 S2 = (S & ~(u128(1) << pts[di])) | (u128(1) << add);
                std::vector<int> pts2 = pts;
                pts2[di] = add;
                std::sort(pts2.begin(), pts2.end());
                int u2 = 0;
                int c2 = evaluate(pts2, S2, &u2);
                ++escape_evals;
                if (c2 == 91 && u2 == 0) {
                    report_found(pts2);
                    return 0;
                }
            }
        }

        // exhaustive 2-swap
        for (int i = 0; i < K; ++i) {
            for (int j = i + 1; j < K; ++j) {
                u128 base = S & ~(u128(1) << pts[i]) & ~(u128(1) << pts[j]);
                for (int a1 = 0; a1 < V; ++a1) {
                    if (base >> a1 & 1) continue;
                    for (int a2 = a1 + 1; a2 < V; ++a2) {
                        if (base >> a2 & 1) continue;
                        u128 S2 = base | (u128(1) << a1) | (u128(1) << a2);
                        std::vector<int> pts2 = pts;
                        pts2[i] = a1;
                        pts2[j] = a2;
                        std::sort(pts2.begin(), pts2.end());
                        int u2 = 0;
                        int c2 = evaluate(pts2, S2, &u2);
                        ++escape_evals;
                        if (c2 == 91 && u2 == 0) {
                            report_found(pts2);
                            return 0;
                        }
                    }
                }
            }
        }

        if (radius >= 3) {
            // exhaustive 3-swap
            for (int i = 0; i < K; ++i) {
                for (int j = i + 1; j < K; ++j) {
                    for (int l = j + 1; l < K; ++l) {
                        u128 base = S & ~(u128(1) << pts[i]) &
                                    ~(u128(1) << pts[j]) & ~(u128(1) << pts[l]);
                        for (int a1 = 0; a1 < V; ++a1) {
                            if (base >> a1 & 1) continue;
                            for (int a2 = a1 + 1; a2 < V; ++a2) {
                                if (base >> a2 & 1) continue;
                                for (int a3 = a2 + 1; a3 < V; ++a3) {
                                    if (base >> a3 & 1) continue;
                                    u128 S2 = base | (u128(1) << a1) |
                                              (u128(1) << a2) |
                                              (u128(1) << a3);
                                    std::vector<int> pts2 = pts;
                                    pts2[i] = a1;
                                    pts2[j] = a2;
                                    pts2[l] = a3;
                                    std::sort(pts2.begin(), pts2.end());
                                    int u2 = 0;
                                    int c2 = evaluate(pts2, S2, &u2);
                                    ++escape_evals;
                                    if (c2 == 91 && u2 == 0) {
                                        report_found(pts2);
                                        return 0;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        std::printf("plateau %lld escaped=no sa_evals=%lld escape_evals=%lld\n",
                    plateaus, sa_evals, escape_evals);
        std::fflush(stdout);
    }
    std::printf("done no escape found, plateaus=%lld\n", plateaus);
    return 0;
}

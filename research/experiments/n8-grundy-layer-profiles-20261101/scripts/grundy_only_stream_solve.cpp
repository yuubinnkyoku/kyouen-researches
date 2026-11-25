// Grundy-only streaming DP over spilled safe-set levels (square boards n<=8).
//
// Consumes level_k.occ (sorted u64 occupancy masks per safe-set layer) produced
// by the validated enumerator round5_prand_stream.cpp --enum, and computes
// g(S) = mex{g(S | (1<<v)) : v legal} for EVERY safe set, descending from the
// terminal layer. Two layers are resident at a time: child masks via mmap
// (reclaimable page cache), parent masks streamed in chunks, DP values 1 B/state.
//
// Outputs per level k:
//   dp_k.bin   int8 Grundy value per state, index-aligned with level_k.occ
// and a JSON summary: level sizes, P/N counts, per-level g histogram, layer max
// M_n(k), first ceiling-attaining witness, root g, timings, peak RSS.
//
// Memory: O(|L_k| + |L_{k+1}|) anonymous bytes (widest pair ~4 GB at n=8),
// versus ~19 GB for the combined grundy+p_rand DP. This is the enabling change
// for rerunning the n=8 DP on the 19 GiB WSL box.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cmath>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#ifdef _OPENMP
#include <omp.h>
#endif
#include "../../../../scripts/research/kc_core.h"

using kc::u64;

static double now_s() {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}
static double rss_cur_gb() {
    FILE* f = fopen("/proc/self/status", "r"); if (!f) return -1;
    char line[256]; double v = 0;
    while (fgets(line, sizeof line, f))
        if (strncmp(line, "VmRSS:", 6) == 0) { long long x; sscanf(line+6, "%lld", &x); v = x/1048576.0; break; }
    fclose(f); return v;
}
static double rss_peak_gb() {
    FILE* f = fopen("/proc/self/status", "r"); if (!f) return -1;
    char line[256]; long long v = -1;
    while (fgets(line, sizeof line, f))
        if (strncmp(line, "VmHWM:", 6) == 0) { sscanf(line+6, "%lld", &v); break; }
    fclose(f); return v/1048576.0;
}

// ============================================================ context
struct Ctx {
    kc::Board board;
    int n = 0, V = 0;
    std::vector<u64> quads;
    u64 FULL = 0;
    u64 triple_blk[64][64][64] = {};
};
static void build_ctx(Ctx& ctx, int n) {
    kc::build_square(ctx.board, n);
    ctx.n = n; ctx.V = ctx.board.V; ctx.FULL = ctx.board.full;
    ctx.quads = ctx.board.quads;
    std::sort(ctx.quads.begin(), ctx.quads.end());
    memset(ctx.triple_blk, 0, sizeof(ctx.triple_blk));
    for (u64 q : ctx.quads) {
        int p[4], cnt = 0; u64 t = q;
        while (t) { p[cnt++] = __builtin_ctzll(t); t &= t-1; }
        if (cnt != 4) continue;
        ctx.triple_blk[p[0]][p[1]][p[2]] |= (u64(1)<<p[3]);
        ctx.triple_blk[p[0]][p[1]][p[3]] |= (u64(1)<<p[2]);
        ctx.triple_blk[p[0]][p[2]][p[3]] |= (u64(1)<<p[1]);
        ctx.triple_blk[p[1]][p[2]][p[3]] |= (u64(1)<<p[0]);
    }
}
static inline u64 legal_one(const Ctx& ctx, u64 occ) {
    u64 empty = ctx.FULL & ~occ, blocked = 0;
    u64 o1 = occ;
    while (o1) {
        int p1 = __builtin_ctzll(o1); o1 &= o1-1;
        u64 o2 = o1;
        while (o2) {
            int p2 = __builtin_ctzll(o2); o2 &= o2-1;
            u64 o3 = o2;
            while (o3) {
                int p3 = __builtin_ctzll(o3); o3 &= o3-1;
                blocked |= ctx.triple_blk[p1][p2][p3];
            }
        }
    }
    return empty & ~blocked;
}
static inline int hib(u64 x) { return x ? (63 - __builtin_clzll(x)) : -1; }

// ============================================================ file helpers
static size_t file_states(const std::string& path) {
    struct stat st;
    if (stat(path.c_str(), &st) != 0) return 0;
    return (size_t)(st.st_size / 8);
}
static std::string dp_path(const std::string& dir, int k) {
    return dir + "/dp_" + std::to_string(k) + ".bin";
}
static void save_g(const std::string& path, const int8_t* vals, size_t n) {
    FILE* f = fopen(path.c_str(), "wb");
    if (!f) { fprintf(stderr, "cannot write %s\n", path.c_str()); exit(7); }
    if (n && fwrite(vals, 1, n, f) != n) { fprintf(stderr, "short write %s\n", path.c_str()); exit(7); }
    fclose(f);
}

struct MappedLevel {
    int fd = -1;
    const u64* data = nullptr;
    size_t n = 0;
    void open(const std::string& path) {
        fd = ::open(path.c_str(), O_RDONLY);
        if (fd < 0) { fprintf(stderr, "cannot open %s\n", path.c_str()); exit(7); }
        struct stat st; fstat(fd, &st);
        n = (size_t)(st.st_size / 8);
        data = (const u64*)mmap(nullptr, (size_t)st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
        if (data == MAP_FAILED) { fprintf(stderr, "mmap fail %s\n", path.c_str()); exit(7); }
    }
    void close() {
        if (data && data != MAP_FAILED) munmap((void*)data, n * 8);
        if (fd >= 0) ::close(fd);
        data = nullptr; fd = -1; n = 0;
    }
    ~MappedLevel() { close(); }
};

// ============================================================ level summary
struct LevelSummary {
    size_t size = 0, edges = 0;
    long long nP = 0, nN = 0;
    int gmax = -1;
    u64 witness_mask = 0;
    size_t witness_idx = 0;
    uint64_t hist[32] = {};
    double secs = 0.0;
};

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <n> --spill=dir [--out=f.json] [--chunk=N]\n", argv[0]);
        return 2;
    }
    int n = atoi(argv[1]);
    std::string spill, outpath;
    size_t CHUNK = 2000000;
    for (int i = 2; i < argc; ++i) {
        std::string a = argv[i];
        if (a.rfind("--spill=", 0) == 0) spill = a.substr(8);
        else if (a.rfind("--out=", 0) == 0) outpath = a.substr(6);
        else if (a.rfind("--chunk=", 0) == 0) CHUNK = (size_t)atol(a.c_str() + 8);
    }
    if (spill.empty()) { fprintf(stderr, "need --spill=dir\n"); return 2; }

    Ctx ctx; build_ctx(ctx, n);
    fprintf(stderr, "[grundy-solve n=%d] V=%d F=%zu spill=%s\n", n, ctx.V, ctx.quads.size(), spill.c_str());
    fflush(stderr);

    // Discover levels
    std::vector<size_t> lsizes;
    for (int k = 0; k <= ctx.V + 2; ++k) {
        size_t sz = file_states(spill + "/level_" + std::to_string(k) + ".occ");
        if (sz == 0) break;
        lsizes.push_back(sz);
    }
    if (lsizes.empty()) { fprintf(stderr, "no level files in %s\n", spill.c_str()); return 3; }
    int K = (int)lsizes.size() - 1;

    // Terminal level K: all maximal, g=0.
    std::vector<int8_t> dp_next(lsizes[K], 0);

    std::vector<LevelSummary> st(K + 1);
    st[K].size = lsizes[K];
    st[K].hist[0] = lsizes[K];
    st[K].nP = (long long)lsizes[K];
    st[K].gmax = 0;  // all terminal (maximal) sets have g=0

    double t0 = now_s();
    long long edge_total = 0;

    for (int k = K - 1; k >= 0; --k) {
        double tk = now_s();
        size_t Mk = lsizes[k], Mk1 = lsizes[k + 1];

        MappedLevel child_lvl;
        child_lvl.open(spill + "/level_" + std::to_string(k + 1) + ".occ");
        if (child_lvl.n != Mk1) {
            fprintf(stderr, "child size mismatch k=%d: %zu vs %zu\n", k, child_lvl.n, Mk1);
            exit(6);
        }
        if (dp_next.size() != Mk1) {
            fprintf(stderr, "dp_next size mismatch k=%d: %zu vs %zu\n", k, dp_next.size(), Mk1);
            exit(6);
        }

        std::vector<int8_t> dp_k(Mk, 0);
        std::vector<u64> buf(CHUNK);
        int fd_k = open((spill + "/level_" + std::to_string(k) + ".occ").c_str(), O_RDONLY);
        if (fd_k < 0) { fprintf(stderr, "cannot open level %d\n", k); exit(7); }

        long long nP = 0, nN = 0, edges = 0;
        int gmax = -1; u64 witness_mask = 0; size_t witness_idx = 0;
        uint64_t hist[32] = {};

        for (size_t done = 0; done < Mk; ) {
            size_t want = std::min(CHUNK, Mk - done);
            ssize_t want_b = (ssize_t)(want * 8);
            char* dst = (char*)buf.data();
            ssize_t got = 0;
            while (got < want_b) {
                ssize_t r = read(fd_k, dst + got, (size_t)(want_b - got));
                if (r <= 0) { fprintf(stderr, "short read level %d\n", k); exit(7); }
                got += r;
            }
#pragma omp parallel for schedule(dynamic, 256) reduction(+:nP,nN,edges)
            for (long long ii = 0; ii < (long long)want; ++ii) {
                size_t i = (size_t)ii;
                u64 S = buf[i];
                u64 lm = legal_one(ctx, S);
                int deg = __builtin_popcountll(lm);
                edges += deg;
                int8_t g = 0;
                if (deg) {
                    u64 gm = 0;
                    while (lm) {
                        int v = __builtin_ctzll(lm); lm &= lm - 1;
                        u64 child = S | (u64(1) << v);
                        const u64* Np = child_lvl.data;
                        size_t lo = 0, hi = child_lvl.n;
                        while (lo < hi) {
                            size_t mid = (lo + hi) / 2;
                            if (Np[mid] < child) lo = mid + 1;
                            else hi = mid;
                        }
                        if (lo >= child_lvl.n || Np[lo] != child) {
#pragma omp critical
                            { fprintf(stderr, "CHILD NOT FOUND k=%d S=%#llx child=%#llx\n",
                                      k, (unsigned long long)S, (unsigned long long)child); exit(4); }
                        }
                        gm |= (u64(1) << dp_next[lo]);
                    }
                    g = (int8_t)__builtin_ctzll((~gm) & (gm + 1));
                }
                dp_k[done + i] = g;
                if (g == 0) ++nP; else ++nN;
            }
            done += want;
        }
        close(fd_k);
        child_lvl.close();

        // histogram + witness (serial; dp_k is ready)
        for (size_t i = 0; i < Mk; ++i) {
            int g = dp_k[i];
            if (g < 0 || g >= 32) { fprintf(stderr, "g out of range k=%d i=%zu g=%d\n", k, i, g); exit(8); }
            hist[g]++;
            if (g > gmax) { gmax = g; witness_mask = 0; witness_idx = i; }
        }
        // witness mask: first index attaining gmax (re-read from level file)
        {
            int fd = open((spill + "/level_" + std::to_string(k) + ".occ").c_str(), O_RDONLY);
            if (fd >= 0) {
                u64 target = 0;
                size_t want_idx = 0;
                for (size_t i = 0; i < Mk; ++i) if (dp_k[i] == gmax) { want_idx = i; break; }
                if (pread(fd, &target, 8, (off_t)want_idx * 8) == 8) witness_mask = target;
                witness_idx = want_idx;
                close(fd);
            }
        }

        save_g(dp_path(spill, k), dp_k.data(), Mk);
        dp_next = std::move(dp_k);

        LevelSummary& s = st[k];
        s.size = Mk; s.edges = edges; s.nP = nP; s.nN = nN;
        s.gmax = gmax; s.witness_mask = witness_mask; s.witness_idx = witness_idx;
        for (int g = 0; g < 32; ++g) s.hist[g] = hist[g];
        s.secs = now_s() - tk;
        edge_total += (long long)edges;

        fprintf(stderr, "  k=%2d M=%12zu E=%12lld P=%9lld N=%9lld gmax=%2d %.1fs rss=%.2fGB peak=%.2fGB\n",
                k, Mk, edges, nP, nN, gmax, s.secs, rss_cur_gb(), rss_peak_gb());
        fflush(stderr);
    }
    double total_s = now_s() - t0;

    // ============================================================ JSON
    std::string o = "{\n";
    char b[2048];
    o += "  \"n\": " + std::to_string(n) + ",\n";
    o += "  \"V\": " + std::to_string(ctx.V) + ",\n";
    o += "  \"F\": " + std::to_string(ctx.quads.size()) + ",\n";
    o += "  \"method\": \"grundy-only streaming DP: int8 g per state (1 B/state), child masks via mmap, "
         "parent streamed in chunks, legal_one via 3-subset table, mex from child g bitmask\",\n";
    size_t total_states = std::accumulate(lsizes.begin(), lsizes.end(), (size_t)0);
    o += "  \"n_safe_subsets\": " + std::to_string(total_states) + ",\n";
    o += "  \"max_safe_size\": " + std::to_string(K) + ",\n";
    o += "  \"edge_total\": " + std::to_string(edge_total) + ",\n";
    long long totP = 0, totN = 0;
    for (int k = 0; k <= K; ++k) { totP += st[k].nP; totN += st[k].nN; }
    o += "  \"n_P\": " + std::to_string(totP) + ",\n";
    o += "  \"n_N\": " + std::to_string(totN) + ",\n";
    snprintf(b, sizeof b, "  \"g_root\": %d,\n", (int)dp_next[0]); o += b;
    o += "  \"level_sizes\": [";
    for (int k = 0; k <= K; ++k) o += (k ? "," : "") + std::to_string(lsizes[k]);
    o += "],\n";
    o += "  \"M_n_k\": [";
    for (int k = 0; k <= K; ++k) o += (k ? "," : "") + std::to_string(st[k].gmax);
    o += "],\n";
    o += "  \"levels\": [\n";
    for (int k = 0; k <= K; ++k) {
        std::string h = "[";
        for (int g = 0; g < 32; ++g) h += (g ? "," : "") + std::to_string(st[k].hist[g]);
        h += "]";
        char wb[64];
        snprintf(wb, sizeof wb, "%llu", (unsigned long long)st[k].witness_mask);
        snprintf(b, sizeof b,
                 "    {\"k\": %d, \"size\": %zu, \"edges\": %zu, \"nP\": %lld, \"nN\": %lld, "
                 "\"gmax\": %d, \"witness_idx\": %zu, \"witness_mask\": \"%s\", \"hist\": %s, \"secs\": %.2f}",
                 k, st[k].size, st[k].edges, st[k].nP, st[k].nN, st[k].gmax,
                 st[k].witness_idx, wb, h.c_str(), st[k].secs);
        o += b;
        if (k < K) o += ",";
        o += "\n";
    }
    o += "  ],\n";
    snprintf(b, sizeof b, "  \"solve_seconds\": %.1f,\n", total_s); o += b;
    snprintf(b, sizeof b, "  \"peak_rss_gb\": %.3f\n", rss_peak_gb()); o += b;
    o += "}\n";
    printf("%s", o.c_str());
    if (!outpath.empty()) {
        FILE* f = fopen(outpath.c_str(), "w");
        if (f) { fputs(o.c_str(), f); fclose(f); fprintf(stderr, "wrote %s\n", outpath.c_str()); }
    }
    return 0;
}

// Independent terminal-closed native proof checker. No solver headers/imports.
// Four-point geometry is the integer determinant of rows (x,y,x*x+y*y,1).
// Subtracting the first row reduces this exactly to a 3-by-3 determinant.
#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>
#include <zlib.h>

using Mask = __uint128_t;
constexpr uint32_t NONE = std::numeric_limits<uint32_t>::max();

[[noreturn]] void fail(const std::string& s) { throw std::runtime_error(s); }
int count(Mask m) { return __builtin_popcountll(uint64_t(m)) + __builtin_popcountll(uint64_t(m >> 64)); }
std::string decimal(Mask m) {
    if (!m) return "0";
    std::string s;
    while (m) { s.push_back(char('0' + m % 10)); m /= 10; }
    std::reverse(s.begin(), s.end()); return s;
}
uint64_t number(std::string_view s) {
    uint64_t v = 0;
    auto r = std::from_chars(s.data(), s.data() + s.size(), v);
    if (s.empty() || r.ec != std::errc() || r.ptr != s.data() + s.size()) fail("invalid unsigned integer");
    return v;
}
Mask mask_decimal(std::string_view s) {
    Mask v = 0, maximum = ~Mask(0);
    if (s.empty()) fail("empty mask");
    for (char c : s) {
        if (c < '0' || c > '9' || v > (maximum - (c - '0')) / 10) fail("invalid 128-bit mask");
        v = v * 10 + c - '0';
    }
    return v;
}
struct Hash {
    static uint64_t mix(uint64_t x) { x += 0x9e3779b97f4a7c15ULL; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL; x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL; return x ^ (x >> 31); }
    size_t operator()(Mask m) const { return mix(uint64_t(m)) ^ mix(uint64_t(m >> 64)); }
};
std::vector<int> points(Mask m) {
    std::vector<int> p; p.reserve(count(m));
    uint64_t lo = uint64_t(m), hi = uint64_t(m >> 64);
    while (lo) { p.push_back(__builtin_ctzll(lo)); lo &= lo - 1; }
    while (hi) { p.push_back(64 + __builtin_ctzll(hi)); hi &= hi - 1; }
    return p;
}

struct Board {
    int n, size;
    Mask full;
    std::array<std::array<Mask, 121>, 8> maps{};
    std::vector<Mask> triples;
    std::array<int, 122> c2{}, c3{};
    explicit Board(int n_) : n(n_), size(n*n), full((Mask(1) << size) - 1) {
        for (int i = 0; i <= size; ++i) { c2[i] = i * (i-1) / 2; c3[i] = i * (i-1) * (i-2) / 6; }
        for (int p = 0; p < size; ++p) {
            int x = p % n, y = p / n, m = n - 1;
            std::array<std::pair<int,int>,8> images{{{x,y},{m-y,x},{m-x,m-y},{y,m-x},{m-x,y},{m-y,m-x},{x,m-y},{y,x}}};
            for (int t = 0; t < 8; ++t) maps[t][p] = Mask(1) << (images[t].second*n + images[t].first);
        }
        triples.resize(c3[size]);
        for (int c = 2; c < size; ++c) for (int b = 1; b < c; ++b) for (int a = 0; a < b; ++a) {
            int64_t ax = a % n, ay = a / n, aq = ax*ax + ay*ay;
            int64_t bx = b % n - ax, by = b / n - ay;
            int64_t bq = (b%n)*(b%n) + (b/n)*(b/n) - aq;
            int64_t cx = c % n - ax, cy = c / n - ay;
            int64_t cq = (c%n)*(c%n) + (c/n)*(c/n) - aq;
            Mask completion = 0;
            for (int p = 0; p < size; ++p) {
                int64_t px = p % n - ax, py = p / n - ay;
                int64_t pq = (p%n)*(p%n) + (p/n)*(p/n) - aq;
                int64_t det = bx*(cy*pq - cq*py) - by*(cx*pq - cq*px) + bq*(cx*py - cy*px);
                if (!det) completion |= Mask(1) << p;
            }
            triples[c3[c]+c2[b]+a] = completion;
        }
    }
    Mask canonical(Mask m, const std::vector<int>& ps) const {
        Mask best = m;
        for (int t = 1; t < 8; ++t) { Mask v = 0; for (int p : ps) v |= maps[t][p]; if (v < best) best = v; }
        return best;
    }
    Mask canonical(Mask m) const { return canonical(m, points(m)); }
    Mask legal(Mask m, const std::vector<int>& ps) const {
        if (m & ~full) fail("out-of-board node " + decimal(m));
        Mask blocked = m;
        for (size_t k = 2; k < ps.size(); ++k) for (size_t j = 1; j < k; ++j) for (size_t i = 0; i < j; ++i) {
            int a = ps[i], b = ps[j], c = ps[k];
            Mask completion = triples[c3[c]+c2[b]+a];
            Mask triple = (Mask(1)<<a) | (Mask(1)<<b) | (Mask(1)<<c);
            if (completion & (m ^ triple)) fail("unsafe occupied node " + decimal(m));
            blocked |= completion;
        }
        return full & ~blocked;
    }
};

struct Edge { Mask child; uint32_t next = NONE; uint8_t move = 0; };
struct Node {
    Mask mask;
    uint32_t first = NONE, edge_count = 0;
    uint8_t verdict = 0, terminal = 0, state = 0, legal_count = 0;
};
struct Reader {
    std::ifstream plain;
    gzFile zip = nullptr;
    explicit Reader(const std::string& path) {
        if (path.size() >= 3 && path.substr(path.size()-3) == ".gz") {
            zip = gzopen(path.c_str(), "rb");
            if (!zip) fail("cannot open trace");
            gzbuffer(zip, 1 << 20);
        } else { plain.open(path); if (!plain) fail("cannot open trace"); }
    }
    ~Reader() { if (zip) gzclose(zip); }
    bool line(std::string& s) {
        if (!zip) { if (std::getline(plain, s)) return true; if (!plain.eof()) fail("trace read error"); return false; }
        std::array<char,1024> buffer{};
        s.clear();
        while (gzgets(zip, buffer.data(), buffer.size())) {
            s += buffer.data();
            if (!s.empty() && s.back() == '\n') { s.pop_back(); return true; }
            if (s.size() > 4096) fail("overlong trace line");
        }
        int error = Z_OK; gzerror(zip, &error);
        if (error != Z_OK && error != Z_STREAM_END) fail("gzip trace read error");
        return !s.empty();
    }
};
struct Writer {
    std::ofstream plain;
    gzFile zip = nullptr;
    explicit Writer(const std::string& path) {
        if (path.size() >= 3 && path.substr(path.size()-3) == ".gz") { zip = gzopen(path.c_str(), "wb6"); if (!zip) fail("cannot create output"); gzbuffer(zip, 1 << 20); }
        else { plain.open(path); if (!plain) fail("cannot create output"); }
    }
    ~Writer() { if (zip) gzclose(zip); }
    void write(const std::string& s) {
        if (zip) { if (gzwrite(zip, s.data(), unsigned(s.size())) != int(s.size())) fail("gzip output write error"); }
        else { plain << s; if (!plain) fail("output write error"); }
    }
    void finish() {
        if (zip) { int code = gzclose(zip); zip = nullptr; if (code != Z_OK) fail("gzip output close error"); }
        else { plain.close(); if (!plain) fail("output close error"); }
    }
};
std::vector<std::string_view> fields(const std::string& s) {
    std::vector<std::string_view> v;
    size_t start = 0;
    while (true) { size_t end = s.find(',', start); v.emplace_back(s.data()+start, (end == std::string::npos ? s.size() : end)-start); if (end == std::string::npos) return v; start = end+1; }
}

struct Proof {
    int n = 0, root_verdict = 0;
    Mask root = 0;
    std::vector<Node> nodes;
    std::vector<Edge> edges;
    std::unordered_map<Mask,uint32_t,Hash> ids;
    size_t defined_nodes = 0, reachable_nodes = 0, reachable_edges = 0, terminals = 0;
    Board* board = nullptr;
    uint32_t intern(Mask mask) {
        auto it = ids.find(mask); if (it != ids.end()) return it->second;
        if (nodes.size() >= NONE) fail("too many nodes");
        uint32_t id = uint32_t(nodes.size()); ids.emplace(mask, id); nodes.push_back(Node{mask}); return id;
    }
    void load(const std::string& path) {
        Reader in(path); std::string line;
        if (!in.line(line)) fail("missing trace header");
        if (!line.empty() && line.back() == '\r') line.pop_back();
        auto h = fields(line);
        if (h.size() != 5 || h[0] != "# kyouen-proof-trace-v1" || h[1].substr(0,2) != "n=" || h[2].substr(0,8) != "root_lo=" || h[3].substr(0,8) != "root_hi=" || h[4].substr(0,8) != "verdict=") fail("invalid trace header");
        uint64_t parsed_n = number(h[1].substr(2)), parsed_verdict = number(h[4].substr(8));
        if (parsed_n < 1 || parsed_n > 11 || parsed_verdict < 1 || parsed_verdict > 2) fail("invalid board size/root verdict");
        n = int(parsed_n); root_verdict = int(parsed_verdict);
        root = Mask(number(h[2].substr(8))) | (Mask(number(h[3].substr(8))) << 64);
        ids.reserve(1 << 20); nodes.reserve(1 << 20); edges.reserve(1 << 20);
        size_t line_no = 1;
        while (in.line(line)) {
            ++line_no; if (!line.empty() && line.back() == '\r') line.pop_back();
            if (line.empty()) continue;
            try {
                auto f = fields(line);
                if (f.size() == 5 && f[0] == "N") {
                    Mask mask = Mask(number(f[1])) | (Mask(number(f[2])) << 64);
                    auto v = number(f[3]), t = number(f[4]);
                    if (v < 1 || v > 2 || t > 1) fail("invalid node verdict/terminal marker");
                    uint32_t id = intern(mask);
                    if (nodes[id].verdict) fail("duplicate node");
                    nodes[id].verdict = uint8_t(v); nodes[id].terminal = uint8_t(t); ++defined_nodes;
                } else if (f.size() == 6 && f[0] == "E") {
                    Mask parent = Mask(number(f[1])) | (Mask(number(f[2])) << 64);
                    auto move = number(f[3]); if (move >= uint64_t(n*n)) fail("out-of-board move label");
                    Mask child = Mask(number(f[4])) | (Mask(number(f[5])) << 64);
                    uint32_t id = intern(parent);
                    if (edges.size() >= NONE) fail("too many edges");
                    edges.push_back(Edge{child,nodes[id].first,uint8_t(move)});
                    nodes[id].first = uint32_t(edges.size()-1); ++nodes[id].edge_count;
                } else fail("malformed proof row");
            } catch (const std::exception& e) { fail("line " + std::to_string(line_no) + ": " + e.what()); }
        }
        auto it = ids.find(root);
        if (it == ids.end() || nodes[it->second].verdict != root_verdict) fail("missing root or header/root verdict disagreement");
    }
    void visit(uint32_t id) {
        Node& node = nodes[id];
        if (node.state == 2) return;
        if (node.state == 1) fail("cycle");
        if (!node.verdict) fail("reachable edge references undefined node");
        if (node.mask & ~board->full) fail("out-of-board reachable node");
        auto ps = points(node.mask);
        if (board->canonical(node.mask,ps) != node.mask) fail("noncanonical reachable node " + decimal(node.mask));
        Mask legal = board->legal(node.mask,ps);
        node.legal_count = uint8_t(count(legal));
        if (node.terminal != !legal) fail("terminal marker disagrees with geometry " + decimal(node.mask));
        node.state = 1;
        Mask labels = 0;
        bool existential = node.verdict == (ps.size()%2 ? 2 : 1);
        if (!legal) {
            if (node.first != NONE || node.verdict != (ps.size()%2 ? 1 : 2)) fail("incorrect terminal edges/parity");
            ++terminals;
        } else {
            if (existential && node.edge_count != 1) fail("existential node must carry exactly one witness");
            if (!existential && node.edge_count != unsigned(node.legal_count)) fail("universal node has incomplete legal boundary");
            for (uint32_t e = node.first; e != NONE; e = edges[e].next) {
                const Edge& edge = edges[e]; Mask bit = Mask(1) << edge.move;
                if (!(legal & bit) || labels & bit) fail("illegal or duplicate concrete move label");
                labels |= bit;
                auto it = ids.find(edge.child);
                if (it == ids.end() || !nodes[it->second].verdict) fail("reachable edge references missing child");
                if (count(edge.child) != int(ps.size())+1 || edge.child != board->canonical(node.mask | bit)) fail("incorrect ranked canonical transition");
                if (nodes[it->second].verdict != node.verdict) fail("incorrect fixed-player child polarity");
                visit(it->second); ++reachable_edges;
            }
            if (!existential && labels != legal) fail("universal node omits a concrete legal move");
        }
        node.state = 2; ++reachable_nodes;
    }
    std::vector<uint32_t> retained() const {
        std::vector<uint32_t> v; v.reserve(reachable_nodes);
        for (uint32_t i = 0; i < nodes.size(); ++i) if (nodes[i].state == 2) v.push_back(i);
        std::sort(v.begin(),v.end(),[&](uint32_t a,uint32_t b){return nodes[a].mask < nodes[b].mask;}); return v;
    }
    std::vector<uint32_t> sorted_edges(uint32_t id) const {
        std::vector<uint32_t> es;
        for (uint32_t e = nodes[id].first; e != NONE; e = edges[e].next) es.push_back(e);
        std::sort(es.begin(),es.end(),[&](uint32_t a,uint32_t b){return edges[a].move < edges[b].move;}); return es;
    }
    void output_trace(const std::string& path, const std::vector<uint32_t>& keep) const {
        Writer w(path);
        w.write("# kyouen-proof-trace-v1,n="+std::to_string(n)+",root_lo="+std::to_string(uint64_t(root))+",root_hi="+std::to_string(uint64_t(root>>64))+",verdict="+std::to_string(root_verdict)+"\n");
        for (uint32_t id : keep) {
            const Node& x = nodes[id];
            std::string key = std::to_string(uint64_t(x.mask))+","+std::to_string(uint64_t(x.mask>>64));
            w.write("N,"+key+","+std::to_string(x.verdict)+","+std::to_string(x.terminal)+"\n");
            for (uint32_t e : sorted_edges(id)) w.write("E,"+key+","+std::to_string(edges[e].move)+","+std::to_string(uint64_t(edges[e].child))+","+std::to_string(uint64_t(edges[e].child>>64))+"\n");
        }
        w.finish();
    }
    void output_json(const std::string& path, const std::vector<uint32_t>& keep) const {
        Writer w(path);
        w.write("{\"schema\":\"kyouen-proof-dag-edge-v1\",\"board_size\":"+std::to_string(n)+",\"proposition\":\"original_first_player_wins\",\"root\":\""+decimal(root)+"\",\"nodes\":{");
        bool first = true;
        for (uint32_t id : keep) {
            const Node& x = nodes[id]; std::string m = decimal(x.mask);
            if (!first) w.write(",");
            first = false;
            w.write("\""+m+"\":{\"mask\":\""+m+"\",\"stones\":"+std::to_string(count(x.mask))+",\"verdict\":"+std::to_string(x.verdict)+",\"terminal\":"+(x.terminal?"true":"false")+",\"legal_count\":"+std::to_string(x.legal_count)+",\"edges\":[");
            bool first_edge = true;
            for (uint32_t e : sorted_edges(id)) { if (!first_edge) w.write(","); first_edge = false; w.write("{\"move\":"+std::to_string(edges[e].move)+",\"child\":\""+decimal(edges[e].child)+"\"}"); }
            w.write("]}");
        }
        w.write("}}\n"); w.finish();
    }
};

int main(int argc, char** argv) {
    try {
        if (argc < 2) fail("usage: check_trace TRACE[.gz] [--pruned TRACE.csv[.gz]] [--json-dag DAG.json[.gz]] [--expect-root DECIMAL] [--expect-verdict 1|2]");
        std::string trace = argv[1], pruned, json, expected_root;
        uint64_t expected_verdict = 0;
        for (int i = 2; i < argc; i += 2) {
            if (i+1 >= argc) fail("missing option value");
            std::string key = argv[i], value = argv[i+1];
            if (key == "--pruned") pruned = value;
            else if (key == "--json-dag") json = value;
            else if (key == "--expect-root") expected_root = value;
            else if (key == "--expect-verdict") { expected_verdict = number(value); if (expected_verdict < 1 || expected_verdict > 2) fail("invalid expected verdict"); }
            else fail("unknown option " + key);
        }
        if (trace == pruned || trace == json || (!pruned.empty() && pruned == json)) fail("input/output paths must differ");
        auto start = std::chrono::steady_clock::now();
        Proof proof; proof.load(trace);
        if (!expected_root.empty() && proof.root != mask_decimal(expected_root)) fail("root does not match external expectation");
        if (expected_verdict && proof.root_verdict != int(expected_verdict)) fail("verdict does not match external expectation");
        auto loaded = std::chrono::steady_clock::now();
        Board board(proof.n); proof.board = &board; proof.visit(proof.ids.at(proof.root));
        auto verified = std::chrono::steady_clock::now();
        if (!pruned.empty() || !json.empty()) {
            auto keep = proof.retained();
            if (!pruned.empty()) proof.output_trace(pruned, keep);
            if (!json.empty()) proof.output_json(json, keep);
        }
        auto end = std::chrono::steady_clock::now();
        auto seconds = [](auto a, auto b) { return std::chrono::duration<double>(b-a).count(); };
        std::cout << "{\"verdict\":" << proof.root_verdict << ",\"board_size\":" << proof.n
                  << ",\"root_mask\":\"" << decimal(proof.root) << "\",\"nodes\":" << proof.reachable_nodes
                  << ",\"edges\":" << proof.reachable_edges << ",\"terminal_nodes\":" << proof.terminals
                  << ",\"trusted_leaves\":0,\"trace_nodes\":" << proof.defined_nodes << ",\"trace_edges\":" << proof.edges.size()
                  << ",\"orphan_nodes\":" << proof.defined_nodes-proof.reachable_nodes
                  << ",\"load_seconds\":" << seconds(start,loaded) << ",\"verify_seconds\":" << seconds(loaded,verified)
                  << ",\"output_seconds\":" << seconds(verified,end) << ",\"total_seconds\":" << seconds(start,end) << "}\n";
        return 0;
    } catch (const std::exception& e) { std::cerr << "REJECT: " << e.what() << '\n'; return 1; }
}

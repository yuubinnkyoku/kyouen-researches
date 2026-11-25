// Bounded residual sampling using the shared 128-bit geometry core.
// No game verdicts, long search, or shared cache writes are performed.
#include "../../../../scripts/research/kc_core121.h"
#include <cstdio>
#include <map>
#include <random>
#include <set>
#include <stdexcept>
#include <vector>

static std::vector<int> points(kc::Bits b) {
    std::vector<int> out;
    while (b.lo) { int v=__builtin_ctzll(b.lo); b.lo&=b.lo-1; out.push_back(v); }
    while (b.hi) { int v=__builtin_ctzll(b.hi); b.hi&=b.hi-1; out.push_back(v+64); }
    return out;
}

static std::vector<kc::Bits> residual(const kc::Board& board, kc::Bits occupied,
                                     kc::Bits legal) {
    std::set<kc::Bits> candidates;
    for (auto q:board.quads) {
        kc::Bits r{q.lo&~occupied.lo,q.hi&~occupied.hi};
        if (r.count()>=2 && kc::is_subset(r,legal)) candidates.insert(r);
    }
    std::vector<kc::Bits> minimal;
    for (auto r:candidates) {
        auto vertices=points(r);
        bool redundant=false;
        for (unsigned s=1;s+1<(1u<<vertices.size());++s) {
            if (__builtin_popcount(s)<2) continue;
            kc::Bits sub;
            for (unsigned i=0;i<vertices.size();++i) if (s&(1u<<i)) sub.set(vertices[i]);
            if (candidates.count(sub)) { redundant=true; break; }
        }
        if (!redundant) minimal.push_back(r);
    }
    return minimal;
}

static std::vector<std::vector<int>> twins(kc::Bits legal,
                                          const std::vector<kc::Bits>& edges) {
    std::map<std::vector<kc::Bits>,std::vector<int>> groups;
    for (int v:points(legal)) {
        std::vector<kc::Bits> link;
        for (auto e:edges) if (e.test(v)) { e.clear(v); link.push_back(e); }
        std::sort(link.begin(),link.end());
        groups[link].push_back(v);
    }
    std::vector<std::vector<int>> result;
    for (const auto& group:groups) result.push_back(group.second);
    return result;
}

static void array(const std::vector<int>& p) {
    std::printf("[");
    for (std::size_t i=0;i<p.size();++i) std::printf("%s%d",i?",":"",p[i]);
    std::printf("]");
}

int main(int argc,char** argv) {
    int trials=argc>1?std::stoi(argv[1]):200;
    if (trials<1 || trials>2000) throw std::invalid_argument("trials must be 1..2000");
    std::mt19937 random(20261005);
    std::printf("{\"seed\":20261005,\"trials_per_board\":%d,\"legal_limit\":18,"
                "\"n11_empty_root_outcome\":\"UNKNOWN\",\"cases\":[",trials);
    for (int n=4;n<=11;++n) {
        kc::Board board;
        kc::build_square(board,n);
        unsigned snapshots=0,reducible=0,nonisolated=0,max_removed=0;
        std::map<unsigned,unsigned> removed_hist;
        std::vector<kc::Bits> witness_edges;
        kc::Bits witness_occupied,witness_legal;
        std::vector<std::vector<int>> witness_twins;
        unsigned witness_removed=0;
        for (int trial=0;trial<trials;++trial) {
            kc::Bits occupied;
            while (true) {
                auto legal=kc::legal_mask(board,occupied);
                auto available=points(legal);
                if (available.size()<=18 && !available.empty()) {
                    auto edges=residual(board,occupied,legal);
                    auto classes=twins(legal,edges);
                    unsigned removed=0,nonisolated_removed=0;
                    for (const auto& group:classes) {
                        unsigned k=group.size(),keep=k%2?1:2;
                        if (k>keep) {
                            bool incident=false;
                            for (auto e:edges) if (e.test(group.front())) incident=true;
                            removed+=k-keep;
                            if (incident) nonisolated_removed+=k-keep;
                        }
                    }
                    ++snapshots;
                    if (removed) ++reducible;
                    if (nonisolated_removed) ++nonisolated;
                    max_removed=std::max(max_removed,removed);
                    ++removed_hist[removed];
                    // Prefer a nonisolated reduction, then larger savings.
                    unsigned score=nonisolated_removed*1000+removed;
                    if (removed && (witness_twins.empty() || score>witness_removed)) {
                        witness_removed=score;
                        witness_occupied=occupied;
                        witness_legal=legal;
                        witness_edges=edges;
                        witness_twins=classes;
                    }
                }
                if (available.empty()) break;
                occupied.set(available[random()%available.size()]);
            }
        }
        std::printf("%s{\"n\":%d,\"snapshots\":%u,\"reducible_snapshots\":%u,"
                    "\"nonisolated_reducible_snapshots\":%u,\"max_removed\":%u,"
                    "\"removed_histogram\":{",n==4?"":",",n,snapshots,reducible,
                    nonisolated,max_removed);
        bool first=true;
        for (auto row:removed_hist) { std::printf("%s\"%u\":%u",first?"":",",row.first,row.second); first=false; }
        std::printf("},\"witness\":");
        if (witness_twins.empty()) std::printf("null");
        else {
            std::printf("{\"occupied\":");array(points(witness_occupied));
            std::printf(",\"legal\":");array(points(witness_legal));
            std::printf(",\"minimal_residual_edges\":[");
            for (std::size_t i=0;i<witness_edges.size();++i) { if(i)std::printf(",");array(points(witness_edges[i])); }
            std::printf("],\"twin_classes\":[");
            for (std::size_t i=0;i<witness_twins.size();++i) { if(i)std::printf(",");array(witness_twins[i]); }
            std::printf("]}");
        }
        std::printf("}");std::fflush(stdout);
        std::fprintf(stderr,"n=%d snapshots=%u reducible=%u nonisolated=%u maxremoved=%u\n",
                     n,snapshots,reducible,nonisolated,max_removed);
    }
    std::printf("]}\n");
}

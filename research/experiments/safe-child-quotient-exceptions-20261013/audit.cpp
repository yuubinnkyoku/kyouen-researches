// Independent audit: no repository geometry/canonicalization/solver imports.
// Exhaust all parents of size 0..3, then compute legal moves, parent-stabilizer
// move orbits and complete D4 canonical-child classes directly.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Mask = __uint128_t;

struct Example {
    std::vector<int> parent;
    std::vector<int> merged_moves;
    int legal = 0;
    int children = 0;
};

struct Report {
    int n = 0;
    std::array<std::uint64_t, 4> parents{};
    std::array<std::uint64_t, 4> exceptions{};
    std::array<std::uint64_t, 4> excess{};
    std::array<std::set<Mask>, 4> canonical_exceptions;
    std::array<std::vector<Example>, 4> examples;
    std::uint64_t edges = 0;
};

class Audit {
public:
    explicit Audit(int n_) : n(n_), size(n*n), maps(8, std::vector<int>(size)),
                            bits(size), center(n%2 ? (size-1)/2 : -1) {
        if (size > 127) throw std::runtime_error("audit mask capacity exceeded");
        for (int p=0; p<size; ++p) {
            bits[p] = Mask(1) << p;
            for (int t=0; t<8; ++t) {
                int x=p%n, y=p/n;
                if (t>=4) x=n-1-x;
                for (int r=0; r<t%4; ++r) {
                    const int old_x=x;
                    x=n-1-y;
                    y=old_x;
                }
                maps[t][p]=y*n+x;
            }
        }
        report.n=n;
    }

    Report run() {
        std::vector<int> parent;
        inspect(parent);
        for (int a=0; a<size; ++a) {
            parent={a}; inspect(parent);
            for (int b=a+1; b<size; ++b) {
                parent={a,b}; inspect(parent);
                for (int c=b+1; c<size; ++c) {
                    parent={a,b,c}; inspect(parent);
                }
            }
        }
        const std::uint64_t generic_count = n%2 ? std::uint64_t(n-1)*(n-3)
                                               : std::uint64_t(n)*(n-2);
        const std::array<std::uint64_t, 4> expected{
            0, generic_count, generic_count*(1+n%2), generic_count*(n%2)};
        for (int k=0; k<4; ++k) {
            require(report.exceptions[k]==expected[k], "count formula");
            require(report.excess[k]==expected[k], "one extra merge");
            require(8*report.canonical_exceptions[k].size()==expected[k],
                    "free D4 action on exceptional parents");
        }
        return report;
    }

private:
    int n, size;
    std::vector<std::vector<int>> maps;
    std::vector<Mask> bits;
    int center;
    Report report;

    static void require(bool condition, const std::string& name) {
        if (!condition) throw std::runtime_error("failed: "+name);
    }

    bool generic(int p) const {
        const int x=2*(p%n)-(n-1), y=2*(p/n)-(n-1);
        return x!=0 && y!=0 && x!=y && x!=-y;
    }

    bool legal_four(const std::vector<int>& s, int p) const {
        // Translate the first point to the origin. The 4x4 lifted determinant
        // becomes det([dx,dy,dx^2+dy^2]) over the other three points.
        const std::int64_t ax=s[0]%n, ay=s[0]/n;
        const std::int64_t ux=s[1]%n-ax, uy=s[1]/n-ay;
        const std::int64_t vx=s[2]%n-ax, vy=s[2]/n-ay;
        const std::int64_t wx=p%n-ax, wy=p/n-ay;
        const std::int64_t uq=ux*ux+uy*uy;
        const std::int64_t vq=vx*vx+vy*vy;
        const std::int64_t wq=wx*wx+wy*wy;
        const std::int64_t determinant =
            ux*(vy*wq-vq*wy)-uy*(vx*wq-vq*wx)+uq*(vx*wy-vy*wx);
        return determinant!=0;
    }

    std::vector<int> predicted_merge(const std::vector<int>& s) const {
        std::vector<int> noncentral;
        for (int p:s) if (p!=center) noncentral.push_back(p);
        if (noncentral.empty() || noncentral.size()>2 || !generic(noncentral[0]))
            return {};
        const int a=noncentral[0];
        if (noncentral.size()==2 && noncentral[1]!=maps[1][a]
                                && noncentral[1]!=maps[3][a]) return {};
        std::vector<int> missing;
        for (int t=0; t<4; ++t) {
            const int p=maps[t][a];
            if (std::find(s.begin(), s.end(), p)==s.end()) missing.push_back(p);
        }
        if (noncentral.size()==1) {
            missing={maps[1][a], maps[3][a]};
        }
        std::sort(missing.begin(), missing.end());
        require(missing.size()==2, "predicted merge has two moves");
        return missing;
    }

    void inspect(const std::vector<int>& s) {
        const int k=static_cast<int>(s.size());
        ++report.parents[k];
        Mask parent=0;
        for (int p:s) parent|=bits[p];
        std::array<Mask, 8> images{};
        std::vector<int> stabilizer;
        for (int t=0; t<8; ++t) {
            for (int p:s) images[t]|=bits[maps[t][p]];
            if (images[t]==parent) stabilizer.push_back(t);
        }
        std::vector<std::pair<Mask, int>> children;
        std::set<int> move_orbits;
        for (int p=0; p<size; ++p) {
            if ((parent&bits[p]) || (k==3 && !legal_four(s,p))) continue;
            int representative=p;
            for (int t:stabilizer) representative=std::min(representative,maps[t][p]);
            move_orbits.insert(representative);
            Mask key=images[0]|bits[p];
            for (int t=1; t<8; ++t) key=std::min(key,images[t]|bits[maps[t][p]]);
            children.emplace_back(key,p);
        }
        report.edges+=children.size();
        std::sort(children.begin(),children.end());
        std::vector<std::vector<int>> actual_extra_groups;
        int child_classes=0;
        for (std::size_t i=0; i<children.size();) {
            std::size_t j=i+1;
            while (j<children.size() && children[j].first==children[i].first) ++j;
            ++child_classes;
            std::set<int> representatives;
            std::vector<int> moves;
            for (std::size_t z=i; z<j; ++z) {
                const int p=children[z].second;
                int rep=p;
                for (int t:stabilizer) rep=std::min(rep,maps[t][p]);
                representatives.insert(rep);
                moves.push_back(p);
            }
            if (representatives.size()>1) actual_extra_groups.push_back(moves);
            i=j;
        }
        const auto expected=predicted_merge(s);
        const bool exceptional=!expected.empty();
        require(actual_extra_groups.size()==std::size_t(exceptional),
                "necessary and sufficient classification at n="+std::to_string(n));
        const int extra=static_cast<int>(move_orbits.size())-child_classes;
        require(extra==static_cast<int>(exceptional), "exact quotient correction");
        if (exceptional) {
            require(stabilizer.size()==1, "exceptional stabilizer trivial");
            require(actual_extra_groups[0]==expected, "exact merged move pair");
            ++report.exceptions[k];
            report.excess[k]+=extra;
            report.canonical_exceptions[k].insert(*std::min_element(images.begin(),images.end()));
            if (report.examples[k].size()<2) {
                report.examples[k].push_back({s,expected,static_cast<int>(children.size()),child_classes});
            }
        }
    }
};

static void print_array(const std::array<std::uint64_t, 4>& values) {
    std::cout << '[';
    for (int i=0; i<4; ++i) std::cout << (i ? "," : "") << values[i];
    std::cout << ']';
}

static void print_points(const std::vector<int>& values) {
    std::cout << '[';
    for (std::size_t i=0; i<values.size(); ++i) std::cout << (i ? "," : "") << values[i];
    std::cout << ']';
}

int main(int argc, char** argv) {
    const int last=argc>1 ? std::stoi(argv[1]) : 11;
    if (last<1 || last>11) throw std::runtime_error("last n must be in 1..11");
    std::cout << "{\"schema\":\"safe-child-quotient-exception-audit-v1\","
                 "\"method\":\"independent integer lifted determinant and raw eight-element D4 maps\","
                 "\"coverage\":\"every subset with size 0..3\",\"boards\":[\n";
    for (int n=1; n<=last; ++n) {
        const auto report=Audit(n).run();
        std::cout << (n>1 ? ",\n" : "") << "{\"n\":" << n << ",\"parents_by_size\":";
        print_array(report.parents);
        std::cout << ",\"exceptional_parents_by_size\":";
        print_array(report.exceptions);
        std::cout << ",\"total_extra_merges_by_size\":";
        print_array(report.excess);
        std::array<std::uint64_t, 4> classes{};
        for (int k=0; k<4; ++k) classes[k]=report.canonical_exceptions[k].size();
        std::cout << ",\"exceptional_parent_d4_classes_by_size\":";
        print_array(classes);
        std::cout << ",\"legal_edges\":" << report.edges << ",\"classification_mismatches\":0,\"examples\":[";
        bool first=true;
        for (const auto& bucket:report.examples) for (const auto& example:bucket) {
            std::cout << (first ? "" : ",") << "{\"parent\":";
            first=false;
            print_points(example.parent);
            std::cout << ",\"merged_moves\":";
            print_points(example.merged_moves);
            std::cout << ",\"legal\":" << example.legal
                      << ",\"canonical_children\":" << example.children << '}';
        }
        std::cout << "]}";
        std::cerr << "n=" << n << " classification and pair-level checks passed\n";
    }
    std::cout << "\n]}\n";
}

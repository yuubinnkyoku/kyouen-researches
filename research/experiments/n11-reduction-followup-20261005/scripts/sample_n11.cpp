// Reuse the previously audited residual/point/array functions directly.
// Renaming its entry point does not execute its earlier experiment.
#pragma GCC diagnostic push
// Its renamed, unused entry point lacks the implicit return supplied to main.
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main twins_reference_main
#include "../../n11-residual-twins/scripts/sample_residual_twins.cpp"
#undef main
#pragma GCC diagnostic pop

int main(int argc, char** argv) {
    int trials=argc>1?std::stoi(argv[1]):200;
    if (trials<1 || trials>2000) throw std::invalid_argument("trials must be 1..2000");
    kc::Board board;
    kc::build_square(board,11);
    std::mt19937 random(20261005);
    std::printf("{\"n\":11,\"seed\":20261005,\"trials\":%d,\"legal_limit\":18,"
                "\"n11_empty_root_outcome\":\"UNKNOWN\",\"snapshots\":[",trials);
    unsigned snapshots=0;
    for (int trial=0;trial<trials;++trial) {
        kc::Bits occupied;
        while (true) {
            auto legal=kc::legal_mask(board,occupied);
            auto available=points(legal);
            if (!available.empty() && available.size()<=18) {
                auto edges=residual(board,occupied,legal);
                std::printf("%s{\"trial\":%d,\"occupied\":",snapshots?",":"",trial);
                array(points(occupied));
                std::printf(",\"legal\":");array(available);
                std::printf(",\"minimal_residual_edges\":[");
                for (std::size_t i=0;i<edges.size();++i) {
                    if (i) std::printf(",");
                    array(points(edges[i]));
                }
                std::printf("]}");
                ++snapshots;
            }
            if (available.empty()) break;
            occupied.set(available[random()%available.size()]);
        }
    }
    std::printf("]}\n");
    std::fprintf(stderr,"n11 snapshots=%u\n",snapshots);
}

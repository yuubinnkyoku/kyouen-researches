// Reuse the independent board/residual generator, not the df-pn evaluator.
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main sampler_reference_main
#include "../n11-residual-twins/scripts/sample_residual_twins.cpp"
#undef main
#pragma GCC diagnostic pop
int main(){
    constexpr int trials=512;
    constexpr unsigned seed=2026102107;
    kc::Board board;kc::build_square(board,11);
    std::mt19937 random(seed);
    std::printf("{\"n\":11,\"seed\":%u,\"trials\":%d,\"snapshots\":[",seed,trials);
    unsigned count=0;
    for(int trial=0;trial<trials;++trial){
        kc::Bits occupied;
        for(;;){
            auto legal=kc::legal_mask(board,occupied);
            auto available=points(legal);
            if(available.size()>=6 && available.size()<=18){
                auto edges=residual(board,occupied,legal);
                std::printf("%s{\"trial\":%d,\"occupied\":",count?",":"",trial);array(points(occupied));
                std::printf(",\"legal\":");array(available);std::printf(",\"minimal_residual_edges\":[");
                for(std::size_t i=0;i<edges.size();++i){if(i)std::printf(",");array(points(edges[i]));}
                std::printf("]}");++count;
            }
            if(available.empty())break;
            occupied.set(available[random()%available.size()]);
        }
    }
    std::printf("]}\n");
}

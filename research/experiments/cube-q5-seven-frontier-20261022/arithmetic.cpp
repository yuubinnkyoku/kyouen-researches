// Independent std::bitset comparison for the checker's six-word arithmetic.
#define main q5_verifier_main
#include "verify.cpp"
#undef main
#include <bitset>
#include <random>
int main() {
    std::mt19937_64 rng(20261022);
    uint64_t checks=0;
    for(int sample=0;sample<16;sample++) {
        U value;std::bitset<384> reference;
        for(int j=0;j<6;j++) {
            value.words[j]=rng();
            for(int k=0;k<64;k++)reference[j*64+k]=(value.words[j]>>k)&1;
        }
        auto equal=[&](const U& result,const std::bitset<384>& expected) {
            for(int j=0;j<384;j++)if(bool((result.words[j/64]>>(j%64))&1)!=expected[j])throw std::runtime_error("word arithmetic mismatch");
            ++checks;
        };
        for(int shift=0;shift<=384;shift++){equal(value<<shift,reference<<shift);equal(value>>shift,reference>>shift);}
        auto minus=reference;
        for(int j=0;j<384;j++){bool old=minus[j];minus.flip(j);if(old)break;}
        equal(value-1,minus);equal(~value,~reference);
    }
    U all=(U(1)<<343)-1;
    if(count(all)!=343 || elements(all).back()!=342)throw std::runtime_error("board mask mismatch");
    std::cout<<"{\"six_word_arithmetic_cases\":"<<checks<<"}\n";
}

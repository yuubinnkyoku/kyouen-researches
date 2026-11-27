// Active cache-only exclusions from results/n11-s5-evidence-quarantine.json.
// Registry synchronization is checked by the independent audit regression.
// Rehabilitation requires changing the registry AND this compiled policy.
#pragma once
#include <array>
#include <cstdint>
#include <utility>
inline constexpr std::array<std::pair<std::uint64_t,std::uint64_t>,2>
n11_s5_quarantined_keys{{
    {1152925911243358208ULL,536870912ULL},
    {10448351135499552768ULL,128ULL},
}};

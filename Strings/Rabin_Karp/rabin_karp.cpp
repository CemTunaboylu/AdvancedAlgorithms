// This implemented in C++ because the hashing part can overflow, thus I care about handling that explicitly.

#include <iostream>
#include <type_traits>

// https://stackoverflow.com/questions/874298/c-templates-that-accept-only-certain-types
// https://stackoverflow.com/questions/1505675/power-of-an-integer-in-c


using namespace std;

#define BASE int base = 128;
#define RET_TYPE int
// We may define a mod

void set_base(int num_symbols, int pattern_length){
        // calculating the upper bounds of the Rabin Fingerprint Function
        if (num_symbols == 26){

        }else{
                #ifdef BASE
                #undef BASE
                #define BASE int base=15;
                #endif
        }
}

template <typename base>
struct fast_power {
        RET_TYPE int_power(const int x){
        if constexpr (x == 0) return 1;
        if constexpr (x == 1) return base;

        int tmp = int_power<base>(x/2);
        if constexpr ((x % 2) == 0) { return tmp * tmp; }
        else { return base * tmp * tmp; }
        }
};


RET_TYPE rabin_fingerprint(const string& str){
        for(char c: str){
                unsigned int p = int(c);
                fast_power<unsigned int>(base);
        }
        return 1;
} 


int main(){
        set_base(-1,5);
        BASE 
        cout << base <<endl;

        rabin_fingerprint("abc");

        return 0;
}
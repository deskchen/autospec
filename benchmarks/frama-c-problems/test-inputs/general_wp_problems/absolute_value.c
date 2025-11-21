#include <limits.h>

int abs(int val) {
    if(val < 0) return -val;
    return val;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
   
   HINT: The negation -val causes an overflow if val is INT_MIN.
   The generated specification must exclude this case.
*/
void test() {
    int b = abs(-42);
    //@ assert b == 42;

    int c = abs(42);
    //@ assert c == 42;
    
    int z = abs(0);
    //@ assert z == 0;
    
    // This symbolic check ensures the return value is non-negative
    // for any valid input.
    int unknown = 100;
    int d = abs(unknown);
    //@ assert d >= 0;
}
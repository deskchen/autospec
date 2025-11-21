#include <stdio.h>

int func(int c) {
    int x = c;
    int y = 0;

    while(x > 0) {
        x = x - 1;
        y = y + 1;
    }
    return y;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    // Case 1: Large positive number
    int r1 = func(100);
    //@ assert r1 == 100;

    // Case 2: Smallest allowed positive number (c > 0)
    int r2 = func(1);
    //@ assert r2 == 1;
    
    // Case 3: Arbitrary positive number
    int r3 = func(42);
    //@ assert r3 == 42;
}
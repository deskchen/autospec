#include <limits.h>

/*@
    requires a >= 0 && b >= 0;
    // FIX 1: Prevent overflow
    requires (integer)a * b <= INT_MAX;
    
    ensures \result == a * b;
    assigns \nothing;
*/
int mul(int a, int b) {
    int x = a;
    int y = b; 
    int prod = 0;
    
    /*@ 
        loop invariant 0 <= x <= a; // Helps prove x stays in bounds
        loop invariant prod == (a - x) * y;
        loop assigns prod, x;
        
        // FIX 2: Prove the loop terminates (x decreases to 0)
        loop variant x;
    */
    while(x > 0) { // FIX 3: Stop when x hits 0 (don't include 0)
        prod = prod + y;
        x--;
    }
    return prod;
}

int main() {
    int pdt = mul(2, 5);
    //@ assert pdt == 10;
}
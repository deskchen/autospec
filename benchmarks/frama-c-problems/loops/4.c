#include <stdio.h>

/*@
    requires n >= 0;
    requires n < 31; // Prevent 32-bit integer overflow (2^31)
    
    // Use bit-shift logic for powers of 2: (1 << k) is 2^k
    ensures \result == (1 << (n+1)) - 1;
    
    assigns \nothing;
*/
int fun(int n) {
    int y = 0;
    int i = 0;

    /*@
        // FIX 1: Allow i to reach n + 1 (exit state)
        loop invariant 0 <= i <= n + 1;
        
        // FIX 2: Match the code's logic (sum of geometric series)
        loop invariant y == (1 << i) - 1;
        
        loop assigns i, y;
        
        // FIX 3: Prove termination
        loop variant n - i;
    */
    while(i <= n) {
        // 1 << i is equivalent to pow(2, i) but exact for integers
        y = y + (1 << i);
        i = i + 1;
    }
    return y;
}

int main() {
    int res = fun(4);
    // FIX 4: Correct mathematical answer for n=4 is 31
    //@ assert res == 31;
    
    int res2 = fun(2);
    //@ assert res2 == 7; // This is 7
}
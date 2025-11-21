#include <limits.h>

/*@
    requires n > 0 && x > 0;
    // FIX 1: Prevent Integer Overflow (sum must fit in int)
    requires (integer)n * x <= INT_MAX;
    
    // FIX 2: Declare 'sum' as a valid pointer we can write to
    requires \valid(sum);
    requires \valid_read(a + (0..n-1));

    // FIX 3: Declare what the function modifies
    assigns *sum;

    ensures \result >= 0 && \result <= n;
    ensures *sum == \result * x;
*/
int func(int *a, int n, int x, int *sum) {
    int p = 0;
    int count = 0;
    *sum = 0;

    /*@
        loop invariant 0 <= p <= n;
        loop invariant 0 <= count <= p; // Helpful bounds hint
        loop invariant *sum == count * x;
        
        loop assigns p, count, *sum;
        
        // FIX 4: Prove termination
        loop variant n - p;
    */
    while (p < n) {
        if (a[p] == x) {
            count = count + 1;
            *sum = *sum + x;
        }
        p = p + 1;
    }

    Label_a:
    *sum += 0;
    
    //@ assert \at(*sum, Label_a) == count*x;
    return count;
}
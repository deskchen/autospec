/*@
    requires n >= 0;
    requires n % 2 == 0;       // FIX 1: The formula is only valid for even n
    
    // FIX 2: Use integer arithmetic instead of '0.25'
    ensures \result == n * (n + 2) / 4;
    
    assigns \nothing;
*/
int func(int n) {
    int sum = 0;
    int i = 0;
    /*@
        // FIX 3: Bound i (it goes 1 step past the limit n/2)
        loop invariant 0 <= i <= n/2 + 1;
        
        loop invariant sum == i * (i - 1);
        loop assigns sum, i;
        
        // FIX 4: Prove termination
        loop variant n/2 - i;
    */
    while(i <= n/2) {
        sum = sum + 2*(i);
        i++;
    }
    return sum;
}
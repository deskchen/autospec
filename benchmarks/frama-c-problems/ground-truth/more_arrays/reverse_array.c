/*@
    requires n > 0;
    // FIX 1: Must be writable (\valid), not just readable
    requires \valid(a + (0..n-1));

    assigns a[0..n-1];

    // FIX 2: Correct Postcondition for Reverse
    // "The element at k is equal to the OLD element at n-1-k"
    ensures \forall integer k; 0 <= k < n ==> a[k] == \at(a[n-1-k], Pre);
*/
void reverse(int *a, int n) {
    int i = 0;
    int j = n-1;
    
    /*@
        loop invariant 0 <= i <= n/2;
        
        // FIX 3: Link j to i
        loop invariant j == n - 1 - i;

        // FIX 4: Describe the partial state of the array
        // A. The bottom part (0..i) has been swapped
        loop invariant \forall integer k; 0 <= k < i ==> a[k] == \at(a[n-1-k], Pre);

        // B. The top part (j+1..n) has been swapped
        loop invariant \forall integer k; j < k < n ==> a[k] == \at(a[n-1-k], Pre);

        // C. The middle part (i..j) is untouched (same as Pre)
        loop invariant \forall integer k; i <= k <= j ==> a[k] == \at(a[k], Pre);

        loop assigns i, j, a[0..n-1];
        loop variant j - i;
    */
    while (i < n/2) {
        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
        i++;
        j--;
    }
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int a[] = {1, 2, 3, 4, 5};
    reverse(a, 5);
    //@ assert a[0] == 5 && a[1] == 4 && a[2] == 3 && a[3] == 2 && a[4] == 1;
}
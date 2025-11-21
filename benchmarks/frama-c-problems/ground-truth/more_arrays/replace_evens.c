/*@
    requires n > 0;
    requires \valid_read(a + (0..n-1));
    ensures  \forall integer k; (0<=k<n) && (k%2==0) ==> (a[k] == 0);
*/
void func(int *a, int n) {
    /*@
        loop invariant 0 <= i <= n;
        loop invariant \forall integer k;  (0 <= k < i) && (k%2==0) ==> a[k] == 0;
        loop invariant \forall integer k;  (0 <= k < i) && (k%2==1) ==> a[k] == a[k];
        loop assigns i, a[0..(n-1)];
    */
    for (int i = 0; i < n; i++) {
        if (i%2==0) 
            a[i] = 0;
    }
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int a[] = {1, 2, 3, 4, 5};
    func(a, 5);
    //@ assert \forall integer k; (0<=k<5) && (k%2==0) ==> (a[k] == 0);
}
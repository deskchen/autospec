void func(int *a, int n) {

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
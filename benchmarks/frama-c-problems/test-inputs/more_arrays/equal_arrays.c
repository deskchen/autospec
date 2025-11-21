int check(int *a, int *b, int n) {

    for (int i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            return 0;
        }
    }
    return 1;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int a[] = {1,2,3,4,5};
    int b[] = {1,2,3,4,5};
    int result = check(a, b, 5);
    //@ assert result == 1;
}
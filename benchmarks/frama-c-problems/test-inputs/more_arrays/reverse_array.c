void reverse(int *a, int n) {
    int i = 0;
    int j = n-1;
    
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
// Program to swap 2 elements of an array at the givem indices n1, n2

/*@
    requires n >= 0;
    requires 0 <= n1 < n && 0 <= n2 < n;
    requires \valid_read(arr+(0..n-1));
    ensures (arr[n2] == \old(arr[n1])) && (arr[n1] == \old(arr[n2]));
*/
void array_swap(int* arr, int n, int n1, int n2) {
    int temp = arr[n1];
    arr[n1] = arr[n2];
    arr[n2] = temp;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int arr[] = {1, 2, 3, 4, 5};
    array_swap(arr, 5, 1, 2);
    //@ assert arr[1] == 3 && arr[2] == 2;
}
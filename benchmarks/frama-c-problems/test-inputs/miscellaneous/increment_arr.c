void increment_array_by(int* arr, int n, int c) {

    for (int  i = 0; i < n; i++) {
        arr[i] = arr[i] + c;
    }
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int arr[] = {1, 2, 3, 4, 5};
    increment_array_by(arr, 5, 1);
    //@ assert arr[0] == 2 && arr[1] == 3 && arr[2] == 4 && arr[3] == 5 && arr[4] == 6;
}
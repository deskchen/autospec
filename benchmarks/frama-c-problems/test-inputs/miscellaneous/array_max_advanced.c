int array_max_advanced(int* arr, int n) {
    int max = arr[0];
    
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int arr[] = {1, 2, 3, 4, 5};
    int max = array_max_advanced(arr, 5);
    //@ assert max == 5;
}
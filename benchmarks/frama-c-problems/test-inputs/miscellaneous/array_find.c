// Program to find index of an element in an array
// Behaviors not used in this program

int array_find(int* arr, int n, int x) {
    int i = 0;

    for (i = 0; i < n; i++) {
        if (arr[i] == x) {
            return i;
        }
    }
    return -1;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int arr[] = {1, 2, 3, 4, 5};
    int index = array_find(arr, 5, 3);
    //@ assert index == 2;
}
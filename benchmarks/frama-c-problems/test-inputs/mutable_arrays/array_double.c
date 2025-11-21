void arrayDouble(int *a, int n) {
    int p = 0;

    while (p < n) {
        a[p] = a[p] * 2;
        p = p + 1;
    } 
}

int main() {
    int arr[] = {0,1,2,3,4,5};
    arrayDouble(arr, 6);
    //@ assert \forall integer k; 0 <= k < 6 ==> arr[k] == 2*k;
}
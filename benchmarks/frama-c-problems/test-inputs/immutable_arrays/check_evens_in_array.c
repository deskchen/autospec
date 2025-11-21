
int areElementsEven(int *a, int n) {
    int p = 0;

    while (p < n) {
        if (a[p]%2 != 0) {
            return 0;
        }
        p = p + 1;
    }
    return 1;
}

void main() {
    int arr[] = {2,4,6,8,10};
    int res = areElementsEven(arr, 5);
    //@ assert res == 1;
}
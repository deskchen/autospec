int binarysearch(int* a, int x, int n) {
    int low = -1;
    int high = n;
    int p;

    while (low+1 < high) {
        p = (low + high) / 2;
        if (a[p] == x) 
            return p;
        else 
            if (a[p] < x)
            low = p;
            else high = p;
    }
    return -1;
}

void test_present() {
    int arr[3] = {10, 20, 30};

    int idx = binarysearch(arr, 20, 3);
    //@ assert arr[idx] == 20;
}

void test_not_present() {
    int arr[3] = {10, 20, 30};
    int idx = binarysearch(arr, 25, 3);
    
    //@ assert idx == -1;
}
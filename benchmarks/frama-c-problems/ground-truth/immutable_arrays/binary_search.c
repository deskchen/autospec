/*@
    requires n > 0;
    requires \valid_read(a+(0..n-1));
    requires \forall integer k, l; 0 <= k <= l < n ==> a[k] <= a[l];
    
    assigns \nothing;

    ensures \result >= -1 && \result < n;

    behavior present:
        assumes \exists integer k ; 0 <= k < n && a[k] == x ;
        ensures a[\result] == x ;

    behavior not_present:
        assumes \forall integer k ; 0 <= k < n ==> a[k] != x ;
        ensures \result == -1;

    disjoint behaviors;
    complete behaviors;
*/
int binarysearch(int* a, int x, int n) {
    int low = -1;
    int high = n;
    int p;

    /*@
        loop invariant -1 <= low < high <= n;
        
        // FIX: Stronger "Exclusion" Invariants
        // These are much easier for Z3/Alt-Ergo to prove than the implicit one.
        // 1. Everything to the left of 'low' is strictly smaller than x
        loop invariant \forall integer k; 0 <= k <= low ==> a[k] < x;
        
        // 2. Everything to the right of 'high' is strictly larger than x
        loop invariant \forall integer k; high <= k < n ==> a[k] > x;
        
        loop assigns low, high, p;
        loop variant high - low; 
    */
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
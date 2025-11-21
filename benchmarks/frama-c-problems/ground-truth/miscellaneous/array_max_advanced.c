/*@
    requires n > 0;
    requires \valid_read(arr+(0..n-1));
    
    assigns \nothing;

    // FIX 1: Replace '\max' with the standard logical definition
    // Condition A: Result is >= all elements
    ensures \forall integer k; 0 <= k < n ==> arr[k] <= \result;
    
    // Condition B: Result actually exists in the array
    ensures \exists integer k; 0 <= k < n && arr[k] == \result;
*/
int array_max_advanced(int* arr, int n) {
    int max = arr[0];
    
    // FIX 2: Start at 1. Since max is arr[0], we don't need to check index 0.
    // This makes the initial invariant "0 <= k < 1" valid immediately.
    /*@
        loop invariant 1 <= i <= n;
        
        // Invariant A: max is >= everything we've seen so far
        loop invariant \forall integer k; 0 <= k < i ==> arr[k] <= max;
        
        // Invariant B: max is an element we have seen
        loop invariant \exists integer k; 0 <= k < i && arr[k] == max;
        
        loop assigns max, i;
        loop variant n - i;
    */
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
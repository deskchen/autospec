/*@
    requires n > 0;
    // FIX 1: This is a Precondition (requires), not a Postcondition (ensures)
    requires \valid_read(a + (0..n-1));
    assigns \nothing;

    behavior present:
        assumes \exists integer k; 0 <= k < n && x == a[k];
        ensures \result == 1;

    behavior not_present:
        // FIX 2: Use \forall. "ALL elements are NOT x"
        // The original \exists meant "At least one element is not x" (which overlaps with present)
        assumes  \forall integer k; 0 <= k < n ==> x != a[k];
        ensures \result == 0;

    disjoint behaviors;
    complete behaviors;
*/
int arraySearch(int *a, int x, int n) {
    int p = 0;
    /*@
        loop invariant  0 <= p <= n;
        loop invariant \forall integer k; 0 <= k < p ==> x != a[k];
        loop assigns p;
        // FIX 3: Prove termination
        loop variant n - p;
    */
    while (p < n) {
        if (a[p] == x) {
            return 1;
        }
        p++;
    }
    return 0;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int arr[] = {10, 20, 30, 40, 50};

    // Case 1: Element is Present (Search for 30)
    int found = arraySearch(arr, 30, 5);
    //@ assert found == 1;

    // Case 2: Element is Not Present (Search for 99)
    int not_found = arraySearch(arr, 99, 5);
    //@ assert not_found == 0;
}
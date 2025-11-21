
int func(int n) {
    int sum = 0;
    int i = 0;

    while(i <= n/2) {
        sum = sum + 2*(i);
        i++;
    }
    return sum;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    // Case 1: Base Case (n=0)
    // Loop runs for i=0. sum = 0.
    // Formula: 0 * 2 / 4 = 0
    int s1 = func(0);
    //@ assert s1 == 0;

    // Case 2: Small even number (n=2)
    // Loop runs for i=0, 1. sum = 0 + 2 = 2.
    // Formula: 2 * 4 / 4 = 2.
    int s2 = func(2);
    //@ assert s2 == 2;

    // Case 3: Larger even number (n=10)
    // Sum of 0, 2, 4, 6, 8, 10 = 30
    // Formula: 10 * 12 / 4 = 120 / 4 = 30.
    int s3 = func(10);
    //@ assert s3 == 30;
    
    // Case 4: Ensure result is non-negative
    int s4 = func(100);
    //@ assert s4 >= 0;
}
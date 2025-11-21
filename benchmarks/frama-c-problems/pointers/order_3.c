/*@
    requires \valid(a) && \valid(b) && \valid(c);
    requires \separated(a, b, c);
    assigns *a, *b, *c;

    // 1. Sorted
    ensures *a <= *b <= *c;

    // 2. Sum Preserved
    ensures *a + *b + *c == \old(*a) + \old(*b) + \old(*c);

    // 3. Extremes (The Fix)
    // *a is the minimum, so it must be <= all inputs
    ensures *a <= \old(*a) && *a <= \old(*b) && *a <= \old(*c);
    // *c is the maximum, so it must be >= all inputs
    ensures *c >= \old(*a) && *c >= \old(*b) && *c >= \old(*c);

    // 4. Membership (Still good to have)
    ensures *a == \old(*a) || *a == \old(*b) || *a == \old(*c);
    ensures *b == \old(*a) || *b == \old(*b) || *b == \old(*c);
    ensures *c == \old(*a) || *c == \old(*b) || *c == \old(*c);
*/
void order_3(int *a, int *b, int *c) {
    if (*a > *b) {
        int temp = *a;
        *a = *b;
        *b = temp;
    }
    if (*a > *c) {
        int temp = *a;
        *a = *c;
        *c = temp;
    }
    if (*b > *c) {
        int temp = *b;
        *b = *c;
        *c = temp;
    }
}

void test(){
    int a1 = 5, b1 = 3, c1 = 4;
    order_3(&a1, &b1, &c1);
    //@ assert a1 == 3 && b1 == 4 && c1 == 5;

    int a2 = 2, b2 = 2, c2 = 2;
    order_3(&a2, &b2, &c2);
    //@ assert a2 == 2 && b2 == 2 && c2 == 2;

    int a3 = 4, b3 = 3, c3 = 4;
    order_3(&a3, &b3, &c3);
    //@ assert a3 == 3 && b3 == 4 && c3 == 4;

    int a4 = 4, b4 = 5, c4 = 4;
    order_3(&a4, &b4, &c4);
    //@ assert a4 == 4 && b4 == 4 && c4 == 5;
}
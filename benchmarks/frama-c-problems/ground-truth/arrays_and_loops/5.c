/*@
    requires x >= y && x > 0 && y > 0;
    ensures *r < y;
    ensures x == \result*y + *r;
    
*/
int fun(int x, int y , int *r) {
    *r = x;
    int d = 0;
    /*@
        loop invariant  *r == x - y*d;
        loop assigns *r, d;
    */
    while (*r >= y) {
        *r = *r - y;
        d = d + 1;
    }
    return d;
}

void test() {
    int r1;
    int q1 = fun(10, 3, &r1);
    // Spec only guarantees: 10 == q1*3 + r1  AND  r1 < 3
    // It does NOT guarantee r1 >= 0, so we cannot prove q1 == 3.
    //@ assert 10 == q1 * 3 + r1;
    //@ assert r1 < 3;

    int r2;
    int q2 = fun(12, 4, &r2);
    // Spec only guarantees: 12 == q2*4 + r2  AND  r2 < 4
    //@ assert 12 == q2 * 4 + r2;
    //@ assert r2 < 4;
    
}
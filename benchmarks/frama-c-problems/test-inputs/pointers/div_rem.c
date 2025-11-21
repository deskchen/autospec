void div_rem(unsigned x, unsigned y, unsigned* q, unsigned* r) {
    *q = x / y;
    *r = x % y;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    unsigned x = 10;
    unsigned y = 3;
    unsigned q = 0;
    unsigned r = 0;
    div_rem(x, y, &q, &r);
    //@ assert x == q * y + r;
    //@ assert r < y;
    //@ assert q == 3;
    //@ assert r == 1;
}
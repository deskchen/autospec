int incr_a_by_b(int* a, int const* b){
    *a += *b;
    return *a;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int a = 1;
    int b = 2;
    int result = incr_a_by_b(&a, &b);
    //@ assert a == 3;
    //@ assert b == 2;
}
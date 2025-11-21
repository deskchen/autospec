int max(int x, int y) {
    if (x >= y) {
        return x;
    }
    return y;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int x = 1;
    int y = 2;
    int max_value = max(x, y);
    //@ assert max_value == 2;
}
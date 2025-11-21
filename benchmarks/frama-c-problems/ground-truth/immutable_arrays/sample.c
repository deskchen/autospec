int fun(int x, int y) {
    int r = x;
    int d = 0;
    /*@
        loop invariant r + d*y == x;
    */
    while (r >= y) {
        printf("r = %d   d = %d   y = %d   x = %d\n", r, d, y, x);
        // Beginning
        r = r - y;
        d = d + 1;
        // ENd
        
    }
    //@ assert r < y;
    //@ assert x == d*y + r;
    return d;
}
#include <limits.h>
/*@
    requires x+y <= INT_MAX;
    requires x >= INT_MIN &&  y >= INT_MIN;
    ensures \result == x+y;
*/
int add(int x, int y) {
    return x+y;
}

void test() {
    int a = add(1, 43);
    //@ assert a == 44;
    int b = add(50, 100);
    //@ assert b == 150;
}
#include <stdio.h>
/*@
    requires n >= 4;
    ensures \result == (n - 4) / 3 + 1; // FIX: Use integer arithmetic
    assigns \nothing;
*/
int fun(int n) {
    int i = 7;
    int x = 1;
    /*@
        loop invariant i == 4 + 3*x;
        loop assigns x, i;
        loop invariant i <= n + 3;
    */
    while(i <= n) {
        x += 1;
        i += 3;
    }
    return x;
}

int main() {
    int a = fun(20);
    //@ assert a == 6;
    int b = fun(10);
    //@ assert b == 3;
    int c = fun(7);
    //@ assert c == 2;
    int d = fun(4);
    //@ assert d == 1;
}
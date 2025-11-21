#include <limits.h>
int add(int *p, int *q) {
    return *p + *q;
}

int main() {
    int a = 24;
    int b = 32;
    int x;

    x = add(&a, &b);
    //@ assert x == a + b;
    //@ assert x == 56;

    // Now this works because we allowed aliasing
    x = add(&a, &a);
    //@ assert x == a + a;
    //@ assert x == 48;
}
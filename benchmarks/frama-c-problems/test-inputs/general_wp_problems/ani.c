#include <stdio.h>

int fun(int n) {
    int i = 7;
    int x = 1;

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
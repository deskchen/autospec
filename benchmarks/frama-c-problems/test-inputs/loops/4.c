#include <stdio.h>

int fun(int n) {
    int y = 0;
    int i = 0;

    while(i <= n) {
        // 1 << i is equivalent to pow(2, i) but exact for integers
        y = y + (1 << i);
        i = i + 1;
    }
    return y;
}

int main() {
    int res = fun(4);
    // FIX 4: Correct mathematical answer for n=4 is 31
    //@ assert res == 31;
    
    int res2 = fun(2);
    //@ assert res2 == 7; // This is 7
}
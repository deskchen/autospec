#include <limits.h>

int mul(int a, int b) {
    int x = a;
    int y = b; 
    int prod = 0;
    

    while(x > 0) {
        prod = prod + y;
        x--;
    }
    return prod;
}

int main() {
    int pdt = mul(2, 5);
    //@ assert pdt == 10;
}
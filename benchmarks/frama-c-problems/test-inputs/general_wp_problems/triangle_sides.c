#include <stdio.h>

int validts(int a, int b, int c) {
    int valid = 0;
    if ((a+b>c) && (a+c>b) && (b+c>a)) {
        valid = 1;
    } else {
        valid = 0;
    }
    return valid;
}

void test() {
    int valid = validts(2, 3, 4);
    /*@ assert valid == 1; */ // 2,3,4 is a valid triangle
    
    int invalid = validts(1, 1, 10);
    /*@ assert invalid == 0; */ // 1,1,10 is NOT a valid triangle
}





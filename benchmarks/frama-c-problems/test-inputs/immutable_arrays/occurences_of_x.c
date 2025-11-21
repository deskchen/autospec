#include <limits.h>

int func(int *a, int n, int x, int *sum) {
    int p = 0;
    int count = 0;
    *sum = 0;

    while (p < n) {
        if (a[p] == x) {
            count = count + 1;
            *sum = *sum + x;
        }
        p = p + 1;
    }

    Label_a:
    *sum += 0;
    
    //@ assert \at(*sum, Label_a) == count*x;
    return count;
}
/* Compute absolute value with overflow checking */
#include <limits.h>

/*@
  @ requires x > INT_MIN;
  @ assigns \nothing;
  @ ensures \result >= 0;
  @ ensures (x >= 0 ==> \result == x);
  @ ensures (x < 0 ==> \result == -x);
  @*/
int abs_value(int x) {
    if (x < 0) {
        return -x;
    } else {
        return x;
    }
}

/*@
  @ requires \valid(a) && \valid(b);
  @ requires \separated(a, b);
  @ requires *a > INT_MIN;
  @ assigns *a, *b;
  @ ensures *a >= 0;
  @ ensures *b == \old(*a);
  @*/
void abs_in_place(int *a, int *b) {
    *b = *a;
    if (*a < 0) {
        *a = -(*a);
    }
}


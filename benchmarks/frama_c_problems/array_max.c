/* Find the maximum value in an array */
#include <limits.h>

/*@
  @ requires n > 0;
  @ requires \valid_read(arr + (0..n-1));
  @ ensures \result >= arr[0];
  @ ensures \exists integer i; 0 <= i < n && \result == arr[i];
  @ ensures \forall integer i; 0 <= i < n ==> \result >= arr[i];
  @*/
int array_max(int *arr, int n) {
    int max = arr[0];
    
    /*@
      @ loop invariant 1 <= i <= n;
      @ loop invariant \forall integer j; 0 <= j < i ==> max >= arr[j];
      @ loop invariant \exists integer k; 0 <= k < i && max == arr[k];
      @ loop assigns i, max;
      @ loop variant n - i;
      @*/
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    
    return max;
}


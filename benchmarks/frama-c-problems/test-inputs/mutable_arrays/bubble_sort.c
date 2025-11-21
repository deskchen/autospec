#include <stdio.h>
void bubbleSort(int *a, int n) {
    int i, j, temp;
      for(i=n-1; i>0; i--) {
        for(j=0; j<i; j++) {
            if (a[j] > a[j+1]) {
                    temp = a[j];
                    a[j] = a[j+1];
                    a[j+1] = temp;
            }
        }
    }
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int a[] = {5, 4, 3, 2, 1};
    bubbleSort(a, 5);
    //@ assert \forall integer i,j; 0<=i<=j<=4 ==> a[i]<=a[j];
}
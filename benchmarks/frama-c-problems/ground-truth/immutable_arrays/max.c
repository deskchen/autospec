/*@ 
    requires \valid_read(a + (0..n-1));
    requires n > 0;

    ensures \forall integer k;  0 <= k < n ==> \result >=  a[k];
    ensures \exists integer k;  0 <= k < n && \result == a[k];

    assigns \nothing;
*/
int arraymax(int* a, int n) {
  int i = 1;
  int max = a[0];

  /*@ 
     loop invariant \forall integer k;  0 <= k < i ==> max >=  a[k];
     loop invariant \exists integer k;  0 <= k < i &&  max == a[k];
     loop invariant 0 <= i <= n;
     loop assigns i,max;
 */
  while (i < n) {
    // Beginning of loop
    if (max < a[i])
    max = a[i];
    i = i + 1;
    // End of loop: Loop invariant comes here
  }
  return max;
}  

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
  // Case 1: Ascending order
  int a1[] = {1, 2, 3, 4, 5};
  int max1 = arraymax(a1, 5);
  //@ assert max1 == 5;

  // Case 2: Descending order
  int a2[] = {5, 4, 3, 2, 1};
  int max2 = arraymax(a2, 5);
  //@ assert max2 == 5;

  // Case 3: Max in the middle
  int a3[] = {10, 50, 20};
  int max3 = arraymax(a3, 3);
  //@ assert max3 == 50;

  // Case 4: Negative numbers
  int a4[] = {-5, -10, -1};
  int max4 = arraymax(a4, 3);
  //@ assert max4 == -1;
  
  // Case 5: Single element
  int a5[] = {42};
  int max5 = arraymax(a5, 1);
  //@ assert max5 == 42;
}
/*@
    logic integer sumArr(int *a, integer n) = 
        (n <= 0) ? 0 : sumArr(a, n-1) + a[n-1];
*/

/*@
    requires n > 0;
    requires \valid_read(a + (0..n-1));
    assigns \nothing;
    ensures \result == sumArr(a, n);
*/
int sumArray(int *a, int n) {
  int p = 0, sum = 0;
  /*@
      loop invariant 0 <= p <= n;
      loop invariant sum == sumArr(a, p);
      loop assigns p, sum;
      loop variant n - p;
  */
  while (p < n) {
      sum = sum + a[p];
      p++;
  }
  return sum;
}

/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
  // Case 1: Sum of {1, 2, 3}
  int a1[] = {1, 2, 3};
  int s1 = sumArray(a1, 3);
  // Logic: 3 + 2 + 1 + 0 = 6
  //@ assert s1 == 6;

  // Case 2: Sum of {10}
  int a2[] = {10};
  int s2 = sumArray(a2, 1);
  //@ assert s2 == 10;

  // Case 3: Sum of {-5, 5}
  int a3[] = {-5, 5};
  int s3 = sumArray(a3, 2);
  //@ assert s3 == 0;
}
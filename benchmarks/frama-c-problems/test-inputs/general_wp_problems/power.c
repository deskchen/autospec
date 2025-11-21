/*@
    // Logical definition of Exponentiation
    logic integer Pow(integer x, integer n) =
        (n <= 0) ? 1 : x * Pow(x, n-1);
*/

int power(int x, int n) {
  int res = 1;
  int i = 0;

  while (i < n) {
      res = res * x;
      i = i + 1;
  }
  return res;
}

/* PROOF GOALS */
void test() {
  int p1 = power(2, 3);
  //@ assert p1 == 8;

  int p2 = power(5, 2);
  //@ assert p2 == 25;
  
  int p3 = power(10, 0);
  //@ assert p3 == 1;
  
  int p4 = power(1, 10);
  //@ assert p4 == 1;
}
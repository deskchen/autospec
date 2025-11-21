/*@
    // Logical definition of Exponentiation
    logic integer Pow(integer x, integer n) =
        (n <= 0) ? 1 : x * Pow(x, n-1);
*/

/*@
    requires n >= 0;
    
    // Prevent overflow (optional, but good for strict verification)
    // requires \abs(x) <= 46340 || n < 10; 
    
    assigns \nothing;

    // Postcondition: The result matches the logical definition
    ensures \result == Pow(x, n);
*/
int power(int x, int n) {
  int res = 1;
  int i = 0;
  
  /*@
      // 1. Bounds: i goes from 0 to n
      loop invariant 0 <= i <= n;
      
      // 2. Functional Invariant:
      //    "res" holds the calculated power so far (x^i)
      loop invariant res == Pow(x, i);
      
      loop assigns i, res;
      
      // 3. Termination: The distance to 'n' decreases
      loop variant n - i;
  */
  while (i < n) {
      res = res * x;
      i = i + 1;
  }
  return res;
}

/* PROOF GOALS */
void test() {
  int p1 = power(2, 3);
  // Logic: Pow(2,3) -> 2*Pow(2,2) -> 2*2*Pow(2,1) -> 2*2*2*1 = 8
  //@ assert p1 == 8;

  int p2 = power(5, 2);
  //@ assert p2 == 25;
  
  int p3 = power(10, 0);
  //@ assert p3 == 1;
  
  int p4 = power(1, 10);
  //@ assert p4 == 1;
}
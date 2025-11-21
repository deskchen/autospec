/*@
    logic integer GCD(integer a, integer b) =
        (a == 0) ? b :
        (b == 0) ? a :
        (a == b) ? a :
        (a > b) ? GCD(a-b, b) : GCD(a, b-a);
*/

/*@
    requires a >= 0 && b >= 0;
    
    // FIX: 'decreases' must come BEFORE assigns/ensures
    decreases a + b;
    
    assigns \nothing;
    ensures \result == GCD(a, b);
*/
int gcd(int a, int b) {
  if (a == 0)
     return b;

  if (b == 0)
     return a;

  if (a == b)
      return a;

  if (a > b)
      return gcd(a-b, b);
  return gcd(a, b-a);
}

/* PROOF GOALS */
void test() {
  int g1 = gcd(98, 56);
  //@ assert g1 == 14;

  int g2 = gcd(12, 18);
  //@ assert g2 == 6;
  
  int g3 = gcd(0, 5);
  //@ assert g3 == 5;
  
  int g4 = gcd(13, 17);
  //@ assert g4 == 1;
}
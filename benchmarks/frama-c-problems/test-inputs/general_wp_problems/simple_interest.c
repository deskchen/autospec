#include<limits.h>

int simple(int p,int n,int r)
{
 int si;
 si = p*n*r/100;
 return si;
}
 
/* PROOF GOALS:
   The verifier must prove these assertions are true.
*/
void test() {
    int s1 = simple(10000, 3, 10);
    //@ assert s1 > 0;
    //@ assert s1 <= 2 * 10000;
}
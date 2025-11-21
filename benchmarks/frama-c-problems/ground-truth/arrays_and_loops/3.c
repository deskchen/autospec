/*@ 
    requires a!=0;
    ensures \result == 1;
    assigns \nothing;
*/
int func(int a) {
    int x, y;
    int sum, res;
    if (a == 0){
        x = 0; y = 0;
    }
    else {
        x = 5; y = 5;
    }
    sum = x + y; 
    res = 10/sum; 
    return res;
}

/* PROOF GOALS:
   The verifier must prove this assertion is true.
   
   HINT: The function has a critical path (a == 0) that leads to 
   division by zero (10/0). The generated specification must 
   exclude this case for the proof to succeed.
*/
void test() {
    int res = func(10);
    //@ assert res == 1;
    
    int res2 = func(-5);
    //@ assert res2 == 1;
}
/*@
    // Define the mathematical concept of "Sum of Digits"
    // Base case: 0 or negative numbers contribute 0.
    // Recursive step: Last digit + SumDigits(Rest)
    logic integer SumDigits(integer n) =
        (n <= 0) ? 0 : (n % 10) + SumDigits(n / 10);
*/

/*@
    requires num >= 0;
    assigns \nothing;
    
    // The result must match our logical definition
    ensures \result == SumDigits(num);
*/
int func(int num) {
    int i = 0;
    int sum = 0;
    
    /*@
        loop invariant 0 <= num;
        
        // The core invariant: 
        // The sum of digits of the ORIGINAL input (\at(num,Pre))
        // is always equal to the sum we've built so far ('sum')
        // PLUS the sum of digits of the remaining number ('num').
        loop invariant SumDigits(\at(num, Pre)) == sum + SumDigits(num);
        
        loop assigns num, i, sum;
        loop variant num;
    */
    while(num > 0) {
        i = num % 10;
        sum += i;
        num /= 10;
    }
    return sum;
}

/* PROOF GOALS */
void test() {
    // Case 1: Single digit (5 -> 5)
    int s1 = func(5);
    //@ assert s1 == 5;

    // Case 2: Multiple digits (123 -> 1+2+3 = 6)
    int s2 = func(123);
    //@ assert s2 == 6;
    
    // Case 3: Number with zeros (10203 -> 1+0+2+0+3 = 6)
    int s3 = func(10203);
    //@ assert s3 == 6;

    // Case 4: Zero (0 -> 0)
    int s4 = func(0);
    //@ assert s4 == 0;
}
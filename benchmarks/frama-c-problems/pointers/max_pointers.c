/*@
    requires \valid_read(a) && \valid_read(b);
    requires \separated(a, b);
    assigns \nothing;
    
    // Correct properties of MAX:
    // 1. It is at least as big as both
    ensures \result >= *a && \result >= *b;
    
    // 2. FIX: It is equal to one OR the other (not both!)
    ensures \result == *a || \result == *b;
*/
int max_ptr(int *a, int *b){
    return (*a < *b) ? *b : *a ;
}

extern int h;

int main() {
    h = 42;
    int a = 24;
    int b = 42;

    int x = max_ptr(&a, &b);

    //@ assert x == 42;
    
    // This assertion passes because max_ptr assigns \nothing
    //@ assert h == 42;
}
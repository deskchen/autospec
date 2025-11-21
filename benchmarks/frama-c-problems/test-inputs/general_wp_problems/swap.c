void swap(int* a, int* b){
    int tmp = *a;
    *a = *b;
    *b = tmp;
    }
   
    void test(){
    int a = 42;
    int b = 37;
   
    swap(&a, &b);
   
    //@ assert a == 37 && b == 42;
   }
   
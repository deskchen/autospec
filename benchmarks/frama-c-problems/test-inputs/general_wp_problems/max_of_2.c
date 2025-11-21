#include <limits.h>

int max ( int x, int y ) {
    if ( x >=y ) 
        return x ;
    return y ;
}

 

void test()
{
    int s = max(34,45);
    //@ assert s == 45;
    int t = max(-43,34);
    //@ assert t == 34;
    int u = max(0,0);
    //@ assert u == 0;
}
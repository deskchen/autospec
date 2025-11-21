
int arraysearch(int* a, int x, int n) { 

  for (int p = 0; p < n; p++) {
    // STart
    if (x == a[p]) 
       return 1;
    // End
  }
  return 0;
} 

/* Case 1: Element is Present */
void test_present() {
  int arr[3];
  arr[0] = 10; arr[1] = 20; arr[2] = 30;

  // Helper: Proves the 'present' assumption (\exists k ...)
  //@ assert arr[1] == 20;

  int res = arraysearch(arr, 20, 3);
  
  // Verify the result is 1 (Found)
  //@ assert res == 1;
}

/* Case 2: Element is Not Present */
void test_not_present() {
  int arr[3];
  arr[0] = 10; arr[1] = 20; arr[2] = 30;

  // Helper: Proves the 'not_present' assumption (\forall k ...)
  //@ assert arr[0] != 99 && arr[1] != 99 && arr[2] != 99;
  //@ assert \forall integer k; 0 <= k < 3 ==> arr[k] != 99;

  int res = arraysearch(arr, 99, 3);
  
  // Verify the result is 0 (Not Found)
  //@ assert res == 0;
}
/* Binary search in a sorted array */

/*@
  @ predicate is_sorted(int *arr, integer n) =
  @   \forall integer i, j; 0 <= i < j < n ==> arr[i] <= arr[j];
  @*/

/*@
  @ requires n >= 0;
  @ requires \valid_read(arr + (0..n-1));
  @ requires is_sorted(arr, n);
  @ ensures \result == -1 || (0 <= \result < n && arr[\result] == target);
  @ ensures \result == -1 ==> (\forall integer i; 0 <= i < n ==> arr[i] != target);
  @*/
int binary_search(int *arr, int n, int target) {
    int left = 0;
    int right = n - 1;
    
    /*@
      @ loop invariant 0 <= left && right < n;
      @ loop invariant left <= right + 1;
      @ loop invariant \forall integer i; 0 <= i < left ==> arr[i] < target;
      @ loop invariant \forall integer i; right < i < n ==> arr[i] > target;
      @ loop assigns left, right;
      @ loop variant right - left;
      @*/
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}


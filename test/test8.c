int is_even(int n) {
  if(n < 1) {
    return 1;
  }
  return is_odd(n-1);
}
int is_odd(int n) {
  if(n < 1) {
    return 0;
  }
  return is_even(n-1);
}
int main(void) {
  int x;
  x = 9;
  printf("%d\n", is_even(x));
  printf("%d\n", is_odd(x));
  x = 8;
  printf("%d\n", is_even(x));
  printf("%d\n", is_odd(x));
}
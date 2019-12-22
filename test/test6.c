int fib(int n) {
  if(n < 2) {
    return n;
  }
  return fib(n-1) + fib(n-2);
}
int fact(int n) {
  if(n < 2) {
    return 1;
  }
  return n * fact(n-1);
}
int main(void) {
  printf("%d\n", fib(5));
  printf("%d\n", fact(5));
}
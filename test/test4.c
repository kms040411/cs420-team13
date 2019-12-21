int test2(void) {
  int x;
  x = 2+3;
  return x+4;
}
int test(void) {
  int i;
  i = 3;
  return i+test2();
}
int main(void) {
  int x;
  x = test();
  printf("%d\n", x);
}
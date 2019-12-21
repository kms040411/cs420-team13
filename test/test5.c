int test(int y) {
  int i;
  i = 3;
  return i+y;
}
int main(void) {
  int x;
  x = (test(5) + 1);
  printf("%d\n", x);
}
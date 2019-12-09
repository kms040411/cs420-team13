int multiple_call(int x) {
  return x + 2;
}
int main(void) {
  printf("%d\n", multiple_call(1));
  printf("%d\n", multiple_call(2));
}
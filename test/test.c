int callee(void) {
  printf("I am callee");
  return 1;
}
int caller(void) {
  printf("Hi");
  callee();
  printf("Bye");
  return 2;
}
int main(void) {
  caller();
}

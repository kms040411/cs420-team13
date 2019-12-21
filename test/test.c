int callee(void) {
  printf("I am callee\n");
}
int caller(void) {
  printf("Hi\n");
  callee();
  printf("Bye\n");
}
int main(void) {
  caller();
}

int callee(void) {
  printf("I am callee");
}
int caller(void) {
  printf("Hi");
  callee();
  printf("Bye");
}
int main(void) {
  caller();
}

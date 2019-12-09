int test2(void) {
  int i;
  for(i = 0; i < 10; i++) {
    if(i > 3) {
      return 1;
    }
  }
  return 0;
}

int main(void) {
  test2(); 
}
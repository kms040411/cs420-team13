int main(void) {
  int i;
  for(i = 0; i < 9; i++) {
    if(i < 2) {
      printf("if\n");
    }
    else if(i < 6) {
      printf("else if\n");
    }
    else {
      printf("else\n");
    }
  }
}
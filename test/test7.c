int main(void) {
  int i, j;
  for(i = 0; i < 3; i++) {
    for(j = 0; j < 4; j++) {
      printf("%d + %d = %d\n", i, j, i+j);
    }
  }
}
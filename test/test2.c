int test2(int y, int z) {
  int i;
  for(i = 0; i < y+z; i++) {
    if(i > 3) {
      return 1;
    }
  }
  return 0;
}

int main(void) {
  printf("%d\n", test2(4, 6)); 
}
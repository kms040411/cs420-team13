int main(void)
{
    int a;
    int *pa;
    pa = &a;
    a = 3;
    printf("%d\n", *pa);
    a = 1;
    printf("%d\n", *pa);
}
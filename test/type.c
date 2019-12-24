int f(int x, int y)
{
    return x + y;
}

int main(void)
{
    int a, b;
    int arr[3];
    a = 2.8;
    b = 1.8;
    printf("%d\n", a + b);

    printf("%d\n", f(2.6, 2.6));

    arr[0] = 1.5;
    arr[1] = 1.5;
    arr[2] = 1.5;
    printf("%d %d\n", arr[0], arr[1] + arr[2]);
}
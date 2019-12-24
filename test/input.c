int avg(int count, int *value) {
	int i, total;
	total = 0;
	for (i = 1; i < count; i++) {
		total = total + value[i];
	}
	return (total / count);
}
int main(void) {
	int studentNumber, count, i, sum;
	int mark[7];
	float average;
	sum = 0;
	for (i = 0; i < 7; i++) {
		mark[i] = i * 30;
		sum = sum + mark[i];
		average = avg(i + 1, mark);
		if (average > 40) {
		printf("%f\n", average);
		}
	}
	return 0;
	print("end");
}
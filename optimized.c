int main(void){
<<<<<<< HEAD
	int a;
	int *pa;
	pa = a &;
	a = 3;
	printf("%d\n", *pa);
	a = 1;
	printf("%d\n", *pa);
=======
	int studentNumber, count, i, sum;
	int mark[7];
	float average;
	sum = 0;
	for(i = 0; i < 6; i = i + 3){
		mark[i] = i * 30;
		sum = sum + mark[i];
		average = avg(i + 1, mark);
		if(average > 40){
			printf("%f\n", average);
		}
		mark[(i + 1)] = (i + 1) * 30;
		sum = sum + mark[(i + 1)];
		average = avg((i + 1) + 1, mark);
		if(average > 40){
			printf("%f\n", average);
		}
		mark[(i + 2)] = (i + 2) * 30;
		sum = sum + mark[(i + 2)];
		average = avg((i + 2) + 1, mark);
		if(average > 40){
			printf("%f\n", average);
		}
	}
	mark[6] = 6 * 30;
	sum = sum + mark[6];
	average = avg(6 + 1, mark);
	if(average > 40){
		printf("%f\n", average);
	}
	return 0;
>>>>>>> 2b28931a92519855cc314abc78363bc4ea290d55
}

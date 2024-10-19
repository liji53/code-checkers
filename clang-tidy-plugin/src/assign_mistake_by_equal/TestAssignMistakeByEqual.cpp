void test() {
	int a = 0, b = 0;
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-comparison"
	a == 1;
	if (b == 0) {
		a == 2;
	}
#pragma GCC diagnostic pop
	
}
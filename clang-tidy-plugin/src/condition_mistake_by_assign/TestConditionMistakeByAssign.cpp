void test() {
	int a = 0, b = 0;
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wparentheses"
	if (b = 1) {
		a = 2;
	}
	while (b = 1) {}
	for (int i = 0; i = a; i++) {}
	do {} while (b = 1);
#pragma GCC diagnostic pop
	
}
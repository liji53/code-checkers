#include <cstdio>
void test() {
	int a = 0;
	unsigned long long b = 0;
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wformat-insufficient-args,-Wformat-extra-args"
	char buf[10] = { 0 };
	snprintf(buf, sizeof(buf), "%d%%%llu", a);
	snprintf(buf, sizeof(buf), "%d%%llu", a, b);
#pragma GCC diagnostic pop
	
}
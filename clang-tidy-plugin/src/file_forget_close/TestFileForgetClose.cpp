
#include <stdio.h>

void writeCharToLog(char* data) {
    FILE* file = fopen("mylog.txt", "w");
    if (file != NULL) {
        if (!data) {
            return;
        }
        fputc(*data, file);
        fclose(file);
    }
    return;
}


void checkDoubleClose(int* data) {
    FILE* file = fopen("myfile.txt", "w");

    if (!data) {
        fclose(file);
    }
    else {
        fputc(*data, file);
    }
    fclose(file);
}


int checkLeak(int* data) {
    FILE* file = fopen("myfile.txt", "w");
    fputc(*data, file);
    return *data;
}
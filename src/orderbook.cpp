/*
ADDITIONAL IMPROVEMENTS:
- Create system for logging all transactions that have occurred
- Create system for cancelling orders
*/
#include <cstdlib>
#include <iostream>
// Datetime concerns
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

std::string utc_time() {
    char outstr[200];
    time_t t;
    struct tm *tmp;
    const char* fmt = "%T, %D";

    t = time(NULL);
    tmp = gmtime(&t);
    if (tmp == NULL) {
        perror("UTC Time Error");
        exit(EXIT_FAILURE);
    }

    if (strftime(outstr, sizeof(outstr), fmt, tmp) == 0) {
        fprintf(stderr, "strftime returned 0");
        exit(EXIT_FAILURE);
    }
    printf("%s\n", outstr);
    exit(EXIT_SUCCESS);
}

int main() {
    
    std::cout << "Hello World!";
    return 0;
}
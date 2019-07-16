#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

unsigned long x;

int vulnerable() {
	printf("> ");
	fflush(stdout);

	char buffer[128];
	read(STDIN_FILENO, &buffer[0], 1024);
  return 0;
}

void not_called() {
	if (x == (unsigned long)0xdeadbabebeefc0deUL) {
		system("/bin/sh");
	}
}

int main(int argc, char** argv) {
	vulnerable();
  if (argc == 100) {
    not_called();
  }

	return EXIT_SUCCESS;
}

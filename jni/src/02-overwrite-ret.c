#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void not_called() {
	printf("launching shell...\n");
	system("/bin/sh");
}

int vulnerable() {
	printf("> ");
	fflush(stdout);

	char buffer[128];
	read(STDIN_FILENO, &buffer[0], 256);
  return 0;
}

int main(int argc, char** argv) {
	vulnerable();

  if (argc == 1000) {
    not_called();
  }

	return EXIT_SUCCESS;
}

// Switch the 'E'xectable flag of the GNU_STACK program header in an ELF file.

#include <elf.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <memory>

using namespace std;

class UniqueFd {
 public:
  UniqueFd() : fd_(-1) {}
  UniqueFd(int fd) : fd_(fd) {}
  UniqueFd(const UniqueFd &) = delete;
  UniqueFd &operator=(const UniqueFd &) = delete;
  ~UniqueFd() {
    if (fd_ >= 0) close(fd_);
  }

  int Fd() const { return fd_; }

 private:
  int fd_;
};

int main(int argc, char **argv) {
  if (argc != 3) {
    fprintf(stderr, "usgae: %s elf on|off\n", argv[0]);
    return -1;
  }

  uint32_t xflag = 0;
  if (strcmp(argv[2], "on") == 0) {
    xflag = PF_X;
  } else if (strcmp(argv[2], "off") != 0) {
    fprintf(stderr, "usage: %s elf on|off\n", argv[0]);
    return -1;
  }

  UniqueFd fd(open(argv[1], O_RDWR));
  if (fd.Fd() == -1) {
    fprintf(stderr, "can't open %s: %s\n", argv[1], strerror(errno));
    return -1;
  }

  struct stat stat;
  if (fstat(fd.Fd(), &stat) == -1) {
    fprintf(stderr, "stat error: %s\n", strerror(errno));
    return -1;
  }
  if (stat.st_size < sizeof(Elf64_Ehdr)) {
    fprintf(stderr, "%s is not Elf format(file size too small)\n", argv[1]);
    return -1;
  }

  unique_ptr<Elf64_Ehdr> ehdr(new Elf64_Ehdr);
  if (read(fd.Fd(), ehdr.get(), sizeof(Elf64_Ehdr)) != sizeof(Elf64_Ehdr)) {
    fprintf(stderr, "read Elf64_Ehdr error\n");
    return -1;
  }
  if (ehdr->e_ident[EI_MAG0] != ELFMAG0 || ehdr->e_ident[EI_MAG1] != ELFMAG1 ||
      ehdr->e_ident[EI_MAG2] != ELFMAG2 || ehdr->e_ident[EI_MAG3] != ELFMAG3) {
    fprintf(stderr, "%s is not ELF format\n", argv[1]);
    return -1;
  }
  if (ehdr->e_ident[EI_CLASS] != ELFCLASS64) {
    fprintf(stderr, "only ELF64 is supported\n");
    return -1;
  }

  Elf64_Addr phoff = ehdr->e_phoff;
  uint16_t phnum = ehdr->e_phnum;
  unique_ptr<Elf64_Phdr> phdr(new Elf64_Phdr);
  bool found = false;
  if (lseek(fd.Fd(), phoff, SEEK_SET) == -1) {
    fprintf(stderr, "can't lseek: %s\n", strerror(errno));
    return -1;
  }
  for (uint16_t i = 0; i < phnum; ++i) {
    if (read(fd.Fd(), phdr.get(), sizeof(Elf64_Phdr)) != sizeof(Elf64_Phdr)) {
      fprintf(stderr, "read Elf64_Phdr error\n");
      return -1;
    }
    phoff += sizeof(Elf64_Phdr);
    if (phdr->p_type == PT_GNU_STACK) {
      found = true;
      break;
    }
  }
  if (!found) {
    fprintf(stderr, "can't find GNU_STACK program header\n");
    return -1;
  }
  phoff -= sizeof(Elf64_Phdr);

  if ((phdr->p_flags & PF_X) == xflag) {
    fprintf(stderr, "X flag is already %s\n", xflag ? "set" : "clear");
    return 0;
  }

  if (xflag) {
    phdr->p_flags |= xflag;
  } else {
    phdr->p_flags &= ~PF_X;
  }
  if (lseek(fd.Fd(), phoff, SEEK_SET) == -1) {
    fprintf(stderr, "can't lseek for write: %s\n", strerror(errno));
    return -1;
  }
  if (write(fd.Fd(), phdr.get(), sizeof(Elf64_Phdr)) != sizeof(Elf64_Phdr)) {
    fprintf(stderr, "write Elf64_Phdr error: %s\n", strerror(errno));
    return -1;
  }
  return 0;
}

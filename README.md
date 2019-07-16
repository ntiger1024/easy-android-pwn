Easy android pwn
================

This project is based on [easy-linux-pwn](https://github.com/xairy/easy-linux-pwn).

Those tasks in the origin project can't be solved on the newer android platforms(for example, 9.0)
because thare are some differences between android and traditional linux distributions:

1. Android randomizes addresses of dynamic libraries even if ASLR is disabled
2. Android-NDK forces '-z noexecstack' option when build executables

So I do some works to port these tasks to Android platform.

Rrerequisites & Setup
---------------------

1. Follow instructions in [easy-linux-pwn](https://github.com/xairy/easy-linux-pwn)
2. Android 9.0 device
3. Build you own Android ROM with the following change. (or just push [linker64](linker64) to /system/bin/ if you are lucky enough(May brick you device!!!))

    ```C++
    diff --git a/linker/linker.cpp b/linker/linker.cpp
    index c78b9aba6..d20995162 100644
    --- a/linker/linker.cpp
    +++ b/linker/linker.cpp
    @@ -1493,13 +1493,13 @@ static bool find_library_internal(android_namespace_t* ns,

     static void soinfo_unload(soinfo* si);

    -static void shuffle(std::vector<LoadTask*>* v) {
    -  for (size_t i = 0, size = v->size(); i < size; ++i) {
    -    size_t n = size - i;
    -    size_t r = arc4random_uniform(n);
    -    std::swap((*v)[n-1], (*v)[r]);
    -  }
    -}
    +// static void shuffle(std::vector<LoadTask*>* v) {
    +//   for (size_t i = 0, size = v->size(); i < size; ++i) {
    +//     size_t n = size - i;
    +//     size_t r = arc4random_uniform(n);
    +//     std::swap((*v)[n-1], (*v)[r]);
    +//   }
    +// }

     // add_as_children - add first-level loaded libraries (i.e. library_names[], but
     // not their transitive dependencies) as children of the start_with library.
    @@ -1603,7 +1603,7 @@ bool find_libraries(android_namespace_t* ns,
           load_list.push_back(task);
         }
       }
    -  shuffle(&load_list);
    +  // shuffle(&load_list);

       for (auto&& task : load_list) {
         if (!task->load()) {
    diff --git a/linker/linker_phdr.cpp b/linker/linker_phdr.cpp
    index a5eab44ec..4c6cdf494 100644
    --- a/linker/linker_phdr.cpp
    +++ b/linker/linker_phdr.cpp
    @@ -548,6 +548,7 @@ static void* ReserveAligned(void* hint, size_t size, size_t align) {
       uint8_t* first = align_up(mmap_ptr, align);
       uint8_t* last = align_down(mmap_ptr + mmap_size, align) - size;
       size_t n = arc4random_uniform((last - first) / PAGE_SIZE + 1);
    +  n = 1;
       uint8_t* start = first + n * PAGE_SIZE;
       munmap(mmap_ptr, start - mmap_ptr);
       munmap(start + size, mmap_ptr + mmap_size - (start + size));
    ```

4.  For task 04 and task 05, make their stack executable using [`switch_execstack`](tools/switch_execstack.cc)

    ```shell
    $ ./tools/switch_execstack libs/arm64-v8a/04-shellcode-static on

    $ aarch64-linux-android-readelf -l libs/arm64-v8a/04-shellcode-static
    ...
    Program Headers:
        ...
        GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RWE    10
        ...
    ```

5. Disable ASLR: `adb shell 'echo 0 > /proc/sys/kernel/randomize_va_space'`

Issues
------

It seems like [`one_gadget'](https://github.com/david942j/one_gadget) does not support android. So task 03 is not work.

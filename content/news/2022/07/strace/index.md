---
title: "strace"
date: 2022-07-13T22:05:17-04:00
---

So, I am not smart, and I have made this mistake enough times that I'm writing
it down for both my future self, and also for anyone that encounters the same
issue.

I was testing Mesa drivers and ran into the following error:

~~~
libGL error: MESA-LOADER: failed to open iris: libLLVM-13.so.1: cannot open shared object file: No such file or directory (search paths /home/jcgregorio/mesa/22.1.3, suffix _dri)
libGL error: failed to load driver: iris
libGL error: MESA-LOADER: failed to open swrast: libLLVM-13.so.1: cannot open shared object file: No such file or directory (search paths /home/jcgregorio/mesa/22.1.3, suffix _dri)
libGL error: failed to load driver: swrast
X Error of failed request:  BadValue (integer parameter out of range for operation)
  Major opcode of failed request:  149 (GLX)
  Minor opcode of failed request:  24 (X_GLXCreateNewContext)
  Value in failed request:  0x0
  Serial number of failed request:  71
  Current serial number in output stream:  72
~~~

Now the very first thing I _see_ when I read the above is:

~~~
libGL error: MESA-LOADER: failed to open iris:
(search paths /home/jcgregorio/mesa/22.1.3, suffix _dri)
~~~

And I **know** that `iris_dri.so` is in `/home/jcgregorio/mesa/22.1.3`, so I'm
absolutely baffled by the failure. So I spend _way_ too much time rebuilding Mesa
with different configuration flags to figure out why it's not finding the DRI
file, all with no luck.

Finally, in an act of desperation, I run the app under `strace` to see if I can
determine why the file isn't being loaded, and this is what I find:

~~~
geteuid()                               = 1000
getuid()                                = 1000
openat(AT_FDCWD, "./tls/iris_dri.so", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "./iris_dri.so", O_RDONLY|O_CLOEXEC) = 5
read(5, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
~~~

Wait, what? It's actually finding the file and opening it. So why is it eventually failing?
Well, let's look at the strace info after the successful open:

~~~
openat(AT_FDCWD, "./iris_dri.so", O_RDONLY|O_CLOEXEC) = 5
read(5, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0"..., 832) = 832
newfstatat(5, "", {st_mode=S_IFREG|0755, st_size=183442400, ...}, AT_EMPTY_PATH) = 0
getcwd("/home/chrome-bot/mesa/foo", 128) = 26
mmap(NULL, 27868456, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 5, 0) = 0x7f470a800000
mprotect(0x7f470a890000, 24944640, PROT_NONE) = 0
mmap(0x7f470a890000, 16986112, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 5, 0x90000) = 0x7f470a890000
mmap(0x7f470b8c3000, 7954432, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 5, 0x10c3000) = 0x7f470b8c3000
mmap(0x7f470c05a000, 516096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 5, 0x1859000) = 0x7f470c05a000
mmap(0x7f470c0d8000, 1817896, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f470c0d8000
close(5)                                = 0
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 5
newfstatat(5, "", {st_mode=S_IFREG|0644, st_size=76051, ...}, AT_EMPTY_PATH) = 0
mmap(NULL, 76051, PROT_READ, MAP_PRIVATE, 5, 0) = 0x7f470d7d7000
close(5)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/glibc-hwcaps/x86-64-v4/libLLVM-13.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/lib/x86_64-linux-gnu/glibc-hwcaps/x86-64-v4", 0x7ffcebad7830, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/glibc-hwcaps/x86-64-v3/libLLVM-13.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/lib/x86_64-linux-gnu/glibc-hwcaps/x86-64-v3", 0x7ffcebad7830, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/glibc-hwcaps/x86-64-v2/libLLVM-13.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/lib/x86_64-linux-gnu/glibc-hwcaps/x86-64-v2", 0x7ffcebad7830, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/tls/haswell/avx512_1/x86_64/libLLVM-13.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "/lib/x86_64-linux-gnu/tls/haswell/avx512_1/x86_64", 0x7ffcebad7830, 0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/tls/haswell/avx512_1/libLLVM-13.so.1", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
~~~

At this point I realize the problem is that the `iris_dri.so` file depends on `libLLVM-13.so`,
and **that's the file that's missing**. Now looking back at the full error output I can see that's 
what it was trying to tell me:

~~~
libGL error: MESA-LOADER: failed to open iris: libLLVM-13.so.1: cannot open shared object file: No such file or directory (search paths /home/jcgregorio/mesa/22.1.3, suffix _dri)
libGL error: failed to load driver: iris
libGL error: MESA-LOADER: failed to open swrast: libLLVM-13.so.1: cannot open shared object file: No such file or directory (search paths /home/jcgregorio/mesa/22.1.3, suffix _dri)
~~~

The fix was as simple as:

~~~
sudo apt install libllvm13
~~~

But the real lesson is to fully read the error messages before jumping to conclusions.

The second lesson is to jump to using `strace` sooner rather than later.
---
layout: post
title: Core Slicing
---

With [Spectre and Meltdown](https://meltdownattack.com/) we can see the
inevitable results of trying to squeeze more and more performance out of a
small number of cores. I believe the future is in processors with a high
number of cores, such as [RISC-V](https://riscv.org/). With hundreds or
thousands of cores on a single chip you can stop doing time-slicing and start
doing core-slicing. That is, instead of doing preemtive multitasking, each
process will be scheduled with a subset of the total number of core. The cores
will be distrubuted among the processes that are running and they will keep
those cores until they are done. A change in priority for a process would mean
they get more or less cores.

<a href="https://brid.gy/publish/twitter"></a>

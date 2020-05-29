---
title: Compute and Moore's Law
date: 2017-06-21T12:00:00-04:00
tags:
  - tech
---

This article from Technology Review,
[How AI Can Keep Accelerating After Moore’s Law](https://www.technologyreview.com/s/607917/how-ai-can-keep-accelerating-after-moores-law/)
is a good follow-on from a previous article
[Moore’s Law Is Dead. Now What?](https://www.technologyreview.com/s/601441/moores-law-is-dead-now-what/).

From the second article:

> Engineers have kept GPUs getting more powerful because they can be more
> specialized to the particular math they need to perform for graphics or
> machine learning, he says.

In order to continue to squeeze more performance out of the same number of
transistors and/or watts, we are going to need to get closer to the metal, and
the metal is going to have to become more and more specialized, or at the very
least, the metal has to stop looking like monolithic CPUs with a small number
of cores.

GPUs by themselves, even if you only have OpenGL, are attractive because
of the enormous amount of specialized computational power available. This power is what
originally attracted people to General Purpose GPU
[GPGPU](https://en.wikipedia.org/wiki/General-purpose_computing_on_graphics_processing_units), which started as
people transforming scientific computations into a graphical form to get them
to run on a GPU. That work in turn drove the creation and adoption of general
compute APIs like CUDA and then OpenCL, which expose the underlying compute
units and specialized memory access features in a GPU.

Compute APIs are much closer to the metal, exposing the underlying power of
the GPU without the intervening machinery and bugs of the OpenGL abstraction.
The API surface of these compute APIs are much smaller, which should mean
simpler and less buggy drivers. In addition the compute APIs are focused in
part on scientific applications, so the results from using compute APIs should
be much more repeatable. At the very least using compute APIs we are [in
control of what performance/accuracy tradeoff to make](https://www.khronos.org/registry/OpenCL/sdk/1.0/docs/man/xhtml/log.html). Compute APIs are also
becoming more widely available, with every next generation API (Vulkan, DX12,
and Metal) supporting a compute component.

One of the more surprising things I learned recently was exactly how sloppy
OpenGL could be. For example, from the [documentation for the OpenCL log
function](https://www.khronos.org/registry/OpenCL/sdk/1.0/docs/man/xhtml/log.html),
you can choose between the native hardware accelerated version
of log, or use a log function that will return accurate results.

> native_log computes natural logarithm over an implementation-defined range. **The maximum error is implementation-defined**.

I think it's time for me to find an OpenCL library for [Go](https://golang.org) and
start exploring [GPU's on Google Compute Engine](https://cloud.google.com/gpu/).

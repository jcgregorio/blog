---
layout: post
title: Tile Store
---

My team at Google is the infrastructure team for [Skia](https://skia.org):

> Skia is an open source 2D graphics library which provides common APIs that work
> across a variety of hardware and software platforms. It serves as the graphics
> engine for Google Chrome and Chrome OS, Android, Mozilla Firefox and Firefox
> OS, and many other products.

Skia, being a graphics library, needs to be tested for both performance and
correctness, and being cross-platform, it needs to be tested across a wide
variety of platforms and under different configurations. Skia has a variety of
backends, i.e. the same drawing commands can be directed to be rendered via:

  * Raster - Using the CPU-only.
  * Ganesh - Skia’s GPU-accelerated backend.
  * PDF - PDF document creation.
  * SVG - An experimental SVG renderer.

All of those backends need to be tested across different platforms (Windows,
Android, Linux, Max, iOS), different architectures (x86\_64, Arm64, Arm7), and a
wide range of other options that can be selected on how Skia renders. Testing a
wide range of GPUs is required because different GPUs have different behaviors,
including some very buggy but widely deployed versions of OpenGL, so we current
test against a large number of both desktop and mobile GPUs. All of this
variety creates a combinatorial explosion in test data. For every commit to
Skia the tests result in roughly 800,000 performance metrics and one million
images being rendered. There are about 30 commits a day to the Skia repo, so
that ends up being a lot of data. Sure, not a lot compared to other projects in
Google, but Skia is open source, and we prefer to build all of our tooling also
as open source, and we needed to build tools to analyze and monitor all those
performance metrics and correctness images, and so we needed data storage with
the following requirements:

  * Not an SQL database.
  * Very fast access for recent data to allow ad-hoc analysis.
  * Reasonable access for older data.
  * Commit based organization.
  * Robust, i.e. we can’t lose data.

The requirement that it not be an SQL database is a personal preference, I’m
sure there are a large contingent of people that will tell me that Postgres is
the perfect solution, but apparently I’m not smart enough to run/use/tune an
SQL database, particularly for large amounts of data. I might give [Spanner](https://cloud.google.com/spanner/) a
chance  in the future, and if so I will certainly give an update. [BigQuery](https://cloud.google.com/bigquery/)
might also work. Regardless, we built these apps a long time before either
Spanner or BigQuery were available, so they weren’t viable options at the time.

One of the other odd requirements is the commit based organization of the data.
This is obviously because the data needs to align with the commits to Skia, but
it isn’t that straightforward because tests on different machines take
different amounts of time, and we also continually backfill tests when we have
spare capacity, so test results almost never arrive in order.

Since there wasn’t a single system that could meet all these requirements we
split the problem into two systems, one for robust storage, and a second system
for fast access for real time analysis.

  * Robust storage (GCS) - The ‘source of truth’ documents are stored in Google Cloud Storage.
  * Fast Access (Tile Store) - An intermediate form, built on key-value stores, such as BoltDB, organized into chunks of commits called tiles.

Storing the source of truth documents on Google Cloud Storage takes care of the
robustness. The data files are all JSON and PNG images, which is what is
emitted by the tools that do the performance and correctness testing. The JSON
files are written out to a unique name which include year/month/day/hour in the
path. This allows for easy rebuilding of the Tile Store, just scan for all the
files based on the year/month/day/hour over your desired time range and ingest
them into the Tile Store. And given that the Tile Store can be rebuilt easily
from the ‘source of truth’ documents, we don’t need to back them up.

The Tile Store is optimized for very fast writes and fast querying.
Additionally, we run on machines large enough to keep all the data for the last
100 commits in memory for very fast access, refreshed from the tiles
periodically.

For trace data we store each point as a pair, the index of the point and then
the value of the trace at that point. That is, if the tile size is 50 then each
point in a trace is at an index in [0, 49]. So the values stored for a trace
might look like:

    [0, 1.23], [1, 3.21], [2, 5.67], ...

Note that the points may not arrive in order, so they could actually be stored
as:

    [2, 5.67], [0, 1.23], [1, 3.21], ...

Also note that points are only appended, and the last value for a point is the
one that's used, so duplicate data may exist in the trace:

    [2, 5.67], [0, 1.23], [1, 3.21], [2, 5.50], ...

This can happen if a test is re-run, we always use the latter value, so the
value at index 2 of this trace will be 5.50, not 5.67.

You can check out the [code and documentation](https://cloud.google.com/bigquery/) if you are interested in the
details of the how the tiles are structured.

I wrote this up mostly as a historical marker, since by next year we might be
fully on Spanner or some other storage technology, and also to find out how
other people have solved similar problems.

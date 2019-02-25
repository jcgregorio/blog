---
layout: post
title: gcsfuse and systemd --user
---

Google Cloud Storage has an officially supported [fuse client](https://cloud.google.com/storage/docs/gcs-fuse)!

This is something I have always wanted and would have expected for Google
Drive, but 🤷.

The only thing better than a fuse client is a fuse directory that gets
mounted automatically when you log in, which you can do fairly simply
using `systemd --user`, which is just systemd, but everthing runs as you.

Here's a gist of how I set this up on my machine:

<script src="https://gist.github.com/jcgregorio/3d30cb7673e80b85c2153db9ff8be7c4.js"></script>

<a href="https://brid.gy/publish/twitter"></a>

---
title: 'Bazel and Gopls'
date: 2021-06-10T09:12:40-04:00
---

So Bazel and the Go language server
[gopls](https://pkg.go.dev/golang.org/x/tools/gopls) don't get along very well.
The problem is that Bazel generates a bunch of `bazel-\*` directories that gopls
then tries to process, which can cause gopls to produce a slew of invalid
warnings, run slowly, and sometimes even crash. The solution I've found so far
is to add the following to my `.bazelrc` file:

```
build --symlink_prefix=_bazel_
test  --symlink_prefix=_bazel_

# Also suppress the generation of the bazel-out symlink, which always appears,no
# matter what you set --symlink_prefix to.
build --experimental_no_product_name_out_symlink
```

This causes the created directories to begin with an underscore, which all Go
tools should ignore.

This looks like the same solution CockroachDB
[came up with](https://github.com/cockroachdb/cockroach/pull/65327).

Of course, a better solution would be for Go to support an ignore file like
every other tool, ala `.dockerignore`, `.gitignore`, `.bazelignore`, etc. That's
tracked in
[proposal: global ignore mechanism for Go tool ecosystem](https://github.com/golang/go/issues/42965),
but given the push back from the core Go developers every time this issue is
raised is "just sprinkle empty go.mod files in those directories", which is both
impractical and just a tad arrogant, I'm not very hopeful.

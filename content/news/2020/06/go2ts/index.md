---
title: 'go2ts'
date: 2020-06-09T19:10:41-04:00
draft: true
---

[go2ts](https://pkg.go.dev/github.com/skia-dev/go2ts?tab=overview) is a simple
and powerful Go to Typescript generator. It can handle all JSON serializable Go
types and also has the ability to define TypeScript union types.

Written because none of the existing solutions did what I wanted.

This code originally started from
[struct2ts](https://github.com/OneOfOne/struct2ts) when I started writing a PR
to add the features I wanted, but after adding unit tests, cleaning up the code
to meet our internal standards, and removing features temporarily so I could
more easily understand the code, I realized I only had a handful of lines in
common with the original project, so I instead forked it into its own project.

Note that this doesn't have a CLI, and that is intentional. To use the library
you will need to write Go code, which I think is completely reasonable given
what it does.

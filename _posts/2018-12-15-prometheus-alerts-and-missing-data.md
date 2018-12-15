---
layout: post
title: Prometheus alerts and missing data
---

Alerting in [Prometheus](https://prometheus.io) is great, and easy, but one of
the gotchas is that there's no warnings or errors if you write an alert rule
and there's no data for that alert.

Now Prometheus does have the `absent()` function, and you could tack

    OR absent(some_metric_name) == 1

to the end of every alert you write, but that's tedious and error prone.
So I wrote [promk-absent](https://github.com/google/skia-buildbot/blob/master/promk/go/promk-absent/main.go)
a quick little tool on Go to create a set of absence alerts based on
an existing set of alerts. It just processes a single alerts YAML file
and emits a new alerts YAML file with one absent alert for each alert
in the original file. To install it run:

    go get go.skia.org/infra/promk/go/promk-absent

Then run it with

    promk-absent --input=your-rules.yml --output=absent-rules.yml

Don't forget to include your new absent rules in your `prometheus.yml`
file.

The tool does have the restriction that all expressions must be written in
the form of:

    expression relation constant

and so far that hasn't been an issue for us.

<a href="https://brid.gy/publish/twitter"></a>

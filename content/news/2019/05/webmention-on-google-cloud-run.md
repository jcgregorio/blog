---
title: Webmention on Google Cloud Run
date: 2019-05-06T12:00:00-04:00
tags:
  - webmention
---

I just published
[webmention-run,](https://github.com/jcgregorio/webmention-run) a [Google
Run](https://cloud.google.com/run/docs/) application written in
[Go](https://golang.org) that implements
[Webmention](https://indieweb.org/Webmention). I'm now using this to handle
webmentions on [bitworking.org](http://bitworking.org). Given the generous free
quota for Google Run I don't expect this to cost me anything. This is on top of
using [Firebase Hosting](https://firebase.google.com/docs/hosting) to host the
static ([Jekyll](https://jekyllrb.com/)) parts of my blog, which is also
effectively free.

Another awesome feature is that both services will provide SSL certificates; in
my case Firebase Hosting provides the cert for https://bitworking.org, and
Google Cloud Run provides the SSL cert for the subdomain where my instance of
`webmention-run` is running, which is the subdomain
https://webmention.bitworking.org.

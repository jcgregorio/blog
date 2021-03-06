---
title: Stream
date: 2019-06-16T12:00:00-04:00
tags:
  - standards
  - webmention
---

I've launched a new micro-blog at [stream.bitworking.org](https://stream.bitworking.org), which has an
[Atom Feed](https://stream.bitworking.org) if you want to follow along. You
can also follow along on Mastodon by following
`@stream.bitworking.org@stream.bitworking.org` thanks to [https://fed.brid.gy/](https://fed.brid.gy/).
Any entries will also appear on Twitter thanks to [https://brid.gy](https://brid.gy).
Interactions on any of those sites should flow back to
Stream thanks to [webmention](https://www.w3.org/TR/webmention/) support via
[github.com/jcgregorio/webmention-run](https://github.com/jcgregorio/webmention-run).

Finally the admin interface to Stream is a
[PWA](https://developers.google.com/web/progressive-web-apps/) that supports
the [Web Share Target API](https://developers.google.com/web/updates/2018/12/web-share-target),
which means I can trivially share content to Stream using the native Android
Share intent.

The backend is written in Go and it runs entirely on [Google Cloud Run](https://cloud.google.com/run/).
The login is handled via
[Google Sign-In for Websites](https://developers.google.com/identity/sign-in/web/), and
[Workbox](https://developers.google.com/web/tools/workbox/) is used for the
PWA aspects.

The [code for Stream is on GitHub](https://github.com/jcgregorio/stream-run)
and I've endeavored to make it customizable via the `config.json` file, but no
guarantees since I just got it all working today.

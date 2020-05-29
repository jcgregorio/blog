---
title: Blogging drawings
date: 2018-01-21T12:00:00-05:00
---

One of the goals with my new blogging system has been a flow for getting hand
drawn images onto the blog. I will admit this is purely driven by jealousy of
the awesome drawings on [the morning
paper](https://blog.acolyer.org/2016/04/21/the-amazing-power-of-word-vectors/).
I didn't know if I'd ever find a setup I would like until I got to borrow a
[Google Pixelbook](https://store.google.com/us/product/google_pixelbook),
which is just an amazing machine and deserves a writeup on its own, but has
several key features, such as the ability to run Android apps and the ability
to fold over and turn into a tablet, along with one of the best digital pens
I've ever used. In the end my flow looks like this:

![Squid to Google Drive to Jekyll to GCE](/images/2018/blogging_pictures.png){: style="max-width:70%"}

[Squid](https://play.google.com/store/apps/details?id=com.steadfastinnovation.android.projectpapyrus)
is an Android app, one of the dozens I looked at, and the one that worked
the best for me, which means it is simple and has nice defaults.

The "NUC" is my desktop machine which is where my blogging work is mostly
done, but that's a machine I almost never physically touch, I'm almost always
accessing it over SSH, which is why this flow is probably a little more
complicated than you might have guessed.

The "GCE" box in that picture is the Google Compute Enging instance that runs
[userve](https://github.com/jcgregorio/userve) and hosts this blog.

<a href="https://brid.gy/publish/twitter"></a>


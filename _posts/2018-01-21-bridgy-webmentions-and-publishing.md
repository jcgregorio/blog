---
layout: post
title: Bridgy, webmentions, and publishing.
---

[Brid.gy](https://brid.gy/about#webmentions) has a cool feature for
automatically posting blog posts to Twitter, which is interesting because it
uses Webmentions to kick off the whole process. I.e. just including the
link:

    <a href="https://brid.gy/publish/twitter"></a>

The webmention sent to brig.gy triggers it to look back at the post, parse it
and look for microformats indicating what content to publish, and then posts
it to Twitter.

![Using webmentions to trigger brid.gy to publish to Twitter](/images/2018/bridgy.png)

Note that this also works for Facebook and flickr, and you obviously need to
authorize brid.gy to post to Twitter for you.

<a href="https://brid.gy/publish/twitter"></a>

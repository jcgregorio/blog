---
layout: post
title: Vanilla JS Sample Apps
---

I spent some time over the holidays porting [web framework sample apps
over to vanilla JS](https://github.com/jcgregorio/vanillajs).

I'll add the same caveat here that I also included in the code:

> The code works w/o polyfils in Chrome. To get it to run in a wider range of
> browsers you will need to add polyfills and, depending on the target browser
> version, compile the JS back to an older version of ES, and run a prefixer
> on the CSS. The wider the target set of browsers and the older the versions
> you are targeting the more processing you will need to do via webpack, but
> since the original code doesn't need to change, those extra processing steps
> are out of scope for these examples.

The samples are all built using [Yarn](https://yarnpkg.com/) and [WebPack
3](https://webpack.js.org/), both of which I really enjoyed working with.

In all cases, I tried to change as little of the original code as possible,
keeping the same CSS if possible, and the same breakdown in app struture, so
the apps should look and operate identically to the original samples.

Related reading:

  1. [No more JS frameworks](https://bitworking.org/news/2014/05/zero_framework_manifesto).
  2. [Six Places](https://bitworking.org/news/2015/03/Six_Places), guidance on
     how to stich together web applications using custom elements.
  3. [Custom Elements v1: Reusable Web Components](https://developers.google.com/web/fundamentals/web-components/customelements),
     a great intro, in particular check out the "Best Practices" section.

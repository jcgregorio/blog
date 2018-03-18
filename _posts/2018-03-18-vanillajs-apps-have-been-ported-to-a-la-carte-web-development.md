---
layout: post
title: VanillaJS apps have been ported to a la carte web development
---

My [VanillaJS](https://github.com/jcgregorio/vanillajs) project, where I
re-implement popular framework sample apps in vanilla JavaScript, has now been
ported over to ['a la carte'](https://bitworking.org/news/2018/03/a-la-carte-web-development) web development. In this case that means they
all use [pulito](https://www.npmjs.com/package/pulito) for their tooling and
directory structure, and individual framework ports bring in templating
libaries as needed. For example, the [React sample rewrite](https://github.com/jcgregorio/vanillajs/tree/master/react)
uses [lit-html](https://github.com/Polymer/lit-html) for templating, and the
[Angular sample rewrite](https://github.com/jcgregorio/vanillajs/tree/master/angular-todo)
uses [hyperHTML](https://github.com/WebReflection/hyperHTML) for templating.

This is a perfect example of the power of [a la carte](https://bitworking.org/news/2018/03/a-la-carte-web-development)
web development, where you get to pick the components you want and only have
to 'pay' for what you use.

<a href="https://brid.gy/publish/twitter"></a>

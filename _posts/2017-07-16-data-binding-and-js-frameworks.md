---
layout: post
title: Data binding and JS frameworks
---

It was over three years ago that I wrote
[No more JS frameworks](https://bitworking.org/news/2014/05/zero_framework_manifesto), at which time
I was roundly criticized for not understanding that data binding could only be
done via JS framework, the two were inextricably linked, and only 2-way data
binding would do, as one way data binding was for weak-minded fools who
weren't building real applications. You can find the comments on HN yourself,
I don't link to that cesspool.

So, in that context, it was funny to read
[Why Angular 2/4 Is Too Little, Too Late](https://medium.com/@chriscordle/why-angular-2-4-is-too-little-too-late-ea86d7fa0bae):

> Two way data-binding was a feature in 2013 and Facebook said it was a **bug**.
> It turns out they were *right*.

The post goes on to explain how the "industry settled on
[Redux](http://redux.js.org/)", which is nice to see that the functionality
is delivered as a standalone library, and [MIT Licensed](https://github.com/reactjs/redux/blob/master/LICENSE.md),
because [licenses matter](https://issues.apache.org/jira/browse/LEGAL-303).

My only concern is that I believe I too work in the industry and I've spent
the last three years delivering applications using
[Polymer](https://www.polymer-project.org/), so I guess I'm not "settled"?

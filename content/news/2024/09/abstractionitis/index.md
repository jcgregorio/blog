---
title: Abstraction-itis
date: 2024-09-29T23:00:00-04:00
---

So, [Ryan Carniato](https://dev.to/ryansolid), the author of [SolidJS](https://www.solidjs.com/), posted this as a comment on his blog entry entitiled, ["Web Components Are Not the Future"](https://dev.to/ryansolid/web-components-are-not-the-future-48bh#comment-2id69)

> Thank you for your response. A lot of this sprung from my realization just how
> much of a cost supporting Web Components properly has had on the library. And
> how it is basically endless. We doubled the size and complexity of our event
> delegation code in the last release (1.9) just to handle Shadow DOM better and
> it still falls flat for many cases because of how Shadow DOM is designed. It's
> not within our means to fix, but when we say we support Web Components people
> come to expect it. I could delete pages of code if I didn't care to support
> Web Components I could simplify many things.

To summarize, the author of a web framwork that tries to abstract how the author
_thinks_ a browser works, is complaining about the amount of work it takes to
conform their abstraction to how a browser **actually** works. 

To the author, a sufferer of the condition I refer to as _abstractionitis_, I
offer this for all their woes, a tiny unicode violin: <small>🎻<small>.
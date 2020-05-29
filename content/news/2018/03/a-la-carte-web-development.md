---
title: A la carte Web Development
date: 2018-03-13T12:00:00-04:00
tags:
  - a la carte
  - standards
  - web components
---

[Stop using JS Frameworks](https://bitworking.org/news/2014/05/zero_framework_manifesto) is something I’ve been advocating for years now, and a
legitimate question I get is what do you replace it with?

The answer is "a la carte" web development.

Instead of picking a monolithic solution like a web framework, you just pick
the pieces you need. I don’t mean any old random pieces, below I am going to
outline specific criteria that need to be met for some components to
participate in a la carte web development.

To get a better feel for this let's start by looking at what a web framework
"normally" provides. The "normally" is in quotes because not all frameworks
provide all of these features, but most frameworks provide a majority of them:

- Framework
  - Model
  - Tooling and structure
  - Elements
  - Templating
  - State Management

All good things, but why do they have to be bundled together like a TV dinner?

## A la carte

"A la carte" web development does away with the framework, says just
use the browser for the model, and the rest of the pieces you pick and choose
the ones that work for you. In a la carte development each bullet point is a
separate piece of software:

_A la carte_

Tooling and structure
: Defines a directory structure for how a project is put together and provides tooling such as
JS transpiling, CSS prefixing, etc. for projects that conform that directory structure.
Expects ES6 modules with the extension that webpack, rollup, and similar tools presume, i.e.
allow importing other types of files, see [webpack loaders](https://webpack.js.org/concepts/#loaders).

Elements
: A library of v1 custom elements in ES6 modules. Note that these elements must be provided in ES6
modules with the extension that webpack, rollup, and similar tools presume, i.e.
allow importing other types of files, see [webpack loaders](https://webpack.js.org/concepts/#loaders).
The elements much also be ["neat"](https://bitworking.org/news/2018/02/custom-elements-neat), i.e.
just HTML, CSS, and JS. No SCSS or templating libraries.

Templating
: Any templating library you like, as long as it works with v1 custom elements.

State Management
: Any state management library you like, if you even need one.

The assumptions needed for all of this to work together are fairly minimal:

1. ES6 modules and the extension that webpack, rollup, and similar tools presume, i.e.
   allow importing other types of files, see [webpack loaders](https://webpack.js.org/concepts/#loaders).
2. The base elements are “Neat”, i.e. they are JS, CSS, and HTML only. No additional
   libraries are used, such as a templating library. Note that sets of ‘neat’ elements also conform
   to #1, i.e. they are provided as webpack/rollup compatible ES6 modules.

Obviously there are other guidelines that could be added as advisory, for example
[Google Developers Guide - Custom Elements Best Practices](https://developers.google.com/web/fundamentals/web-components/best-practices),
should be followed when creating custom elements sets,
except for the admonition to use Shadow DOM, [which I would avoid for now, unless you really need it](https://bitworking.org/news/2018/02/shadow-dom-and-css).

Such code will natively run in browsers that support custom elements v1. To get
it to run in a wider range of browsers you will need to add polyfills and,
depending on the target browser version, compile the JS back to an older
version of ES, and run a prefixer on the CSS. The wider the target set of
browsers and the older the versions you are targeting the more processing you
will need to do, but the original code doesn't need to change, and all those
extra processing steps are only incurred by projects that need it.

## Concrete

To move this proposal beyond just theoretical I’ve been developing and
porting applications over to this model for the past few months.

We just published [pulito](https://www.npmjs.com/package/pulito), a stake in the ground for what a "tooling and
structure" component looks like. You will note that it isn't very complex, nothing more than an opinionated
webpack config file.

Similarly we’ve published our set of "neat" custom elements
[skia-elements](https://www.npmjs.com/package/skia-elements). A small set of
elements that is still very much a work in progress. Documentation and live
demos for skia-elements can be found on
[jsdoc.skia.org](https://jsdoc.skia.org).

Our current stack looks like:

Tooling and structure
: [pulito](https://www.npmjs.com/package/pulito)

Elements
: [skia-elements](https://www.npmjs.com/package/skia-elements)

Templating
: [lit-html](https://www.npmjs.com/package/lit-html)

We have used Redux in an experimental app that never shipped and haven’t needed
any state management libraries in the other applications we’ve ported over, so
our 'state management' library is still an open question.

## Example

What is like to use this stack? Let's start from an empty directory
and start building a web app:

    $ yarn init
    $ yarn add pulito

We are starting from scratch so use the project skeleton that [pulito](https://www.npmjs.com/package/pulito) provides:

    $ unzip node_modules/pulito/skeleton.zip
    $ yarn

We can now run the dev server and see our running skeleton application:

    $ make serve

Now let's add in [skia-elements](https://www.npmjs.com/package/skia-elements) and add a set of tabs to the UI.

    $ yarn add skia-elements

Now add imports to `pages/index.js` to bring in the elements we need:

```javascript
import 'skia-elements/tabs-sk';
import 'skia-elements/tabs-panel-sk';
import '../modules/example-element';
```

And then use those elements on `pages/index.html`:

```html
<body>
  <tabs-sk>
    <button class="selected">Some Tab</button>
    <button>Another Tab</button>
  </tabs-sk>
  <tabs-panel-sk>
    <div>
      <p>This is Some Tab contents.</p>
    </div>
    <div>
      This is the contents for Another Tab.
    </div>
  </tabs-panel-sk>
  <example-element active></example-element>
</body>
```

Now restart the dev server and see the updated page:

    $ make serve

## Why is this better?

Web frameworks usually make all these choices for you, you don’t
get to choose, even if you don’t need the functionality. For example, state
managament might not be needed, why are you 'paying' for it, where 'paying'
means learning about that aspect of the web framework, and possibly even
having to serve the code that implements state managment even if you never
use it. With a la carte development you only include what you use.

An extra benefit comes when it is time to upgrade. How much time
have you lost with massive upgrades from v1 to v2 of a web framework?
With 'a la carte' developement the upgrades don’t have to be monolithic.
I.e. if you've chosen a templating library and want to upgrade to
the next version you only need to update your templates, and not have to
touch every aspect of your application.

Finally, 'a la carte' web development provides no "model" but the browser. Of
all the things that frameworks provide, "model" is the most problematic.
Instead of just using the browser as it is, many frameworks have their own
model of the browser, how DOM works, how events work, etc. [I have gone into depth on the issues previously](https://bitworking.org/news/2014/05/zero_framework_manifesto), but
they can be summarized as lost effort (learning something that doesn’t
translate) and a barrier to reuse. What should replace it? Just use the
browser, it already has a [model for how to combine elements together](https://bitworking.org/news/2015/03/Six_Places), and now with custom
elements v1 gives you the ability to create your own elements, you have all you
need.

## Let a thousand flowers bloom

One of the most important aspects of 'a la carte' web developement is that it
decouples all the components, allowing them to evolve and adapt to user needs
on a much faster cycle than the normal web framework release cycle allows.
Just because we've published [pulito](https://www.npmjs.com/package/pulito) and [skia-elements](https://www.npmjs.com/package/skia-elements) doesn't mean we believe
they are the best solutions. I'd love to have a slew of options to choose from
for tooling, base element sets, templating, and state management. I’d like to
see Rollup based tools that take the place of [pulito](https://www.npmjs.com/package/pulito), and a whole swarm of
"neat" custom elements sets with varying levels of customizability and breadth.

<a href="https://brid.gy/publish/twitter"></a>

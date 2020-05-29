---
title: Looking back on five years of web components
date: 2019-07-27T12:00:00-04:00
tags:
  - standards
  - web components
---

Over 5 years ago I wrote
[No more JS frameworks](https://bitworking.org/news/2014/05/zero_framework_manifesto)
and just recently Jon Udell asked for an update.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">It&#39;s almost 4
years since <a
href="https://twitter.com/bitworking?ref_src=twsrc%5Etfw">@bitworking</a>
said: &quot;Stop using JS frameworks, start writing reusable,
orthogonally-composable units of HTML+CSS+JS.&quot; <br><br>I&#39;m curious,
Joe, about what you&#39;ve since learned, thought about, and done with the
idea.<a href="https://t.co/zdKjEZfIe3">https://t.co/zdKjEZfIe3</a></p>&mdash;
Jon Udell (@judell) <a
href="https://twitter.com/judell/status/1151608248316788736?ref_src=twsrc%5Etfw">July
17, 2019</a></blockquote> <script async
src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

I have been blogging bits and pieces over the years but Jon's query has given
me a good excuse to roll all of that up into a single document.

For the last five years me and my team have been using web components to build
our web UIs. At the time I wrote the Zero Framework Manifesto we moved all of our
development over to [Polymer](https://www.polymer-project.org/).

## Why Polymer?

We started with Polymer 0.5 as it was the closest thing to web components that
was available. At the time I wrote the Zero Framework Manifest all of the
specifications that made up web components were still just proposed standards
and only Chrome had implemented any of them natively. We closely followed
Polymer, migrating all of our apps to Polymer 0.8 and finally to Polymer 1.0
when it was released. This gave us a good taste for what building web
components was like and verified that building HTML elements was a productive
way to do web development.

## How

One of the questions that comes up regularly when talking about [zero frameworks](http://bitworking.org/news/2014/05/zero_framework_manifesto)
is how can you expect to stitch together an application without a framework? The
short answer is 'the same way you stitch together native elements', but I think
it's interesting and instructional to look at those ways of stitching elements
together individually.

There are six surfaces, or points of contact, between elements, that you can
use when stitching elements together, whether they are native or custom
elements.

Before we go further a couple notes on terminology and scope. For
scope, realize that we are only talking about DOM, we aren't talking about
composing JS modules or strategies for composing CSS. For the terminology
clarification, when talking about DOM I'm referring to the DOM
Interface for an element, not the element markup. Note that there is a
subtle difference between the markup element and the DOM Interface to such
an element.

For example, `<img data-foo="5" src="https://example.com/image.png"/>` may be
the markup for an image. The corresponding DOM Interface has an attribute of
src with a value of `https://example.com/image.png` but the corresponding DOM
Interface doesn't have a `data-foo` attribute, instead all data-\* attributes
are available via the dataset attribute on the DOM Interface. In the
terminology of the [WhatWG Living Standard](https://html.spec.whatwg.org/multipage/infrastructure.html#terminology),
this is the distinction between content attributes vs IDL
attributes, and I'll only be referring to IDL attributes.

With the preliminaries out of the way let's get into the six surfaces
that can be used to stitch together an application.

### Attributes and Methods

The first two surfaces, and probably the most obvious, are attributes and
methods. If you are interacting with an element it's usually either reading and
writing attribute values:

```javascript
element.children;
```

or calling element methods:

```
document.querySelector('#foo');
```

Technically these are the same thing, as they are both just properties with
different types. Native elements have their set of defined attributes and
methods, and depending on which element a custom element is derived from it
will also have that base element's attributes and methods along with the
custom ones it defines.

### Events

The next two surface are events. Events are actually two surfaces because an
element can listen for events,

```
ele.addEventListener(‘some-event’, function(e) { /* */ });
```

and an element can dispatch its own events:

```
var e = new CustomEvent(‘some-event’, {details: details});
this.dispatchEvent(e);
```

### DOM Position

The final two surfaces are position in the DOM tree, and again I'm
counting this as two surfaces because each element has a parent and can be
a parent to another element. Yeah, an element has siblings too, but that
would bring the total count of surfaces to seven and ruin my nice round
even six.

```html
<button>
  <img src="" />
</button>
```

### Combinations are powerful

Let's look at a relatively simple but powerful example, the 'sort-stuff'
element. This is a custom element that allows the user to sort elements. All
children of 'sort-stuff' with an attribute of 'data-key' are used for sorting
the children of the element pointed to by the sort-stuff's 'target' attribute.
See below for an example usage:

```html
<sort-stuff target="#sortable">
  <button data-key="one">Sort on One</button>
  <button data-key="two">Sort on Two</button>
</sort-stuff>
<ul id="sortable">
  <li data-one="c" data-two="x">Item 3</li>
  <li data-one="a" data-two="z">Item 1</li>
  <li data-one="d" data-two="w">Item 4</li>
  <li data-one="b" data-two="y">Item 2</li>
  <li data-one="e" data-two="v">Item 5</li>
</ul>
```

If the user presses the "Sort on One" button then the children of #sortable
are sorted in alphabetical order of their data-one attributes. If the user
presses the "Sort on Two" button then the children of #sortable are sorted in
alphabetical order of their data-two attributes.

Here is the definition of the 'sort-stuff' element:

<pre markdown="0" id="viewcode"></pre>

And here is a running example of the code above:

<style type="text/css" media="screen">
  sort-stuff button {
    padding: 0.5em;
  }
</style>

<sort-stuff target="sortable">
  <button data-key="one">Sort on One</button>
  <button data-key="two">Sort on Two</button>
</sort-stuff>
<ul id="sortable">
  <li data-one="c" data-two="x">Item 3</li>
  <li data-one="a" data-two="z">Item 1</li>
  <li data-one="d" data-two="w">Item 4</li>
  <li data-one="b" data-two="y">Item 2</li>
  <li data-one="e" data-two="v">Item 5</li>
</ul>

<script src="/js/custom-elements.min.js" type="text/javascript" charset="utf-8"></script>
<script markdown="0" id="code" type="text/javascript" charset="utf-8">
window.customElements.define('sort-stuff', class extends HTMLElement {
  connectedCallback() {
    Array.from(this.querySelectorAll('[data-key]')).forEach(
      ele => ele.addEventListener('click', this)
    );
  }

  handleEvent(e) {
    let target = document.getElementById(this.getAttribute('target'));
    let elements = [];
    let children = target.children;
    for (let i=0; i<children.length; i++) {
      elements.push({
        value: children[i].dataset[e.target.dataset.key],
        node: children[i],
      });
    }
    elements.sort((x, y) => (x.value == y.value ? 0 : (x.value > y.value ? 1 : -1)));
    elements.forEach(function(i) {
      target.appendChild(i.node);
    });
  }
});
</script>

<script type="text/javascript" charset="utf-8">
  document.getElementById('viewcode').textContent = document.getElementById('code').textContent;
</script>

Note the surfaces that were used in constructing this functionality:

<ol>
  <li>sort-stuff has an <strong>attribute</strong> 'target' that selects the element to sort.</li>
  <li>The target <strong>children</strong> have data <strong>attributes</strong> that elements are sorted on.</li>
  <li>sort-stuff registers for 'click' events from its <strong>children</strong>.</li>
  <li>sort-stuff <strong>children</strong> have data <strong>attributes</strong> that determine how the target children will be sorted.</li>
</ol>

In addition you could imagine adding a custom event 'sorted' that
'sort-stuff' could generate each time it sorts.

## Why not Polymer?

But after having used Polymer for so many years we looked at the direction of
Polymer 2.0 and now 3.0 and decided that may not be the direction we want to
take.

There are a few reasons we moved away from Polymer. Polymer started out and
continues to be a platform for experimentation with proposed standards, which
is great, as they are able to give concrete feedback to standards committees
and allow people to see how those proposed standards could be used in
development. The downside to the approach of adopting nascent standards is
that sometimes those things don't become standards. For example, HTML Imports
was a part of Polymer 1.0 that had a major impact on how you wrote your
elements, and when [HTML Imports failed to become a
standard](https://hacks.mozilla.org/2015/06/the-state-of-web-components/) you
had a choice of either a major migration to ES modules or to carry around a
polyfill for HTML Imports for the remainder of that web app's life. You can
see the same thing happening today with Polymer 3.0 and [CSS
mixins](https://polymer-library.polymer-project.org/3.0/docs/devguide/custom-css-properties#use-custom-css-mixins).

There are also implementation decisions I don't completely agree with in
Polymer, for example, the default use of [Shadow
DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM).
Shadow DOM allows for the encapsulation of the children of a custom element so
they don't participate in things like `querySelector()` and normal CSS
styling. But there are several problems with that, the first is that when
using Shadow DOM you lose the ability to do global styling changes. If you
suddenly decide to add a "dark mode" to your app you will need to go and
modify each element's CSS. It was also supposed to be faster, but since each
element contains a copy of the CSS there are [performance
implications](https://bitworking.org/news/2018/02/shadow-dom-and-css), though
[there is work underway to address
that](https://github.com/w3c/webcomponents/issues/468). Shadow DOM seems like
a solution searching for a problem, and Polymer defaults to using Shadow DOM
while offering a way to opt out and use Light DOM for your elements; I believe
the default should lie in the other direction.

Finally Polymer's data binding has some mis-features. It offers two-way data
binding which is never a good idea, every instance of two-way data binding is
just a bug waiting to happen. The data binding also has a lot of magic to it,
in theory you just update your model and Polymer will re-render your template
at some point in the future with the updated values. The "at some point in the
future" is because updates happen in an async fashion, which in theory allows
the updates to be more efficient by batching the updates, but the reality is
that you spend a lot of development time updating your model, not getting
updated DOM, and scratching your head until you remember to either call a
function which forces a synchronous render, or that you updated a deep part of
your model and Polymer can't observe that change so you need to update your
code to use the `set()` method where you give the path to the part of the
model you just updated. The async rendering and observing of data is fine for
simple applications, but for more complex applications leads to wasted
developer time debugging situations where a simpler data binding model would
suffice.

It is interesting to note that the Polymer team also produces the
[lit-html](https://lit-html.polymer-project.org/) library which is simply a
library for templating that uses template literals and HTML Templates to make
the rendering more efficient, and it has none of the issues I just pointed
out in Polymer.

## What comes after Polymer?

This is where I started with a very concrete and data driven minimalist
approach, first determining what base elements we really needed and then what
library features we would need as we built up those elements, and finally what
features we need as we build full fledged apps from those base elements. I was
completely open to the idea that maybe I was just being naive about the need
for async render or Shadow DOM and I'd let the process of building real world
applications inform what features were really needed.

The first step was to determine which base elements we really needed. The
library of iron-\* and paper-\* elements that Polymer provides is large and the
idea of writing our own version of each was formidable, so instead I looked
back over the previous years of code we'd written in Polymer to determine
which elements we really did need. If we'd started this process today I would
probably just have gone with [Elix](https://component.kitchen/elix) or another
pure web components library of elements, but none of them existed at the time
we started this process.

The first thing I did was scan each project and record every Polymer element
used in every project. If I'm going to replace Polymer at least I should know
how many elements I'm signing up to rewrite. That initial list was surpising
in a couple of ways, the first was how short the list was:

<style>
table{
  border-collapse: collapse;
  border-spacing: 0;
  border:2px solid gray;
  margin: 1em;
}

th, td {
  padding: 0.2em;
  border:2px solid gray;
}
</style>

| Polymer/Iron elements Used |
| -------------------------- |
| iron-ajax                  |
| iron-autogrow-textarea     |
| iron-collapse              |
| iron-flex-layout           |
| iron-icon                  |
| iron-pages                 |
| iron-resizable-behavior    |
| iron-scroll-threshold      |
| iron-selector              |
| paper-autocomplete         |
| paper-button               |
| paper-checkbox             |
| paper-dialog               |
| paper-dialog-scrollable    |
| paper-drawer-panel         |
| paper-dropdown-menu        |
| paper-fab                  |
| paper-header-panel         |
| paper-icon-button          |
| paper-input                |
| paper-item                 |
| paper-listbox              |
| paper-menu                 |
| paper-menu-button          |
| paper-radio-button         |
| paper-radio-group          |
| paper-spinner              |
| paper-tabs                 |
| paper-toast                |
| paper-toggle-button        |
| paper-toolbar              |
| paper-tooltip              |

After four years of development I expected the list to be much larger.

The second surpise was how many of the elements in that list really shouldn't
be elements at all. For example, some could be replaced with native elements
with some better styling, for example `button` for `paper-button`.
Alternatively some could be replaced with CSS or a non-element solution, such
as `iron-ajax`, which shouldn't be an element at all and should be replaced
with the `fetch()` function. After doing that analysis the number of elements
actually needed to be re-implemented from Polymer fell to a very small number.

In the table below the 'Native' column is for places where we could use native
elements and just have a good default styling for them. The 'Use Instead'
column is what we could use in place of a custom element. Here you will notice
a large number of elements that can be replaced with CSS. Finally the last
column, 'Replacement Element', is the name of the element we made to replace
the Polymer element:

| Polymer                 | Native        | Use Instead             | Replacement Element       |
| ----------------------- | ------------- | ----------------------- | ------------------------- |
| iron-ajax               |               | Use fetch()             |                           |
| iron-collapse           |               |                         | collapse-sk               |
| iron-flex-layout        |               | Use CSS Flexbox/Grid    |                           |
| iron-icon               |               |                         | \*-icon-sk                |
| iron-pages              |               |                         | tabs-panel-sk             |
| iron-resizable-behavior |               | Use CSS Flexbox/Grid    |                           |
| iron-scroll-threshold   |               | Shouldn't be an element |                           |
| iron-selector           |               |                         | select-sk/multi-select-sk |
| paper-autocomplete      |               | No replacement yet.     |                           |
| paper-button            | button        |                         |                           |
| paper-checkbox          |               |                         | checkbox-sk               |
| paper-dialog            |               |                         | dialog-sk                 |
| paper-dialog-scrollable |               | Use CSS                 |                           |
| paper-drawer-panel      |               | Use CSS Flexbox/Grid    |                           |
| paper-dropdown-menu     |               |                         | nav-sk                    |
| paper-fab               | button        |                         |                           |
| paper-header-panel      |               | Use CSS Flexbox/Grid    |                           |
| paper-icon-button       | button        |                         | button + \*-icon-sk       |
| paper-input             | input         |                         |                           |
| paper-item              |               |                         | nav-sk                    |
| paper-listbox           | option/select |                         |                           |
| paper-menu              |               |                         | nav-sk                    |
| paper-menu-button       |               |                         | nav-sk                    |
| paper-radio-button      |               |                         | radio-sk                  |
| paper-radio-group       | \*\*          |                         |                           |
| paper-spinner           |               |                         | spinner-sk                |
| paper-tabs              |               |                         | tabs-sk                   |
| paper-toast             |               |                         | toast-sk                  |
| paper-toggle-button     |               |                         | checkbox-sk               |
| paper-toolbar           |               | Use CSS Flexbox/Grid    |                           |
| paper-tooltip           |               | Use title attribute     |                           |

\*\* - For radio-sk elements just set a common name like you would for a
native radio button.

That set of minimal custom elements has now been launched as
[elements-sk](https://www.npmjs.com/package/elements-sk).

Now that we have our base list of elements let's think about the rest of the
tools and techniques we are going to need.

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
Let's break each of those aspects of a framework out into their own standalone
thing and then we can pick and choose from the various implementations when we
start developing an application. This style of developement we call "a la
carte" web development.

Instead of picking a monolithic solution like a web framework, you just pick
the pieces you need. Below I outline specific criteria that need to be met for
some components to participate in "a la carte" web development.

## A la carte

"A la carte" web development does away with the framework, and says just
use the browser for the model, and the rest of the pieces you pick and choose
the ones that work for you. In a la carte development each bullet point is a
separate piece of software:

_A la carte_

Tooling and structure
: Defines a directory structure for how a project is put together and provides tooling such as
JS transpiling, CSS prefixing, etc. for projects that conform to that directory structure.
Expects ES modules with the extension that webpack, rollup, and similar tools presume, i.e.
allow importing other types of files, see [webpack loaders](https://webpack.js.org/concepts/#loaders).

Elements
: A library of v1 custom elements in ES6 modules. Note that these elements must be provided in ES6
modules with the extension that webpack, rollup, and similar tools presume, i.e.
allow importing other types of files, see [webpack loaders](https://webpack.js.org/concepts/#loaders).
The elements should also be ["neat"](https://bitworking.org/news/2018/02/custom-elements-neat), i.e.
just HTML, CSS, and JS.

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

Such code will natively run in browsers that support custom elements v1. To
get it to run in a wider range of browsers you will need to add polyfills and,
depending on the target browser version, compile the JS back to an older
version of ES, and run a prefixer on the CSS. The wider the target set of
browsers and the older the versions you are targeting the more processing you
will need to do, but the original code doesn't need to change, and all those
extra processing steps are only incurred by projects that need it.

## Concrete

So now that we have our development system we've started to publish some of those pieces.

We published [pulito](https://www.npmjs.com/package/pulito), a stake in the ground for what a "tooling and
structure" component looks like. You will note that it isn't very complex, nothing more than an opinionated
webpack config file. Similarly we published our set of "neat" custom elements [elements-sk](https://www.npmjs.com/package/elements-sk).

Our current stack looks like:

Tooling and structure
: [pulito](https://www.npmjs.com/package/pulito)

Elements
: [elements-sk](https://www.npmjs.com/package/elements-sk)

Templating
: [lit-html](https://www.npmjs.com/package/lit-html)

We have used Redux in an experimental app that never shipped and haven’t needed
any state management libraries in the other applications we’ve ported over, so
our 'state management' library is still an open question.

## Example

What is like to use this stack? Let's start from an empty directory
and start building a web app:

    $ npm init
    $ npm add pulito

We are starting from scratch so use the project skeleton that [pulito](https://www.npmjs.com/package/pulito) provides:

    $ unzip node_modules/pulito/skeleton.zip
    $ npm

We can now run the dev server and see our running skeleton application:

    $ make serve

Now let's add in [elements-sk](https://www.npmjs.com/package/elements-sk) and add a set of tabs to the UI.

    $ npm add elements-sk

Now add imports to `pages/index.js` to bring in the elements we need:

```javascript
import 'elements-sk/tabs-sk';
import 'elements-sk/tabs-panel-sk';
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
use it. With "a la carte" development you only include what you use.

An extra benefit comes when it is time to upgrade. How much time
have you lost with massive upgrades from v1 to v2 of a web framework?
With 'a la carte' developement the upgrades don’t have to be monolithic.
I.e. if you've chosen a templating library and want to upgrade to
the next version you only need to update your templates, and not have to
touch every aspect of your application.

Finally, 'a la carte' web development provides no "model" but the browser. Of
all the things that frameworks provide, "model" is the most problematic.
Instead of just using the browser as it is, many frameworks have their own
model of the browser, how DOM works, how events work, etc. [I have gone into
depth on the issues
previously](https://bitworking.org/news/2014/05/zero_framework_manifesto), but
they can be summarized as lost effort (learning something that doesn’t
translate) and a barrier to reuse. What should replace it? Just use the
browser, it already has a [model for how to combine elements
together](https://bitworking.org/news/2015/03/Six_Places), and now with custom
elements v1 gives you the ability to create your own elements, you have all
you need.

One of the most important aspects of 'a la carte' web developement is that it
decouples all the components, allowing them to evolve and adapt to user needs
on a much faster cycle than the normal web framework release cycle allows.
Just because we've published [pulito](https://www.npmjs.com/package/pulito)
and [elements-sk](https://www.npmjs.com/package/elements-sk) doesn't mean we
believe they are the best solutions. I'd love to have a slew of options to
choose from for tooling, base element sets, templating, and state management.
I’d like to see Rollup based tools that take the place of
[pulito](https://www.npmjs.com/package/pulito), and a whole swarm of "neat"
custom elements sets with varying levels of customizability and breadth.

## What we've learned

We continue to learn as we build larger applications.

lit-html is very fast and all the applications we've ported over have been
smaller and faster after the port. It is rather pleasant to call the
`render()` function and know that the element has been rendered and not
getting tripped up by async rendering. We haven't found the need for async
rendering either, but that's not surprising. Let's think about cases where
async rendering would make a big difference, i.e. where it would be a big
performance difference to batch up renders and do them asynchronously. This
would have to be an element with a large number of properties and each change
of the property would change the DOM expressed and thus would require a large
number of calls to `render()`. But in all the development we've done that
situation has never arisen, elements always have a small number of attributes
and properties. If an element takes in a large amount of data to display
that's usually done by passing in a small number of complex object as
properties on the element and that results in a small number of renders.

We haven't found the need for Shadow DOM. In fact, I've come to think of the
Light DOM children of elements as part of their public API that goes along
with the attributes, properties, and events that make up the 'normal'
programming surface of an element.

We've also learned that there's a difference between creating base elements
and higher level elements as you build up your application. You are not
creating bullet-proof re-usable elements at every step of development; the
same level of detail and re-usability aren't needed as you move up the stack.
If an element looks like it could be re-used across applications then we may
tighten up the surface of the element and add more options to cover more use
cases, but that's done on an as-needed basis, not for every element. Just
because you are using the web component APIs to build an application doesn't
mean that every element you build needs to be as general purpose and bullet
proof as low level elements. You can use HTML Templates without using any
other web component technology. Same for template literals, and for each of
the separate technologies that make up the web components group of APIs.

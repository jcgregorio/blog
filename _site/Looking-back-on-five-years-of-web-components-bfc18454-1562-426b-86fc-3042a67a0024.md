# Looking back on five years of web components

[https://twitter.com/judell/status/1151608248316788736](https://twitter.com/judell/status/1151608248316788736)

Over 5 years ago I wrote [https://bitworking.org/news/2014/05/zero_framework_manifesto](https://bitworking.org/news/2014/05/zero_framework_manifesto) and just recently Jon Udell asked for an update. I have been blogging bits and pieces over the years but Jon's query has given me a good excuse to roll all of that up into a single document.

For the last five years me and my team have been using web components to build our web UIs.

At the time I wrote the Zero Framework Manifesto we moved all of our development over to Polymer.

## Why Polymer?

 We started with Polymer 0.5 as it was the closest thing to web components that was available. At the time I write the Zero Framework Manifest all of the specifications that made up web components were still just proposed standards and hadn't made it to becoming standards and only Chrome had implemented any of them natively. We closely followed Polymer, migrating all of our apps to Polymer 0.8 and finally to Polymer 1.0 when it was released. This gave us a good taste for what building web components was like and verified that building HTML elements was a productive way to do web development. But after having used Polymer for so many years we looked at the direction of Polymer 2.0 and now 3.0 and decided that may not be the direction we want to take.

## Why not Polymer?

There are a few reasons we moved away from Polymer. Polymer started out and continues to be a platform for experimentation with proposed standards, which is great as they are able to give concrete feedback to standards committees and allow people to see how those proposed standards could be used in development. The downside to the approach of adopting nascent standards is that sometimes those things don't become standards. For example, HTML Imports was a part of Polymer 1.0 that had a major impact on how you wrote your elements, and when HTML Imports failed to become a standard you had a choice of either a major migration to ES modules or to carry around a polyfill for HTML Imports for the remainder of that web apps life. You can see the same thing happening today with Polymer 3.0 and [CSS mixins](https://polymer-library.polymer-project.org/3.0/docs/devguide/custom-css-properties#use-custom-css-mixins).

There are also implementation decisions I don't completely agree with in Polymer, for example, the default use of Shadow DOM. Shadow DOM allows for the encapsulation of the children of a custom element so they don't participate in things like querySelector() and normal CSS styling. But there are several problems with that, the first is that when using Shadow DOM you lose the ability to do global styling changes. If you suddenly decide to add a 'dark mode' to you add you will need to go and modify each element's CSS. It was also supposed to be faster, but since each element contains a copy of the CSS there are performance implications, though there is work underway to address that. Shadow DOM seems like a solution searching for a problem, and Polymer defaults to using Shadow DOM but offers a way to opt out and use Light DOM for your elements, when I believe the default should lie in the other direction.

Finally Polymer's data binding has some mis-features. It offers two-way data binding which is never a good idea, every instance of {{}} is just a bug waiting to happen. The data binding also has a lot of magic to it, in theory you just update your model and Polymer will re-render your template at some point in the future with the updated values. The "at some point in the future" is because updates happen in an async fashion, which in theory allows the updates to be more efficient by batching the updates, but the reality is that you spend a lot of time updating your model, not getting updated DOM, and scratching your head until you remember to either call a function which forces a synchronous render, or that you updated a deep part of your model and Polymer can't observe that change so you need to update your code to use the set() method where you give the path to the part of the model you just updated.

It is interesting to note that the Polymer team also produces the lit-html library which is simply a library for templating that uses template literals and HTML Templates to make the rendering more efficient that has none of the issues I just pointed out in Polymer.

## What comes after Polymer?

So if we are going to move away from Polymer, what should replace it? This is where I started with a very concrete and data driven minimalist approach, first determining what base elements we really needed and then what library features we would need as we built up those elements, and finally what features we need as we build full fledged apps from those base elements. Maybe I was just being naive about the need for async render or Shadow DOM and I'd let the process inform what features were really needed.

The first step was to determine which base elements we'd really need. The library of iron-* and paper-* elements that Polymer provides is large and the idea of writing our own version of each was formidable, so instead I looked back over the previous years of code we'd written in Polymer to determine which elements we really did need. If we'd started this process today I would probably just have gone with Elix or another pure web components library of elements, but none of them existed at the time we started this process. As it turned out the list of elements we needed is a very small subset of the Polymer element library.

=⇒ Insert elements blog post here

Now that we have our base list of elements let's think about the rest of the tools and techniques we are going to need.

=⇒ Insert A La Carte blog post here.

## Continuing Education

We continue to learn as build larger applications, for example, we now have a base class for elements that has support for lit-html rendering, and avoids an edge case with web components receiving attributeChangedCallback()s before connectedCallback() is called.

It is rather pleasant to call this._render() and know that the element has been rendered and not getting tripped up by async rendering.

We haven't found the need for Shadow DOM. In fact, I've come to think of the Light DOM children of elements as part of their public API that goes along with the attributes, properties, and events that make up the 'normal' element surface.

Haven't found the need for async rendering either, but that's not surprising. Let's think about cases where async rendering would make a big difference, i.e. where it would be a big performance difference to batch up renders and do them asynchronously. This would have to be an element with a large number of properties and each change of the property would change the DOM expressed and thus would require a large number of calls to render(). But in all the development we've done that situation has never arisen, elements always have a small number of attributes and properties. If an element takes in a large amount of data to display that's usually done by passing in a complex Object as a property on the element and that results in just a single render.

You are not creating bullet-proof re-usable elements at every step of development. The same level of detail and re-usability aren't needed. If an element looks like it could be re-used across elements then we may tighten up the surface of the element and add more options to cover more use cases, but that's done on an as-needed basis, not for every element. Just because you are using the web component APIs to build an application doesn't mean that every element you build needs to be as general purpose and bullet proof as low level elements. You can use HTML Template without using any other web component technology. Same for template literals, and for each of the separate technologies that make up the web components group of APIs.
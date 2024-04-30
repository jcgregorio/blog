---
title: "Custom Element Naming"
date: 2024-04-30T09:40:37-04:00
tags:
  - standards
  - web components
---

In [My approach to HTML web components](https://adactio.com/journal/21078) Jeremy Keith goes into a naming convention for both web components and their attributes.

While I don't have any opinions on attribute naming, I do have a strong opinion on element names, and that's if you decide to namespace your elements it should be done using a post-fix and not a pre-fix.

As an example, all the elements we've build in Skia Infra are post-fixed with `-sk`:

https://jsdoc.skia.org/theme/theme-chooser-sk-demo.html [[Source](https://skia.googlesource.com/buildbot/+/refs/heads/main/elements-sk/modules?autodive=0%2F/)]

        checkbox-sk
        collapse-sk
        error-toast-sk
        icons-demo-sk
        multi-select-sk
        nav-button-sk
        nav-links-sk
        radio-sk
        select-sk
        spinner-sk
        styles
        tabs-panel-sk
        tabs-sk
        toast-sk

This is in contrast to prefixing, which makes the names much harder to read, such as all the `iron-` elements
in Polymer:

https://www.webcomponents.org/collection/PolymerElements/iron-elements

        iron-image
        iron-selector
        iron-localstorage
        iron-label
        iron-collapse
        iron-checked-element-behavior
        iron-demo-helpers
        iron-scroll-target-behavior
        iron-a11y-keys
        iron-form-element-behavior
        iron-meta
        iron-media-query
        iron-validatable-behavior
        iron-pages
        iron-jsonp-library
        iron-ajax
        iron-list
        iron-doc-viewer

To me the former are much easier to read, while the latter just reads like "iron iron iron iron" when used on page.

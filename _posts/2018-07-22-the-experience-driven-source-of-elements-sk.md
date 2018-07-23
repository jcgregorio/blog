---
layout: post
title: The experience driven source of the elements-sk set of custom elements.
---

Last August, as my team was pondering moving away from
[Polymer](https://www.polymer-project.org/) and creating our own set of
[neat](https://bitworking.org/news/2018/02/custom-elements-neat) vanilla js
[custom
elements](https://developers.google.com/web/fundamentals/web-components/customelements),
I decided to take a data driven stab at deciding is this was a viable plan. My
team has been building web applications for over four years using Polymer  and
that corpus of code could be used to guide the decision. The first thing I did
was scan each project and record every Polymer or Iron element used in every
project. If I'm going to replace Polymer at least I should know how many
elements I'm signing up to rewrite. That initial list was surpising in a
couple of ways, the first was how short the list was:

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
|----------------------------|
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

| Polymer                    | Native        | Use Instead              | Replacement Element       |
|----------------------------|---------------|--------------------------|---------------------------|
| iron-ajax                  |               | Use fetch()              |                           |
| iron-collapse              |               |                          |collapse-sk                |
| iron-flex-layout           |               | Use CSS Flexbox/Grid     |                           |
| iron-icon                  |               |                          |\*-icon-sk                 |
| iron-pages                 |               |                          |tabs-panel-sk              |
| iron-resizable-behavior    |               | Use CSS Flexbox/Grid     |                           |
| iron-scroll-threshold      |               | Shouldn't be an element  |                           |
| iron-selector              |               |                          |select-sk/multi-select-sk  |
| paper-autocomplete         |               | No replacement yet.      |                           |
| paper-button               | button        |                          |                           |
| paper-checkbox             |               |                          |checkbox-sk                |
| paper-dialog               |               |                          |dialog-sk                  |
| paper-dialog-scrollable    |               | Use CSS                  |                           |
| paper-drawer-panel         |               | Use CSS Flexbox/Grid     |                           |
| paper-dropdown-menu        |               |                          |nav-sk                     |
| paper-fab                  | button        |                          |                           |
| paper-header-panel         |               | Use CSS Flexbox/Grid     |                           |
| paper-icon-button          | button        |                          |icon-sk                    |
| paper-input                | input         |                          |                           |
| paper-item                 |               |                          |nav-sk                     |
| paper-listbox              | option/select |                          |                           |
| paper-menu                 |               |                          |nav-sk                     |
| paper-menu-button          |               |                          |nav-sk                     |
| paper-radio-button         |               |                          |radio-sk                   |
| paper-radio-group          |               |                          |                           |
| paper-spinner              |               |                          |spinner-sk                 |
| paper-tabs                 |               |                          |tabs-sk                    |
| paper-toast                |               |                          |toast-sk                   |
| paper-toggle-button        |               |                          |checkbox-sk                |
| paper-toolbar              |               | Use CSS Flexbox/Grid     |                           |
| paper-tooltip              |               | Use title attribute      |                           |

That set of minimal custom elements has now been launced as
[elements-sk](https://www.npmjs.com/package/elements-sk). While the number of
elements is small, it is driven by four years of development using custom
elements, and just might be a good set of elements for your development too.
If anyone has done a similar analysis I'd love to hear about it, please let me
know in the comments.

<a href="https://brid.gy/publish/twitter"></a>

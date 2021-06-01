---
title: 'Islands of Data'
date: 2021-05-31T11:11:48-04:00
---

This demo of a shopping list in the 1968 "Mother of All Demos" with Doug
Engelbart & Team is both amazing and depressing all at the same time:

<iframe width="560" height="315" src="https://www.youtube.com/embed/M5PgQS3ZBWA?start=509" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

We have at least progressed to the point where assembling such an application is
a training-wheels level exercise used to introduce different web frameworks. For
example, here's a tutorial from Mozilla on how to write a TODO list application
in four different frameworks:
[Introduction to client-side frameworks](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/Introduction)

That is the amazing part.

The depressing part is that in every single one of those applications you will
end up building a data island. The TODO list is locked inside the database
backing those applications.

- How do you export and import TODO lists?
- How would you even begin to transfer TODO lists from the Vue implementation to
  the Ember implementation?
- How could you edit, with permissions, a React TODO list from someone else in
  your own Angular TODO list editor?
- Why can't I upload my food shopping list to my grocery store and have all the
  items on it delivered?
- Why can't my grocery store sort the shopping list by the aisles in the store?

You can't do any of the things I list above because our focus today is on "apps"
and not on standard formats and protocols, and until that changes we will
continue to make islands of data, and we'll all be poorer for it.

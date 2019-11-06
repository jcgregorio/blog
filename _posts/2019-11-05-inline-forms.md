---
layout: post
title: Inline Forms
---

Based on a [Twitter
discussion](https://twitter.com/bitworking/status/1190822233528242182) about
optimizing the performance of web apps, I implemented a very crude polyfill for
an idea I recently had.

HTML forms support multiple `target` values, i.e. where should the result of
submitting the form be displayed, but there is no value for of `target` for
inline, that is, you submit the form and instead of the whole page refreshing
the server returns HTML that takes the place of the Form contents.

The idea is that there would be a new target type for HTML Forms, an attribute
of `target=_inline` would mean the that Form would be processed by the server
and the contents of the Form would be replaced with the HTML returned by the
server. That is, on submit the form values would be sent to the server, either
POST or GET, and the response should be HTML that the browser will simply
`.innerHTML` on the form that was submitted.

Code: https://github.com/jcgregorio/inline-form

Online Demo: https://inline-form-nuau7zlm6q-uc.a.run.app/

Also huge props to the team behind the [Cloud Run
Button](https://cloud.google.com/blog/products/serverless/introducing-cloud-run-button-click-to-deploy-your-git-repos-to-google-cloud)
which made this insanely simple to deploy.

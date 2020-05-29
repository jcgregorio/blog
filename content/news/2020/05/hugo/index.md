---
title: 'Hugo'
date: 2020-05-28T22:00:59-04:00
---

This blog has just migrated from [Jekyll](https://jekyllrb.com/) to [Hugo](https://gohugo.io/).

Why? Having programmed in Go for six years now I'm very comfortable with Go
templates, which are the basis of Hugo templating. Also, [speed is a
feature](https://www.thinkwithgoogle.com/marketing-resources/the-google-gospel-of-speed-urs-hoelzle/),
and `hugo -D` can rebuild this entire static site, all 2,700 pages, in under 2
seconds.

And while I am happy with Hugo now that I've gotten up to speed, the
introductory documentation is missing a hugely important bit of trivia about
Hugo configuration files and the templates, which is that case is ignored.

That is, if you have a configuration file that looks like this:

        baseURL = "https://example.org/"
        languageCode = "en-us"
        title = "My New Hugo Site"
        theme = "ananke"

You will later look at a template and see:

         {{ .Title | default .Site.Title }}

Which may cause you to scratch your head. As far as I can tell, Hugo doesn't
care about case at all, so `.Site.Title` could just as easily be written
as `.site.title`, or `.SiTe.TiTlE`, and the same things goes for the config file,
where case also doesn't seem to matter:

        baseURL = "https://example.org/"
        languageCode = "en-us"
        TITLE = "My New Hugo Site"
        theme = "ananke"

will work just as well.

Another feature that I really like with Hugo is the simple post tagging functionality
that's built in, allowing me have a page of [categorized posts](/tags/). In the process
I went back and added tags to many, but not all, of my posts. The tags, along with the
[Related Content](https://gohugo.io/content-management/related/) functionality builds
easy navigation paths among related posts. My favorite of these was bringing together
all of my entries that have [visualizations](/tags/visualization/).

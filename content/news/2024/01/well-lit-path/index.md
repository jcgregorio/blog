---
title: "A Well-Lit Path for your software development team."
date: 2024-01-27T21:43:25-05:00
---

Remember LAMP? = Linux/Apache/MySQL/PHP? 

All the parts being open source was a primary reason LAMP this became popular.


you could pick these parts off a shelf, plug them together, and start building a working website.

it reduced choice, but also reduced project startup time and increased developer velocity

the ubiquity of LAMP meant that you could probably find answers to your questions on the web,
along with solutions to problems you ran into

That is, LAMP became a well-lit path for website development.

When building out your development stack, you need to provide as well-lit path for your team.

"well-lit path" in software development signifies a clear and easily navigable route that leads to effective and efficient development practices.

## attributes

reduces choice

decisions are already made for you, reducing cognitive load

Axiom: If all you have is a hammer, everything looks like a nail.

Corollary: Making all your problems look like nails makes tool selection easy.

there should be one way to do something

but that can be taken too far

you could demand everything be stored in an SQL database. But that ignores that some storage
might need to be for massive objects, or data that only needs to be retrieved infrequently, or
for whom slow retrieval is not a problem.

So you might provide two options for storage:
1. MySQL
2. Google Cloud Storage

you are still restricting choice, i.e. folks can go off and spin up Postgres or Spanner databases

nor can they start using Amazon's S3, or Google Cloud Firestore.

This allows you to build up common libraries and tooling, further accelerating development.


# Experiments
Another aspect of a well-lit path is the role of experimentation.

Like real, structured experiments

you, or another developer spots a new technology, for example, CockroachDB, that looks like it
could be a good replacement for 

Experiments are either totally temporary, or are reversible.


But doesn't this lead to a sclerotic development stack? Rigid and unresponsive, unable to adapt better technologies as they appear?

This is the paradox, in fact the opposite is true

Let's say you allow total freedom, a complete wild-west where every team is allowed to create their own development stack?
At first that might appear to be fast, because you reduce the coordination costs. 

But let's skip forward in time, five years has passed and some choices in the group are starting to look old
or say Material Design 5 comes out and everyone wants the UIs to have that same look and feel. Well, w/o a
common UI stack, let's say the teams chose React, or X, or Y. Then each team has to do the work to update
React, or X, or Y to get that MD5 look.

The same for shiny new technologies. Each team will have to do those experiments themselves, and no one else
can benefit from that work. 

 - Link to other people talking about Amazon's issues here.


# Wayfinding

## benefits

## objections

## observations


---
title: 'Creating a Date Column in Notion That Has a Default'
date: 2020-08-14T12:00:02-04:00
draft: true
---

I searched around for a while on how to create a Date column in
[Notion](https://notion.so) that defaulted to the current date and time but
could also be editable. I didn't find anything useful and eventually came up
with my own solution.

This requires three columns:

1.  The first column is the `Created` column which exists by default on tables.
1.  The second column is a Date column named `Override Date`. This will normally
    be empty unless you enter a value in the column.
1.  The last column, `Date`, is a computed column that uses the first two
    columns as its inputs.

The `Date` column uses the following formula:

        if(empty(prop("Override Date")), prop("Created"), prop("Override Date"))

That is, if the `Override Date` is empty then the value of the column is the `Created` date, otherwise its value comes from the `Override Date`.

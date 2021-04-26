---
title: 'Booleans'
date: 2021-04-25T16:23:42-04:00
---

I have come to consider boolean function arguments as a bit of an anti-pattern.

Consider the following function:

```golang
package hex

// ConvertFileToHEX write the hex representation of the src file
// to the dst file. If uppercase is true then write the HEX
// values in uppercase, otherwise write then in lowercase.
func ConvertFileToHEX(src, dst string, uppercase boolean) error {
...
}
```

This seems like a completely simple function that's easy to understand, but
that's when you are looking at the function definition, but most of the time you
won't be look at the function definition, instead you will be looking at that
function being called from code, i.e. when we go to use it. At this point we can
see the weakness of boolean arguments, the values of 'true' and 'false' don't
really have any useful meaning:

```golang
main() {
    ...
    //                       What does 'true' mean here? |
    //                                                   V
    err := hex.ConvertFileToHex("/foo", "/bar", true)
    if err != nil {
        ...
    }
    ...
}
```

To fix the problem I like to create a type and some constant values of that type
to replace the boolean. Let's rewrite our function to do that and replace the
boolean upper/lower case flag.

```golang
package hex

type HexCase int

const UppercaseHex HexCase = 1
const LowercaseHex HexCase = 2

// ConvertFileToHEX write the hex representation of the src
// file to the dst file. The hexCase value controls the case
// of the written HEX values.
func ConvertFileToHEX(src, dst string, hexCase HexCase) error {
...
}
```

The function definition isn't that different, but now the callsites of the
function are much easier to read:

```golang
main() {
    ...
    // I have a good idea what this parameter does: |
    //                                              V
    err := hex.ConvertFileToHex("/foo", "/bar", hex.UppercaseHex)
    if err != nil {
        ...
    }
    ...
}
```

I could even have made the type of `HexCase` to be a boolean, with
`UppercaseHex` defined as true and `LowercaseHex` defined as false, if you
actually care about the size of the underlying type. But really, the thing to
take away is when writing code you need to think of the ergonomics of that code,
and that includes what it will look like when it's called.

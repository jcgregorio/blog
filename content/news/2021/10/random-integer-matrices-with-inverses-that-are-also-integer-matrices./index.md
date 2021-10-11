---
title: 'Random Integer Matrices With Inverses That Are Also Integer Matrices'
date: 2021-10-10T23:05:42-04:00
---

I want to generate a random integer valued \\( n \times n \\) matrix \\( A \\)
whose inverse is also an integer valued matrix, i.e. how can I generate
[Unimodular matrices](https://en.wikipedia.org/wiki/Unimodular_matrix)?

The key is starting with an \\( n \times n \\) identity matrix \\( I \\), which
has a determinant of 1. Then you can apply row operations to \\( I \\) that keep
the determinant 1, i.e. by picking row operations that are expressible as
multiplication by a matrix that also has a determinant of 1 with integer
components.

The very simplest of these row operations is to add row \\( i \\) to row \\( j
\\) where \\( i \neq j \\):

$$ r_i = r_i + r_j $$

Such a row operation has determinant of 1 and all integer values, so the
resulting matrix after the operation still has a determinant of 1, and so it's
inverse also remains integer valued. You can actually add \\( N \\) times row
\\( i \\) to row \\( j \\) and still have a determinant of 1, it's the fact that
\\( i \neq j \\) that keeps the determinant 1.

Such row operations also have nice inverses. If the row operation that
represents:

$$ r_i = r_i + r_j $$

is denoted \\( R \\), then

$$ A=RI $$

and the inverse can be constructed by multiplying \\( I \\) on the right hand
side by \\(R^{-1}\\):

$$ A^{-1}=IR^{-1} $$

And in this case the inverse of our row operation \\( R \\) is to just subtract
column \\( j \\) from column \\( i \\).

If we create a series of such elementary row operations at random we can then
generate both \\( A \\) and \\( A^{-1} \\).

\\( A \\) : $$ A = R\_{m} ... R\_{2} R\_{1} I $$

\\( A^{-1} \\) : $$ A^{-1} = I R\_{1}^{-1} R\_{2}^{-1} ... R\_{m}^{-1} $$

Here is
[Go code](https://gist.github.com/jcgregorio/0c2028a7a27b814641e9f502ed8b8b32)
for an implementation:

<script src="https://gist.github.com/jcgregorio/0c2028a7a27b814641e9f502ed8b8b32.js"></script>

[Generating Invertible Matrices](https://people.math.carleton.ca/~kcheung/math/notes/MATH1107/wk06/06_generating_invertible_matrices.html)
was one of my first stopping points on getting all of this working.

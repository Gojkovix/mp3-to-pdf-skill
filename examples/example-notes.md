---
course: Calculus 1
chapter: 5
title: Derivatives and the chain rule
lecturer: Prof. Jane Smith
date: 2026-10-08
duration: "1:31:40"
institution: University of Ljubljana
lang: en
accent: "#1d5c8a"
---

# The derivative [03:15]

::: idea
The derivative tells you how fast a function changes at a point: the slope of the tangent line.
:::

::: def Derivative
A function $f$ is **differentiable** at a point $a$ if the limit
$$ f'(a) = \lim_{h\to 0} \frac{f(a+h)-f(a)}{h} $$
exists.
:::

::: exam
"You have to be able to write down the definition of the derivative from memory, it's on every midterm." [07:40]
:::

## Basic derivatives [12:05]

::: formula Table of basic derivatives
| $f(x)$ | $f'(x)$ |
|---|---|
| $x^n$ | $n x^{n-1}$ |
| $e^x$ | $e^x$ |
| $\sin x$ | $\cos x$ |
:::

# The chain rule [34:12]

::: formula Chain rule
$$ (f\circ g)'(x) = f'(g(x))\cdot g'(x) $$
:::

::: warn
Common mistake: forgetting to multiply by the derivative of the inner function.
:::

::: unclear Formula on the board [41:20]
The lecturer pointed at the board ("and this cancels out"); the audio doesn't make clear which term.
:::

::: task Derivative of a composite function [52:40]
Differentiate $h(x) = \sin(x^2+1)$.
:::
@@space 4
::: sol
Outer $f(u)=\sin u$, inner $g(x)=x^2+1$:
$$ h'(x) = \cos(x^2+1)\cdot 2x $$

**Result:** $h'(x) = 2x\cos(x^2+1)$
:::

::: summary
| Concept | Key idea |
|---|---|
| Derivative | limit of the difference quotient |
| Chain rule | outer derivative × inner derivative |
:::

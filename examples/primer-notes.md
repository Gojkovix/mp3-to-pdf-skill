---
course: Matematika 1
chapter: 5
title: Odvod in verižno pravilo
lecturer: prof. dr. Janez Novak
date: 2026-10-08
duration: "1:31:40"
institution: FRI UL
lang: sl
accent: "#1d5c8a"
---

# Odvod funkcije [03:15]

::: idea
Odvod pove, kako hitro se funkcija spreminja v točki — naklon tangente.
:::

::: def Odvod
Funkcija $f$ je **odvedljiva** v točki $a$, če obstaja limita
$$ f'(a) = \lim_{h\to 0} \frac{f(a+h)-f(a)}{h}. $$
:::

::: exam
»Definicijo odvoda morate znati napisati na pamet, to je vedno na kolokviju.« [07:40]
:::

## Osnovni odvodi [12:05]

::: formula Tabela osnovnih odvodov
| $f(x)$ | $f'(x)$ |
|---|---|
| $x^n$ | $n x^{n-1}$ |
| $e^x$ | $e^x$ |
| $\sin x$ | $\cos x$ |
:::

# Verižno pravilo [34:12]

::: formula Verižno pravilo
$$ (f\circ g)'(x) = f'(g(x))\cdot g'(x) $$
:::

::: warn
Pogosta napaka: pozabiti pomnožiti z odvodom notranje funkcije.
:::

::: unclear Formula na tabli [41:20]
Predavatelj je pokazal na tablo (»in tole se pokrajša«); iz zvoka ni jasno, kateri člen.
:::

::: task Odvod sestavljene funkcije [52:40]
Odvajaj $h(x) = \sin(x^2+1)$.
:::
@@space 4
::: sol
Zunanja $f(u)=\sin u$, notranja $g(x)=x^2+1$:
$$ h'(x) = \cos(x^2+1)\cdot 2x $$

**Rezultat:** $h'(x) = 2x\cos(x^2+1)$
:::

::: summary
| Pojem | Bistvo |
|---|---|
| Odvod | limita diferenčnega kvocienta |
| Verižno pravilo | zunanji odvod × notranji odvod |
:::

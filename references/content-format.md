# notes.md format

CommonMark + pipe tables + `$math$` (KaTeX) + `:::` boxes + `[mm:ss]` timestamps + `@@space N`.
`scripts/build.py` turns it into HTML and a PDF.

## Frontmatter

```yaml
---
course: Matematika 1            # cover + footer
chapter: 3                      # big number on the cover ("" for none)
title: Odvod in njegova uporaba
lecturer: prof. dr. Janez Novak # only if said in the recording or given by the student
date: 2026-10-08                # lecture date if known
duration: "1:32:10"             # recording length (from transcript.json)
institution: FRI UL
lang: sl                        # sl | en  (box labels)
accent: "#1d5c8a"               # one colour per course; keep it across lectures
solutions: inline               # inline | end (appendix)
formula_sheet: yes              # yes = appendix "Formule na enem mestu" (all formula/rule/thm boxes)
---
```

## Headings

`#` = numbered section (new page), `##` = subsection. Both go into the table of contents.
Put the timestamp where the topic starts in the recording at the end of the heading:
`## Verižno pravilo [34:12]` — it renders as a small grey chip, not in the TOC.

## Boxes

```
::: formula Verižno pravilo
$$ (f\circ g)'(x) = f'(g(x))\cdot g'(x) $$
:::
```

| Fence | sl label | Use for | Numbered |
|---|---|---|---|
| `def` | Definicija | definitions as the lecturer stated them | yes |
| `formula` | Formula | a formula/identity to memorise — ends up on the formula sheet | yes |
| `rule` | Pravilo | procedural rule, algorithm, recipe ("najprej…, nato…") — formula sheet | yes |
| `thm` | Izrek | named theorem/law with conditions — formula sheet | yes |
| `ex` | Zgled | an example the lecturer worked through | yes |
| `task` | Naloga | exercise for the student (homework, "poskusite sami", typical exam task) | yes |
| `sol` | Rešitev | solution of the task directly above | no |
| `idea` | Ideja | intuition / the "why" | no |
| `warn` | Pozor | pitfalls, typical mistakes the lecturer warned about | no |
| `exam` | Za izpit | anything the lecturer said about the exam, tests, what to know | no |
| `unclear` | Nejasno v posnetku | a passage you could not reconstruct reliably — with timestamp | no |
| `proof` | Dokaz | proof / derivation | no |
| `summary` | Povzetek | end-of-lecture summary table | no |

Title after the fence name is optional and may contain `$math$`. Boxes cannot nest.
A box never splits across pages, so keep one box under ~⅔ of a page (`sol` may split).

## Exercises

```
::: task Odvod sestavljene funkcije [52:40]
Odvajaj $h(x) = \sin(x^2+1)$.
:::
@@space 4
::: sol
Zunanja $f(u)=\sin u$, notranja $g(x)=x^2+1$. Po verižnem pravilu …

**Rezultat:** $h'(x) = 2x\cos(x^2+1)$
:::
```

`@@space N` = ruled workspace N cm high (2.5–3 one-liner, 4–5 short derivation, 6–7 proof).

## Math

Inline `$…$`, display `$$ … $$` on its own lines. KaTeX syntax. Multi-step derivations:
`\begin{aligned} … &= … && \text{(razlog)} \\ … \end{aligned}`. Slovenian decimal comma: `0{,}25`.
Units: `9{,}81\,\mathrm{m/s^2}`. Never leave a spoken formula as words if it can be written as math.

## Other

- Code (programming lectures): fenced ``` blocks with a language tag.
- Diagrams: inline `<figure><svg viewBox="…">…</svg><figcaption>…</figcaption></figure>`;
  stroke 1.5, labels in Inter 11px, accent colour. Only where there is real structure.
- Separate lines inside a box need a blank line between them.
- Slovenian quotes »…«.

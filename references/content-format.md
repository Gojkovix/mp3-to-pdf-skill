# notes.md format

CommonMark + pipe tables + `$math$` (KaTeX) + `:::` boxes + `[mm:ss]` timestamps + `@@space N`.
`scripts/build.py` turns it into HTML and a PDF.

## Frontmatter

```yaml
---
course: Calculus 1              # cover + footer
chapter: 3                      # big number on the cover ("" for none)
title: Derivatives and their applications
lecturer: Prof. Jane Smith      # only if said in the recording or given by the student
date: 2026-10-08                # lecture date if known
duration: "1:32:10"             # recording length (from transcript.json)
institution: University of Ljubljana
lang: en                        # sl | en  (box labels; use the lecture's language)
accent: "#1d5c8a"               # one colour per course; keep it across lectures
solutions: inline               # inline | end (appendix)
formula_sheet: yes              # yes = appendix "Formula sheet" / "Formule na enem mestu" (all formula/rule/thm boxes)
---
```

## Headings

`#` = numbered section (new page), `##` = subsection. Both go into the table of contents.
Put the timestamp where the topic starts in the recording at the end of the heading:
`## Chain rule [34:12]` — it renders as a small grey chip, not in the TOC.

## Boxes

```
::: formula Chain rule
$$ (f\circ g)'(x) = f'(g(x))\cdot g'(x) $$
:::
```

| Fence | Label (en / sl) | Use for | Numbered |
|---|---|---|---|
| `def` | Definition / Definicija | definitions as the lecturer stated them | yes |
| `formula` | Formula / Formula | a formula/identity to memorise — ends up on the formula sheet | yes |
| `rule` | Rule / Pravilo | procedural rule, algorithm, recipe ("first…, then…") — formula sheet | yes |
| `thm` | Theorem / Izrek | named theorem/law with conditions — formula sheet | yes |
| `ex` | Example / Zgled | an example the lecturer worked through | yes |
| `task` | Exercise / Naloga | exercise for the student (homework, "try it yourself", typical exam task) | yes |
| `sol` | Solution / Rešitev | solution of the task directly above | no |
| `idea` | Idea / Ideja | intuition / the "why" | no |
| `warn` | Watch out / Pozor | pitfalls, typical mistakes the lecturer warned about | no |
| `exam` | For the exam / Za izpit | anything the lecturer said about the exam, tests, what to know | no |
| `unclear` | Unclear in recording / Nejasno v posnetku | a passage you could not reconstruct reliably — with timestamp | no |
| `proof` | Proof / Dokaz | proof / derivation | no |
| `summary` | Summary / Povzetek | end-of-lecture summary table | no |

Title after the fence name is optional and may contain `$math$`. Boxes cannot nest.
A box never splits across pages, so keep one box under ~⅔ of a page (`sol` may split).

## Exercises

```
::: task Derivative of a composite function [52:40]
Differentiate $h(x) = \sin(x^2+1)$.
:::
@@space 4
::: sol
Outer $f(u)=\sin u$, inner $g(x)=x^2+1$. By the chain rule …

**Result:** $h'(x) = 2x\cos(x^2+1)$
:::
```

`@@space N` = ruled workspace N cm high (2.5–3 one-liner, 4–5 short derivation, 6–7 proof).

## Math

Inline `$…$`, display `$$ … $$` on its own lines. KaTeX syntax. Multi-step derivations:
`\begin{aligned} … &= … && \text{(reason)} \\ … \end{aligned}`. Slovenian decimal comma: `0{,}25`.
Units: `9{,}81\,\mathrm{m/s^2}`. Never leave a spoken formula as words if it can be written as math.

## Other

- Code (programming lectures): fenced ``` blocks with a language tag.
- Diagrams: inline `<figure><svg viewBox="…">…</svg><figcaption>…</figcaption></figure>`;
  stroke 1.5, labels in Inter 11px, accent colour. Only where there is real structure.
- Separate lines inside a box need a blank line between them.
- Slovenian quotes »…«.

# Writing rules — from a spoken lecture to notes you can learn from

A transcript is not notes. Speech is 3–5× longer than the written content it carries: repetitions,
"ne?", "torej", false starts, admin talk, questions from the room. And the most important part —
what the lecturer wrote on the board — is often *not in the audio at all*, only pointed at
("tole tukaj delimo s tem"). Your job is to reconstruct the lecture as the lecturer would have
written it, then add what a student needs to learn it alone.

## 1. Reading the transcript

- Read all of `transcript.txt` once before planning. Topic boundaries show as "zdaj gremo na…",
  "naslednja stvar…", "dobro, to je to za…", or a long pause/break.
- Whisper errors are phonetic. Fix them from context: "integral od iks na kvadrat" is $\int x^2\,dx$;
  "kovarianca" misheard as "ko varianca"; names of theorems, people and Latin/English terms get mangled
  (Lagrange → "lagranž", eigenvalue → "ajgen"). Use your subject knowledge to recover the real term.
- `low_confidence.txt` lists segments Whisper itself doubted. Look at each one in context.
- Repeated identical lines (e.g. the same sentence 5×) or text in a wrong language are hallucinations
  during silence or noise — drop them.
- Questions from students: keep the content of the answer if it adds something; the student's own
  question often reveals a common confusion → a `warn` box.

## 2. Reconstructing formulas from speech

Spoken math is ambiguous. Resolve it with the surrounding derivation, the subject, and dimensional
sanity; then write proper LaTeX.

| Spoken (sl) | Spoken (en) | Write |
|---|---|---|
| a na kvadrat plus b na kvadrat | a squared plus b squared | $a^2 + b^2$ |
| ena skozi n | one over n | $\frac{1}{n}$ |
| koren iz x plus ena | square root of x plus one | ambiguous: $\sqrt{x}+1$ or $\sqrt{x+1}$ — decide from what follows |
| limita, ko gre n proti neskončno | limit as n goes to infinity | $\lim_{n\to\infty}$ |
| vsota po i od ena do n | sum from i equals one to n | $\sum_{i=1}^{n}$ |
| f črtica od x | f prime of x | $f'(x)$ |
| delta x, d x | delta x, d x | $\Delta x$, $dx$ |
| a indeks i j | a sub i j | $a_{ij}$ |
| e na minus lambda t | e to the minus lambda t | $e^{-\lambda t}$ |

When the lecturer only points ("in to tukaj se pokrajša s tem"), reconstruct the step from the
mathematics and the result they state next. If a formula is *partly* reconstructed, write the best
version and add one line in a `warn` box, in the lecture's language: "Reconstructed from context [mm:ss] – check
against the board/slides." (sl: "Rekonstruirano iz konteksta [mm:ss] – preveri s tablo/prosojnicami.")
If you genuinely cannot recover it, use an `unclear` box with the timestamp so the student knows where to
listen. Never invent a formula silently — a confident wrong formula on an exam sheet is worse than a gap.

## 3. What goes in which box

- Anything the lecturer **defined** ("we say that…", "we define…", "this is called…"; sl: "pravimo, da je…", "definiramo…", "temu rečemo…") → `def`.
- Any **formula, identity, relationship** students must know → `formula` (it goes on the formula sheet).
- **Procedures/recipes** ("postopek je tak: najprej…") → `rule` with numbered steps.
- **Named theorems/laws** with conditions → `thm`; state the conditions explicitly — lecturers often say
  them once, quickly.
- Every **example worked aloud** → `ex`, with all steps written out (fill in steps the lecturer skipped
  or did silently on the board).
- **Exercises**: homework, "try this yourself", "a typical exam problem", an example the lecturer
  started but didn't finish (sl: "to poskusite sami", "tipična izpitna naloga", "za domačo nalogo") → `task` + `@@space` + `sol`. Solve them fully: method in
  one sentence, every step with the rule named, **bold result**.
- **Exam hints**: "to bo na izpitu", "to morate znati", "tega ne bo", "na kolokviju…", deadlines,
  allowed materials → `exam` box at the point where it was said. Students value these most; don't
  lose a single one.
- **Pitfalls** the lecturer warned about ("a lot of students get this wrong…"; sl: "tu veliko študentov naredi napako…") → `warn`.
- The lecturer's analogies and motivation → `idea` (one per concept is enough).

## 4. What to drop

Greetings, attendance, technical trouble, jokes without content, repeated explanations (keep the
clearest one), "a je jasno?", organisational talk *except* anything about exams, homework, deadlines
and grading (those go in `exam`).

## 5. Adding value beyond the recording

- Each concept: idea → def/formula → worked example → pitfall. If the lecturer gave no example
  for a key formula, add one short example and say "(added example)" / "(dodan zgled)" in its title.
- If the lecturer made a mistake (sign error, wrong number — it happens when talking), keep the
  correct version and flag it: `warn` titled "Correction" / "Popravek" with what was said vs. what is correct.
- Standard background knowledge you add should be marked: "Addition (not covered in the lecture): …" / "Dopolnilo (ni bilo na predavanju): …".
  The student needs to know what is examinable.
- Length: notes ≈ 30–50 % of the transcript's word count plus solutions. A 90-min lecture
  (~12–14k spoken words) → typically 12–25 A4 pages.

## 6. Language and tone

Write in the lecture's language, with the lecturer's terminology (if they say "množica", don't write
"set"). Plain, direct sentences, standard written language (not the spoken dialect of the transcript).
No emoji, no filler, no "V tem poglavju bomo…".

## Checklist before building

- [ ] Every topic of the recording appears, in the lecturer's order, with a timestamp in its heading
- [ ] Every definition / formula / theorem stated aloud is in a box, written as proper math
- [ ] Every example is worked out completely; every exercise has a solution
- [ ] Every exam hint is in an `exam` box
- [ ] Uncertain reconstructions are flagged (`warn`/`unclear` with timestamp), nothing silently invented
- [ ] Summary table at the end covers every section

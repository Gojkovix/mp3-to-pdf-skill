---
name: mp3-to-pdf
description: Turn a recorded lecture (MP3, M4A, WAV, voice memo, video of a lecture) into a print-ready PDF study workbook — accurate local transcription with Whisper, then properly reconstructed formulas (LaTeX), definitions, worked examples, solved exercises, exam hints, timestamps back into the recording, and a formula sheet. Use this whenever the user gives an audio/video recording of a lecture, class, vaje, seminar or tutorial, or asks to "transcribe", "prepiši", "naredi zapiske iz posnetka", "posnetek predavanja v PDF", "iz mp3 naredi PDF", "da se lažje naučim" — even if they only drop an .mp3 file with no explanation. Also use when they give a recording together with slides or board photos.
---

# Lecture recording → PDF to learn from

The student gives a recording; they get back a PDF they can learn from alone: structured notes in
the lecturer's terminology, every formula written as real math, every example and exercise worked out,
every exam hint highlighted, and a timestamp next to each topic so they can re-listen to any part.

A raw transcript is useless for learning (spoken text is 3–5× too long and the board is not in it), and
cloud "summaries" lose the formulas. The value here is the *reconstruction* — read
`references/writing-rules.md` before writing; it is the quality bar.

`<skill>` below = the folder containing this file. Use `python` (Windows) or `python3` (macOS/Linux).

## 1. Setup and intake

```bash
python <skill>/scripts/setup.py
```

Idempotent and fast once everything is installed; works on Windows, macOS and Linux without admin
rights. It installs missing Python packages (into a private venv in `~/.cache/mp3-to-pdf` when the
system Python refuses pip installs; the other scripts then switch to it automatically), downloads
KaTeX, and finds a Chromium-based browser for PDF printing, downloading one if none is installed.
If it ends with `setup INCOMPLETE`, show the student the `FAIL` lines; they say exactly what to do.

Then collect, without a long interview — ask only what you cannot infer, in one message:
- **Course name and lecture topic/number** (often in the filename or folder; otherwise the lecturer says
  it in the first minutes — check the transcript before asking).
- **Slides, board photos, or a syllabus?** If the student has them, they massively improve formulas and
  terminology. Optional — never block on it.
- Language: default Slovenian (`sl`); use `--lang auto` if unsure.

## 2. Transcribe (local, offline)

```bash
python <skill>/scripts/transcribe.py "<lecture.mp3>" "<work>" --lang sl --prompt "<course>: <10–30 key terms>"
```

- `<work>` = a folder next to the recording, e.g. `<name>_work/`. Output PDF goes next to the recording.
- `--prompt` steers Whisper's spelling of jargon. Fill it with the course name and terms you expect
  (from the slides, the filename, or your knowledge of the subject: e.g. "Verjetnost in statistika:
  pričakovana vrednost, varianca, kovarianca, Poissonova porazdelitev, centralni limitni izrek").
  This is the cheapest accuracy win — do not skip it.
- Default model `large-v3-turbo` (≈1.6 GB, cached after first use). On a CPU expect roughly 0.15–0.4×
  real time, i.e. a 90-min lecture takes ~15–35 min. **Run it in the background** (`run_in_background`)
  and tell the student the estimate; the script prints progress with an ETA. Meanwhile read any slides.
- For very poor audio (far microphone, strong echo) re-run only the bad part or the whole file with
  `--model large-v3` (slower, a bit more accurate).

Outputs: `transcript.txt` (`[mm:ss] text` per line), `transcript.json`, `low_confidence.txt`.

## 3. Read and plan

Read `transcript.txt` in full (chunked if long — every part matters, exam hints hide in the last
minutes). Read `references/writing-rules.md` and `references/content-format.md`.

Write a short plan for yourself:
1. Topic list with start timestamps → 4–10 `#` sections with `##` subsections, in the lecturer's order.
2. Every definition, formula, theorem, procedure stated aloud.
3. Every example and exercise (incl. homework, "poskusite sami", unfinished examples).
4. Every exam/organisational hint (what's on the exam, deadlines, "tega ne bo").
5. Passages where the board was used and the audio alone doesn't give the formula → reconstruct; mark
   what stays uncertain.

## 4. Write `notes.md`

Write `<work>/notes.md` in the format of `references/content-format.md`. Per concept:
**idea** (why) → **def/formula/thm/rule** (exact, as proper LaTeX) → **ex** (fully worked) → **warn**
(pitfall) → **exam** where the lecturer hinted. Exercises: `task` → `@@space N` → `sol`.
End with a `summary` table (one row per section). The builder appends the formula sheet automatically.

For long lectures write section by section (append to the file) rather than one giant write.

**Recordings over ~2 hours** (double lectures, 3 h blocks): the transcript is 25k+ words, too much to
hold in mind at once. Read it in chunks of ~30 minutes; after each chunk append that part's
notes to `notes.md` and keep a running list (topics, open exercises, exam hints, terms) so nothing
from early chunks is lost. If the lecture covers clearly separate topics (often before/after
the break), offer the student two PDFs (`…_part1.pdf`, `…_part2.pdf`) instead of one 50-page file.

## 5. Build and check

```bash
python <skill>/scripts/build.py "<work>/notes.md" "<out>/<Course>_<nn>_<Topic>.pdf"
```

The build prints a QA line: math errors (with the offending LaTeX), unparsed `:::` boxes, raw `$…$`.
Fix every reported problem and rebuild until it says `OK`.

Then look at the PDF yourself with the Read tool (pages 1–6 and a few from the middle): cover/TOC
correct, formulas rendered, no box cut awkwardly, tasks next to their workspace. Cross-check: each
item from the plan in step 3 is in the PDF.

## 6. Deliver

Give the student the PDF path (and offer to move it if it's in a temporary folder). In 2–4 lines say:
how many sections/exercises, what you added (solutions, extra examples), and **list the `unclear`/
reconstructed spots with timestamps** so they can check them against the board photos or a classmate.
Keep `transcript.txt` beside it — mention it exists in case they want to search it.

## Rules that matter most

- **Formulas as math, never as words.** "a na kvadrat" in the PDF is a failure; $a^2$ is the job.
- **Don't silently invent.** Reconstruct what the context determines; flag what it doesn't, with a
  timestamp. A confident wrong formula is worse than a marked gap.
- **Lecturer's terminology and order.** The exam uses their words.
- **Every exercise solved, every exam hint kept.** These are the highest-value parts of a lecture.
- **Timestamps on every section and on every flagged spot**, so the PDF and the recording work together.
- No flashcards, quizzes, emoji or motivational filler — notes, not a course platform.

## Files

- `scripts/setup.py` — dependency check/installer (Python packages, KaTeX, browser); no admin rights needed
- `scripts/_env.py` — shared helpers: private venv switching, browser lookup per OS
- `scripts/transcribe.py` — audio → timestamped transcript (faster-whisper, offline, VAD, progress/ETA)
- `scripts/build.py` — notes.md → HTML → PDF via headless Edge/Chrome; formula sheet; QA report
- `theme/theme.css` — the design (A4, boxes, timestamp chips); change looks here only
- `references/writing-rules.md` — how to turn speech into notes; formula reconstruction table; box choice
- `references/content-format.md` — notes.md syntax: frontmatter, boxes, math, exercises
- `examples/example-notes.md` + `examples/example.pdf` — a small complete example of the format and look
- `README.md` — for humans (installation, usage); not needed while running the skill

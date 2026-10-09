# mp3-to-pdf

**Lecture recording → a PDF you can actually learn from.**

Give Claude an MP3 of a lecture and get back a clean, printable PDF: formulas written as real math, definitions in boxes, examples worked out to the end, solved exercises, everything the professor said about the exam highlighted, and a formula sheet at the end. Every section has a timestamp, so you can jump straight to that part of the recording.

> **Example output:** [`examples/example.pdf`](examples/example.pdf)

---

## Why not just a transcript?

A plain transcript of a 90-minute lecture is about 13,000 words of repetition, "right?" and "so", and the most important part, whatever was on the board, isn't in it at all. This skill doesn't transcribe, it **reconstructs the lecture** the way the professor would have written it:

| Plain transcript                                          | mp3-to-pdf                                                        |
| --------------------------------------------------------- | ----------------------------------------------------------------- |
| "eff of gee of ex prime equals eff prime …"               | $(f\circ g)'(x) = f'(g(x))\cdot g'(x)$ in a green _Formula_ box   |
| example half done, because the rest was on the board      | example worked out completely, every step names its rule          |
| "for homework …" gets lost in the rest of the text        | _Exercise_ box + space to work + solution                         |
| "this will be on the exam" gets lost                      | red **For the exam** box with a timestamp                         |
| transcription errors ("lagrange" → "la grange", "eigen")  | corrected technical terms                                         |
| unclear passages are silently wrong                       | grey _Unclear in recording_ box + timestamp, so you know what to check |

## What's in the PDF

- **Cover page with table of contents** (course, topic, lecturer, date, recording length)
- **Numbered sections** in the lecture's order, each with a timestamp `[34:12]`
- **Coloured boxes:** Definition · Formula · Theorem · Rule · Example · Exercise + Solution · Idea · Watch out · **For the exam** · Unclear in recording
- **Work space** under every exercise (ruled, print-friendly)
- **Summary** at the end and a **formula sheet**: all formulas on one or two pages, for the night before the exam
- A4, ready to print

## Privacy and cost

- **Transcription runs locally on your computer** (Whisper). The recording is never uploaded anywhere.
- Transcription is free. Claude then writes the notes in your conversation, so it uses some of your Claude usage.

---

## Installation (once, ~5 minutes)

### Requirements

|                                                          | Why                            | Where                                                                                     |
| -------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------- |
| **Claude desktop app** (_Code_ tab) or **Claude Code**   | runs the skill                 | [claude.com/download](https://claude.com/download)                                        |
| **Python 3.10+**                                         | transcription and PDF building | [python.org](https://www.python.org/downloads/) (tick _Add to PATH_ during installation) |
| **Edge or Chrome**                                       | printing to PDF                | Edge comes with Windows                                                                   |

> **Note:** use the skill in the **Code** tab (or Claude Code in a terminal), because transcription runs on your computer. It does not work in a regular chat on claude.ai in the browser.

### 1. Download the skill

Download **[mp3-to-pdf.skill](https://github.com/<username>/mp3-to-pdf/releases/latest/download/mp3-to-pdf.skill)**.

### 2. Add it to Claude

In the Claude app open **Settings → Capabilities → Skills** (in newer versions **Customize → Skills**), click **Upload skill** and choose the downloaded `mp3-to-pdf.skill`. The skill appears in the list; just make sure it's turned on.

If someone sends you `mp3-to-pdf.skill` in a Claude conversation, it's even easier: click **Save skill** on the file card.

That's it. On first use Claude installs whatever is missing (Python packages, KaTeX for formulas) and downloads the speech model (~1.6 GB, once).

### Updating

Download the new `mp3-to-pdf.skill` from the same link, remove the old version in Skills and upload the new one.

<details>
<summary>Install with git (for developers)</summary>

```bash
git clone https://github.com/<username>/mp3-to-pdf.git ~/.claude/skills/mp3-to-pdf
```

On Windows PowerShell use `$env:USERPROFILE` instead of `~`. To update, run `git pull` in that folder. A skill installed this way is only visible to Claude Code on that computer.

</details>

---

## Usage

Send the recording and say which course it's for:

```
Here's the recording of my Calculus 1 lecture on derivatives: C:\Users\me\Downloads\calc1_lecture5.mp3
```

Or even shorter: just drag the MP3 into the conversation. The skill starts on its own.

**For an even better result**, add:

- **slides** (PDF): formulas and terms come out exact,
- **photos of the board**: they fill in the spots where the professor only pointed at "this here",
- a few **key terms** of the course, so the transcription spells them right.

Transcription runs in the background and Claude keeps you posted on progress.

### What it supports

- Formats: `mp3`, `m4a` (iPhone voice memos), `wav`, `ogg`, `opus`, `webm`, `mp4` (video of a lecture)
- Languages: Slovenian by default; English and ~100 other languages work too (just say "the lecture is in English"). The notes are written in the lecture's language.
- Any subject: maths, physics, statistics, programming (code in code blocks), economics, law …

### Where are the results?

Next to the recording you get:

```
calc1_lecture5.mp3
calc1_lecture5_work/
    transcript.txt          ← full transcript with timestamps (handy for searching)
    notes.md                ← source of the notes (edit it and rebuild)
    low_confidence.txt      ← spots where the transcription was unsure
Calculus1_05_Derivatives.pdf ← print this
```

---

## Troubleshooting

| Problem                       | Fix                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `python` is not recognized    | Python isn't on PATH. Reinstall and tick _Add to PATH_, or use `py`.                                         |
| Transcription is very slow    | Normal on older computers. Let it run in the background. For faster but worse results: "use the small model". |
| Many wrong terms              | Tell Claude the course name and a few key terms, or give it the slides.                                      |
| Formulas in the PDF are red   | Claude detects and fixes this itself. If it stays, say "fix the formulas and rebuild the PDF".               |
| No PDF is created             | You need Edge or Chrome. Open the `.html` file next to the PDF and print it to PDF yourself (Ctrl+P).        |
| Uploading the skill fails     | Use `mp3-to-pdf.skill` from the link above (not GitHub's _Code → Download ZIP_).                             |
| The skill doesn't start       | Say it explicitly: "use the mp3-to-pdf skill".                                                               |

## What's in the folder

```
mp3-to-pdf/
├── SKILL.md                    instructions for Claude (how to turn speech into notes)
├── README.md                   this file
├── scripts/
│   ├── setup.py                installation and health check
│   ├── transcribe.py           recording → timestamped transcript (faster-whisper, local)
│   └── build.py                notes → PDF (KaTeX formulas, Edge/Chrome)
├── references/
│   ├── writing-rules.md        rules: from speech to notes, reading spoken formulas
│   └── content-format.md       notes format (boxes, formulas, exercises)
├── theme/theme.css             PDF look (colours, fonts)
└── examples/                   example notes and PDF
```

Want a different colour for your course? Tell Claude "use green" (the `accent` field), or edit `theme/theme.css`.

---

<sub>Transcription: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (OpenAI Whisper large-v3-turbo) · Formulas: [KaTeX](https://katex.org) · Notes: Claude.</sub>

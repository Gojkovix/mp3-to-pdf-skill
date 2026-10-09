#!/usr/bin/env python3
"""notes.md -> notes.html -> notes.pdf  (A4, print-ready, KaTeX math)

usage:  python build.py work/notes.md out/Predmet_01_Naslov.pdf [--html-only]

PDF is printed by headless Edge or Chrome (whichever is installed); no extra
Python packages besides markdown-it-py + mdit-py-plugins. Run setup.py once.

Frontmatter keys (title required):
  course, chapter, title, lecturer, date, duration, institution, lang (sl|en),
  accent (#hex), solutions (inline|end), formula_sheet (yes|no)
"""
import sys, re, pathlib, html, json, shutil, subprocess, tempfile, os

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

I18N = {
    "sl": dict(def_="Definicija", formula="Formula", thm="Izrek", rule="Pravilo", ex="Zgled", task="Naloga",
               sol="Rešitev", idea="Ideja", warn="Pozor", exam="Za izpit", unclear="Nejasno v posnetku",
               summary="Povzetek", proof="Dokaz", toc="Vsebina", space="prostor za reševanje",
               solutions="Rešitve nalog", sheet="Formule na enem mestu", rec="Posnetek", lect="Predavatelj"),
    "en": dict(def_="Definition", formula="Formula", thm="Theorem", rule="Rule", ex="Example", task="Exercise",
               sol="Solution", idea="Idea", warn="Watch out", exam="For the exam", unclear="Unclear in recording",
               summary="Summary", proof="Proof", toc="Contents", space="work space",
               solutions="Solutions", sheet="Formula sheet", rec="Recording", lect="Lecturer"),
}
NUMBERED = {"def", "formula", "thm", "rule", "ex", "task"}

def parse_frontmatter(text):
    meta = {}
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if k.strip() and not k.strip().startswith("#"):
                meta[k.strip()] = v.split(" #")[0].strip().strip('"')
        text = text[m.end():]
    return meta, text

def find_browser():
    cands = [
        os.environ.get("PDF_BROWSER", ""),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for c in cands:
        if c and pathlib.Path(c).exists():
            return c
    for n in ("msedge", "google-chrome", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(n)
        if p:
            return p
    sys.exit("No Edge/Chrome/Chromium found for PDF printing (set PDF_BROWSER=path).")

def main():
    src = pathlib.Path(sys.argv[1]).resolve()
    out_pdf = pathlib.Path(sys.argv[2]).resolve()
    html_only = "--html-only" in sys.argv
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    meta, text = parse_frontmatter(src.read_text(encoding="utf-8"))
    lang = meta.get("lang", "sl")
    T = dict(I18N.get(lang, I18N["en"]))
    accent = meta.get("accent", "#1d5c8a")

    from markdown_it import MarkdownIt
    from mdit_py_plugins.container import container_plugin
    from mdit_py_plugins.dollarmath import dollarmath_plugin

    # @@space N  -> ruled workspace N cm high
    text = re.sub(r"^@@space[ \t]+([\d.]+)[ \t]*$",
                  lambda m: f'\n<div class="space" style="height:{float(m.group(1))}cm"><span>{T["space"]}</span></div>\n',
                  text, flags=re.M)
    # display math on its own block
    lines, fixed = text.split("\n"), []
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("$$") and fixed and fixed[-1].strip():
            fixed.append("")
        fixed.append(ln)
        if ln.rstrip().endswith("$$") and len(ln.strip()) > 2 and i + 1 < len(lines) and lines[i + 1].strip():
            fixed.append("")
    text = "\n".join(fixed)

    md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable(["table", "strikethrough"])
    md.use(dollarmath_plugin, double_inline=False)
    LABEL = {"def": T["def_"], "formula": T["formula"], "thm": T["thm"], "rule": T["rule"], "ex": T["ex"],
             "task": T["task"], "sol": T["sol"], "idea": T["idea"], "warn": T["warn"], "exam": T["exam"],
             "unclear": T["unclear"], "summary": T["summary"], "proof": T["proof"]}

    def title_html(t):
        parts = re.split(r"(\$[^$]+\$)", t)
        return "".join(f'<span class="math">{html.escape(p[1:-1])}</span>' if p.startswith("$") else html.escape(p)
                       for p in parts)

    def make_render(kind):
        def render(self, tokens, idx, options, env):
            t = tokens[idx]
            if t.nesting == 1:
                title = t.info.strip()[len(kind):].strip()
                num = ' data-num="1"' if kind in NUMBERED else ""
                head = (f'<div class="bx-head"><span class="bx-label"{num}>{LABEL[kind]}</span>'
                        + (f'<span class="bx-title">{title_html(title)}</span>' if title else "") + "</div>")
                return f'<div class="bx bx-{kind}">{head}<div class="bx-body">'
            return "</div></div>\n"
        return render
    for k in LABEL:
        md.use(container_plugin, name=k, render=make_render(k))
    md.add_render_rule("math_inline", lambda s, tk, i, o, e: f'<span class="math">{html.escape(tk[i].content)}</span>')
    md.add_render_rule("math_block", lambda s, tk, i, o, e: f'<div class="math display">{html.escape(tk[i].content)}</div>')
    body = md.render(text)
    # [12:34] or [1:02:03] -> timestamp chip pointing back into the recording
    body = re.sub(r"\[(\d{1,2}:\d{2}(?::\d{2})?)\]", r'<span class="ts">\1</span>', body)

    # numbering + TOC
    toc, n = [], [0, 0]
    def num_h(m):
        lvl, attrs, inner = m.group(1), m.group(2), m.group(3)
        if lvl == "1":
            n[0] += 1; n[1] = 0; num = f"{n[0]}"
        else:
            n[1] += 1; num = f"{n[0]}.{n[1]}"
        toc.append((lvl, num, re.sub(r'<span class="ts">.*?</span>', "", inner).strip()))
        return f'<h{lvl}{attrs}><span class="hnum">{num}</span>{inner}</h{lvl}>'
    body = re.sub(r"<h([12])([^>]*)>(.*?)</h\1>", num_h, body)
    toc_html = "".join(f'<li class="l{l}"><span class="tnum">{nm}</span>{t}</li>' for l, nm, t in toc)

    css = (ROOT / "theme" / "theme.css").read_text(encoding="utf-8").replace("ACCENT", accent)
    E = lambda k: html.escape(meta.get(k, ""))
    footer_left = f'{meta.get("course", "")} · {meta.get("title", "")}'.strip(" ·").replace('"', "'")
    css += f'\n@page {{ @bottom-left {{ content: "{footer_left}"; }} }}\n'

    kdir = ROOT / "vendor" / "node_modules" / "katex" / "dist"
    if kdir.exists():
        kcss = (kdir / "katex.min.css").read_text(encoding="utf-8").replace("url(fonts/", f"url({kdir.as_uri()}/fonts/")
        katex_tags = f"<style>{kcss}</style>", f"<script>{(kdir / 'katex.min.js').read_text(encoding='utf-8')}</script>"
    else:
        cdn = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
        katex_tags = f'<link rel="stylesheet" href="{cdn}/katex.min.css">', f'<script src="{cdn}/katex.min.js"></script>'
        print("note: KaTeX not vendored (run setup.py); using CDN", file=sys.stderr)

    cover_meta = " · ".join(x for x in [E("lecturer"), E("date"), E("institution")] if x)
    rec = f'{T["rec"]}: {E("duration")}' if meta.get("duration") else ""
    page = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<title>{E('course')} – {E('title')}</title>{katex_tags[0]}<style>{css}</style></head><body>
<section class="cover">
  <div class="cover-course">{E('course')}</div>
  <div class="cover-num">{E('chapter')}</div>
  <h1 class="cover-title">{E('title')}</h1>
  <div class="cover-meta">{cover_meta}<br>{rec}</div>
  <div class="toc"><div class="toc-head">{html.escape(T['toc'])}</div><ul>{toc_html}</ul></div>
</section>
<main>{body}</main>
{katex_tags[1]}
<script>
const T = {json.dumps(T, ensure_ascii=False)};
const SOL_END = {json.dumps(meta.get("solutions", "inline") == "end")};
const SHEET = {json.dumps(meta.get("formula_sheet", "yes") != "no")};
const main = document.querySelector('main');
// numbering per box kind
const cnt = {{}};
document.querySelectorAll('.bx-label[data-num]').forEach(l => {{
  const k = l.closest('.bx').className.match(/bx-(\\w+)/)[1]; cnt[k] = (cnt[k] || 0) + 1;
  l.textContent += ' ' + cnt[k]; l.closest('.bx').dataset.n = cnt[k];
}});
// formula sheet: every formula/rule/thm box, cloned to an appendix
if (SHEET) {{
  const boxes = main.querySelectorAll('.bx-formula, .bx-rule, .bx-thm');
  if (boxes.length) {{
    const sec = document.createElement('section'); sec.className = 'sheet';
    sec.innerHTML = '<h1><span class="hnum"></span>' + T.sheet + '</h1>';
    const grid = document.createElement('div'); grid.className = 'sheet-grid';
    boxes.forEach(b => grid.appendChild(b.cloneNode(true))); sec.appendChild(grid); main.appendChild(sec);
  }}
}}
if (SOL_END) {{
  const app = document.createElement('section'); app.className = 'solutions';
  app.innerHTML = '<h1><span class="hnum"></span>' + T.solutions + '</h1>';
  main.querySelectorAll('.bx-task').forEach(t => {{
    let s = t.nextElementSibling; if (s && s.classList.contains('space')) s = s.nextElementSibling;
    if (s && s.classList.contains('bx-sol')) {{ s.querySelector('.bx-label').textContent = T.sol + ' – ' + T.task + ' ' + t.dataset.n; app.appendChild(s); }}
  }});
  main.appendChild(app);
}}
const wrap = (a, b) => {{ const w = document.createElement('div'); w.className = 'keep'; a.parentNode.insertBefore(w, a); w.appendChild(a); w.appendChild(b); }};
main.querySelectorAll('.bx-task').forEach(t => {{ const s = t.nextElementSibling; if (s && s.classList.contains('space')) wrap(t, s); }});
main.querySelectorAll('h1, h2, h3').forEach(h => {{ const x = h.nextElementSibling; if (x) wrap(h, x); }});
document.querySelectorAll('.math').forEach(el => {{
  try {{ katex.render(el.textContent, el, {{displayMode: el.classList.contains('display'), throwOnError: true}}); }}
  catch (e) {{ el.classList.add('math-error'); el.title = String(e); }}
}});
document.body.dataset.ready = '1';
</script></body></html>"""
    out_html = out_pdf.with_suffix(".html")
    out_html.write_text(page, encoding="utf-8")
    print("wrote", out_html)
    if html_only:
        return

    browser = find_browser()
    with tempfile.TemporaryDirectory() as prof:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={prof}",
               "--no-pdf-header-footer", "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
               f"--print-to-pdf={out_pdf}", out_html.as_uri()]
        subprocess.run(cmd, check=False, timeout=180, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dom = subprocess.run([browser, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}",
                              "--virtual-time-budget=20000", "--dump-dom", out_html.as_uri()],
                             capture_output=True, timeout=180).stdout.decode("utf-8", "replace")
    if not out_pdf.exists():
        sys.exit("PDF printing failed – open the .html in a browser and print to PDF manually.")
    print("wrote", out_pdf)

    # QA: problems that are invisible until rendered
    probs = []
    errs = re.findall(r'class="math[^"]*math-error[^"]*"[^>]*title="([^"]*)"[^>]*>(.*?)</span>', dom)
    probs += [f"math error: {html.unescape(src_)[:80]!r} – {html.unescape(msg)[:90]}" for msg, src_ in errs]
    vis = re.sub(r"<script.*?</script>|<style.*?</style>|<span class=\"katex.*?</span>", "", dom, flags=re.S)
    vis = re.sub(r"<[^>]+>", " ", vis)
    for pat, what in [(r"(?m)^\s*:::", "unparsed ::: box fence"), (r"\$[^$\s][^$]{0,60}\$", "raw $math$")]:
        probs += [f"{what}: {m.group(0)[:70]!r}" for m in re.finditer(pat, vis)][:5]
    if dom and 'data-ready="1"' not in dom:
        probs.append("page script did not finish (KaTeX not loaded?)")
    print("QA: " + ("OK – no math/box errors" if not probs else f"{len(probs)} problem(s):"))
    for p in probs:
        print("  -", p)

if __name__ == "__main__":
    main()

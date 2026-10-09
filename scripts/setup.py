#!/usr/bin/env python3
"""One-time setup / health check. Idempotent; safe to run every time. Windows, macOS, Linux.

usage:  python setup.py        (python3 on macOS/Linux)

1. Python packages: faster-whisper, markdown-it-py, mdit-py-plugins.
   Installed into this Python if pip allows it; otherwise (no pip, or "externally-managed-
   environment" on Ubuntu/Debian/Homebrew) into a private venv in ~/.cache/mp3-to-pdf/venv.
   The other scripts switch to that venv automatically. No admin rights needed.
2. KaTeX (math rendering) downloaded into ~/.cache/mp3-to-pdf so PDFs render offline.
   Kept outside the skill folder because an uploaded skill's folder is replaced on sync.
3. A Chromium-based browser for printing PDFs (Edge, Chrome, Chromium, Brave). If none is
   installed, Playwright's Chromium is downloaded (no admin rights needed).
"""
import glob, io, os, pathlib, shutil, subprocess, sys, tarfile, tempfile, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _env import CACHE, VENV, KATEX, LIBS, venv_python, have, find_browser, browser_works

sys.stdout.reconfigure(line_buffering=True)   # keep our lines in order with child-process output

PKGS = {"faster_whisper": "faster-whisper", "markdown_it": "markdown-it-py", "mdit_py_plugins": "mdit-py-plugins"}
KATEX_VER = "0.16.11"
ok = True


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], **kw).returncode == 0


def make_venv():
    """Private venv. Works even where python3-venv/ensurepip is missing (bootstraps pip)."""
    vp = venv_python()
    if not vp.exists():
        print(f"inst private Python environment in {VENV} …")
        CACHE.mkdir(parents=True, exist_ok=True)
        if not run([sys.executable, "-m", "venv", VENV], capture_output=True):
            run([sys.executable, "-m", "venv", "--clear", "--without-pip", VENV])
    if not run([vp, "-m", "pip", "--version"], capture_output=True):
        print("inst pip (get-pip.py from bootstrap.pypa.io) …")
        gp = CACHE / "get-pip.py"
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", gp)
        run([vp, gp, "-q"])
    return vp


# ---- 1. Python packages
py = pathlib.Path(sys.executable)
if have(PKGS):
    print("ok   python packages (" + ", ".join(PKGS.values()) + ")")
elif venv_python().exists() and run([venv_python(), "-c", "import " + ",".join(PKGS)], capture_output=True):
    py = venv_python()
    print(f"ok   python packages (private env {VENV})")
else:
    missing = [p for m, p in PKGS.items() if not have([m])]
    print("inst " + ", ".join(missing) + " …")
    if not run([sys.executable, "-m", "pip", "install", "-q", *missing], capture_output=True):
        print("     this Python does not allow pip installs – using a private environment instead")
        py = make_venv()
        if not run([py, "-m", "pip", "install", "-q", *PKGS.values()]):
            print("FAIL could not install Python packages"); ok = False
    if ok:
        print("ok   python packages" + ("" if py == pathlib.Path(sys.executable) else f" (private env {VENV})"))

# ---- 2. KaTeX
if (KATEX / "dist" / "katex.min.js").exists():
    print("ok   katex")
else:
    print(f"inst katex {KATEX_VER} …")
    try:
        url = f"https://registry.npmjs.org/katex/-/katex-{KATEX_VER}.tgz"
        data = urllib.request.urlopen(url, timeout=60).read()
        KATEX.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as t:
            for m in t.getmembers():               # strip leading "package/"
                if m.isfile() and m.name.startswith("package/dist/"):
                    m.name = m.name[len("package/"):]
                    t.extract(m, KATEX)
        print("ok   katex")
    except Exception as e:
        print(f"warn katex download failed ({e}) – build.py will load it from the CDN (needs internet)")

def unpack_linux_libs():
    """Debian/Ubuntu without root: download the .debs Chromium needs and unpack them into LIBS."""
    if not (sys.platform.startswith("linux") and shutil.which("apt-get") and shutil.which("dpkg-deb")):
        return False
    want = [("libnss3",), ("libnspr4",), ("libasound2t64", "libasound2")]
    print("inst Chromium system libraries without admin rights (apt-get download → ~/.cache) …")
    got = 0
    with tempfile.TemporaryDirectory() as tmp:
        for alts in want:
            for name in alts:
                if run(["apt-get", "download", "-q", name], cwd=tmp, capture_output=True):
                    got += 1; break
        LIBS.mkdir(parents=True, exist_ok=True)
        for deb in glob.glob(os.path.join(tmp, "*.deb")):
            run(["dpkg-deb", "-x", deb, LIBS])
    return got == len(want)


# ---- 3. Browser for PDF printing
browser = find_browser()
if not browser:
    print("inst no Chrome/Edge/Chromium found – downloading Chromium via Playwright …")
    if run([py, "-m", "pip", "install", "-q", "playwright"]) and run([py, "-m", "playwright", "install", "chromium"]):
        browser = find_browser()
if browser:
    works, err = browser_works(browser)
    if not works and "shared libraries" in err and unpack_linux_libs():
        works, err = browser_works(browser)
    if works:
        print("ok   browser", browser)
    else:
        ok = False
        print("FAIL browser found but cannot start:", browser)
        print("     " + err.strip().replace("\n", "\n     "))
        if sys.platform.startswith("linux"):
            print("     Missing system libraries. Fix with ONE of (needs admin password):\n"
                  "       sudo apt install chromium            (Debian/Ubuntu; or: sudo snap install chromium)\n"
                  f"       sudo {py} -m playwright install-deps chromium")
else:
    ok = False
    print("FAIL no browser for PDF printing. Install Google Chrome or Chromium, or set PDF_BROWSER=/path/to/browser")

# ---- 4. Whisper model
hub = pathlib.Path.home() / ".cache" / "huggingface" / "hub"
models = [p.name.split("--")[-1] for p in hub.glob("models--*whisper*")] if hub.exists() else []
print("ok   whisper models cached:", ", ".join(models) if models else
      "none yet (first transcription downloads ~1.6 GB for large-v3-turbo)")
print("setup ok" if ok else "setup INCOMPLETE")
sys.exit(0 if ok else 1)

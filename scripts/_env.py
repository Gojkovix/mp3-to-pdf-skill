"""Shared environment helpers: private venv, browser lookup.

Many systems don't let you pip-install into the system Python (Debian/Ubuntu 23.04+,
Homebrew Python on macOS: "externally-managed-environment"; minimal Linux: no pip at all).
setup.py then creates a private venv in ~/.cache/mp3-to-pdf/venv, and every script calls
ensure_modules() so it transparently re-runs itself with that venv's Python.
"""
import glob, os, pathlib, shutil, subprocess, sys

CACHE = pathlib.Path.home() / ".cache" / "mp3-to-pdf"
VENV = CACHE / "venv"
KATEX = CACHE / "node_modules" / "katex"
LIBS = CACHE / "libs"   # Linux: shared libraries for Chromium unpacked from .debs without root


def venv_python():
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def have(modules):
    import importlib.util
    return all(importlib.util.find_spec(m) is not None for m in modules)


def ensure_modules(modules):
    """Return if `modules` import here; else re-run this script with the private venv's Python."""
    if have(modules):
        return
    vp = venv_python()
    # compare prefixes, not executables: a venv's python is a symlink to the system one
    if vp.exists() and pathlib.Path(sys.prefix).resolve() != VENV.resolve():
        sys.exit(subprocess.run([str(vp)] + sys.argv).returncode)
    sys.exit(f"Missing Python packages ({', '.join(modules)}). Run scripts/setup.py first.")


def playwright_chromium():
    """Chromium downloaded by `python -m playwright install chromium` (no admin rights needed)."""
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
             os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright"),
             str(pathlib.Path.home() / ".cache" / "ms-playwright"),
             str(pathlib.Path.home() / "Library" / "Caches" / "ms-playwright")]
    # the headless shell first: it needs far fewer system libraries than full Chromium
    pats = ["chromium_headless_shell-*/chrome-*/chrome-headless-shell.exe",
            "chromium_headless_shell-*/chrome-*/chrome-headless-shell",
            "chromium-*/chrome-win*/chrome.exe", "chromium-*/chrome-linux*/chrome",
            "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
            "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"]
    for p in pats:
        hits = sorted(h for r in roots if r and os.path.isdir(r) for h in glob.glob(os.path.join(r, p)))
        if hits:
            return hits[-1]
    return None


def find_browser():
    """Path to a Chromium-based browser that can --print-to-pdf, or None."""
    env = os.environ.get("PDF_BROWSER")
    if env and pathlib.Path(env).exists():
        return env
    fixed = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ]
    for c in fixed:
        if pathlib.Path(c).exists():
            return c
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              "microsoft-edge", "microsoft-edge-stable", "msedge", "brave-browser", "chrome"):
        p = shutil.which(n)
        if p:
            return p
    return playwright_chromium()


def browser_flags():
    flags = ["--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:   # Docker / root: Chromium refuses to sandbox
        flags.append("--no-sandbox")
    return flags


def browser_env():
    """Environment for launching the browser (adds libraries unpacked by setup.py on Linux)."""
    env = dict(os.environ)
    dirs = [d for d in glob.glob(str(LIBS / "usr" / "lib" / "*-linux-gnu")) + [str(LIBS / "usr" / "lib")]
            if os.path.isdir(d)]
    dirs += [os.path.join(d, "nss") for d in dirs if os.path.isdir(os.path.join(d, "nss"))]
    if dirs:
        env["LD_LIBRARY_PATH"] = os.pathsep.join(dirs + [env.get("LD_LIBRARY_PATH", "")]).rstrip(os.pathsep)
    return env


def browser_works(browser):
    """Can this browser actually start headless? (catches missing system libraries on Linux)"""
    import tempfile
    with tempfile.TemporaryDirectory() as prof:
        try:
            r = subprocess.run([browser, *browser_flags(), f"--user-data-dir={prof}", "--dump-dom",
                                "data:text/html,<p>ok</p>"], capture_output=True, timeout=60, env=browser_env())
        except (OSError, subprocess.TimeoutExpired) as e:
            return False, str(e)
    out = r.stdout.decode("utf-8", "replace")
    return ("<p>ok</p>" in out), r.stderr.decode("utf-8", "replace")[-600:]

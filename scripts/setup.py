#!/usr/bin/env python3
"""One-time setup / health check. Idempotent; safe to run every time.

usage:  python setup.py

Checks/installs: faster-whisper, markdown-it-py, mdit-py-plugins (pip), KaTeX (npm, vendored
into ../vendor so PDFs render offline), and an Edge/Chrome browser for PDF printing.
"""
import importlib, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ok = True

for mod, pkg in [("faster_whisper", "faster-whisper"), ("markdown_it", "markdown-it-py"),
                 ("mdit_py_plugins", "mdit-py-plugins")]:
    try:
        importlib.import_module(mod); print(f"ok   {pkg}")
    except ImportError:
        print(f"inst {pkg} …")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg])
        ok &= r.returncode == 0

kdir = ROOT / "vendor" / "node_modules" / "katex"
if kdir.exists():
    print("ok   katex (vendored)")
elif shutil.which("npm"):
    print("inst katex …")
    (ROOT / "vendor").mkdir(exist_ok=True)
    r = subprocess.run("npm install --silent --no-audit --no-fund katex@0.16.11", shell=True, cwd=ROOT / "vendor")
    print("ok   katex" if kdir.exists() else "warn katex install failed – build.py will use the CDN")
else:
    print("warn npm missing – build.py will load KaTeX from the CDN (needs internet)")

sys.path.insert(0, str(ROOT / "scripts"))
from build import find_browser
try:
    print("ok   browser", find_browser())
except SystemExit as e:
    print("FAIL", e); ok = False

hub = pathlib.Path.home() / ".cache" / "huggingface" / "hub"
models = [p.name.split("--")[-1] for p in hub.glob("models--*whisper*")] if hub.exists() else []
print("ok   whisper models cached:", ", ".join(models) if models else
      "none yet (first transcription downloads ~1.6 GB for large-v3-turbo)")
print("setup ok" if ok else "setup INCOMPLETE")

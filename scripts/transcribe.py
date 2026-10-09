#!/usr/bin/env python3
"""Lecture audio -> timestamped transcript (local, offline, faster-whisper).

usage:
  python transcribe.py lecture.mp3 work/ [--lang sl] [--model large-v3-turbo]
                       [--prompt "Matematika 1: odvod, integral, limita ..."]

Writes:
  work/transcript.txt   one line per segment:  [mm:ss] text      (read this)
  work/transcript.json  segments with start/end/avg_logprob     (for spot checks)
  work/low_confidence.txt  segments Whisper itself was unsure about

Accepts mp3, m4a, wav, ogg, opus, mp4, webm … (decoded by PyAV, no ffmpeg needed).
Progress is printed every ~2 minutes of audio so a background run can be followed.
"""
import argparse, json, pathlib, sys, time

def fmt(t):
    t = int(t)
    h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def decode(path, sr=16000):
    """Any audio/video file -> mono float32 at 16 kHz. Own decoder so we don't depend on the
    PyAV version faster-whisper was written against (av>=16 broke its decode_audio)."""
    import av, numpy as np
    chunks = []
    with av.open(str(path)) as c:
        rs = av.AudioResampler(format="s16", layout="mono", rate=sr)
        for frame in c.decode(audio=0):
            for f in rs.resample(frame):
                chunks.append(f.to_ndarray().reshape(-1))
        for f in rs.resample(None):
            chunks.append(f.to_ndarray().reshape(-1))
    return np.concatenate(chunks).astype(np.float32) / 32768.0

def main():
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from _env import ensure_modules
    ensure_modules(["faster_whisper", "av", "numpy"])
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("outdir")
    ap.add_argument("--lang", default="sl", help="language code, or 'auto'")
    ap.add_argument("--model", default="large-v3-turbo",
                    help="large-v3-turbo (fast, good) | large-v3 (slowest, best) | medium | small")
    ap.add_argument("--prompt", default="",
                    help="course name + technical terms; steers spelling of jargon")
    ap.add_argument("--device", default="auto", help="auto | cpu | cuda")
    a = ap.parse_args()

    from faster_whisper import WhisperModel
    out = pathlib.Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    compute = "int8" if a.device in ("auto", "cpu") else "float16"
    print(f"loading {a.model} ({a.device}/{compute}) …", flush=True)
    model = WhisperModel(a.model, device=a.device, compute_type=compute)

    t0 = time.time()
    audio = decode(a.audio)
    segments, info = model.transcribe(
        audio,
        language=None if a.lang == "auto" else a.lang,
        initial_prompt=a.prompt or None,
        vad_filter=True,                       # skip silence / breaks – fewer hallucinations
        vad_parameters={"min_silence_duration_ms": 700},
        beam_size=5,
        condition_on_previous_text=False,      # stops repeated-phrase loops in long recordings
        temperature=(0.0, 0.2, 0.4, 0.6),
    )
    dur = info.duration
    print(f"audio {fmt(dur)}  language={info.language} (p={info.language_probability:.2f})", flush=True)

    rows, low, last_report = [], [], 0.0
    with open(out / "transcript.txt", "w", encoding="utf-8") as f:
        for s in segments:
            text = s.text.strip()
            if not text:
                continue
            f.write(f"[{fmt(s.start)}] {text}\n"); f.flush()
            rows.append(dict(start=round(s.start, 2), end=round(s.end, 2), text=text,
                             avg_logprob=round(s.avg_logprob, 3), no_speech=round(s.no_speech_prob, 3)))
            if s.avg_logprob < -1.0 or s.compression_ratio > 2.4:
                low.append(f"[{fmt(s.start)}] (logprob {s.avg_logprob:.2f}) {text}")
            if s.end - last_report > 120:
                last_report = s.end
                el = time.time() - t0
                eta = el / max(s.end, 1) * (dur - s.end)
                print(f"  {fmt(s.end)} / {fmt(dur)}   elapsed {fmt(el)}   eta {fmt(eta)}", flush=True)

    (out / "transcript.json").write_text(json.dumps(
        dict(audio=str(pathlib.Path(a.audio).resolve()), duration=dur, language=info.language,
             model=a.model, prompt=a.prompt, segments=rows), ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "low_confidence.txt").write_text("\n".join(low), encoding="utf-8")
    words = sum(len(r["text"].split()) for r in rows)
    print(f"done in {fmt(time.time() - t0)}: {len(rows)} segments, {words} words, "
          f"{len(low)} low-confidence -> {out / 'transcript.txt'}", flush=True)

if __name__ == "__main__":
    sys.exit(main())

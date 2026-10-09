# 🎓 mp3-to-pdf

**Posnetek predavanja → PDF, iz katerega se res lahko naučiš.**

Claudu pošlješ MP3 s predavanja, nazaj dobiš urejen PDF za tiskanje: formule zapisane kot prava matematika, definicije v okvirjih, do konca izpeljani zgledi, rešene naloge, označeno vse, kar je profesor rekel o izpitu, in na koncu list z vsemi formulami. Ob vsakem poglavju je časovna oznaka, da takoj najdeš pravo mesto v posnetku.

> 📄 **Primer rezultata:** [`examples/primer.pdf`](examples/primer.pdf)

---

## Zakaj ne samo »prepis«?

Navaden prepis 90-minutnega predavanja ima okoli 13.000 besed ponavljanja, »ne?« in »torej«, najpomembnejšega dela, tistega na tabli, pa v njem sploh ni. Ta skill zato ne prepisuje, ampak **rekonstruira predavanje**, kot bi ga profesor napisal:

| Navaden prepis | mp3-to-pdf |
|---|---|
| »ef od gje od iks črtica je ef črtica …« | $(f\circ g)'(x) = f'(g(x))\cdot g'(x)$ v zelenem okvirju *Formula* |
| zgled napol izpeljan, ker je bil preostanek na tabli | zgled izpeljan do konca, vsak korak z imenom pravila |
| »za domačo nalogo pa …« izgine med ostalim besedilom | okvir *Naloga* + prostor za reševanje + rešitev |
| »to bo na izpitu« se izgubi | rdeč okvir **Za izpit** s časovno oznako |
| napake prepisa (»lagranž«, »ajgen«) | popravljeni strokovni izrazi |
| nejasna mesta so tiho napačna | siv okvir *Nejasno v posnetku* + čas, da veš, kaj preveriti |

## Kaj dobiš v PDF-ju

- **Naslovnica s kazalom** (predmet, tema, predavatelj, datum, dolžina posnetka)
- **Oštevilčena poglavja** v vrstnem redu predavanja, vsako s časovno oznako `[34:12]`
- **Barvni okvirji:** Definicija · Formula · Izrek · Pravilo · Zgled · Naloga + Rešitev · Ideja · Pozor · **Za izpit** · Nejasno v posnetku
- **Prostor za reševanje** pod vsako nalogo (črte, primerno za tisk)
- **Povzetek** na koncu in **»Formule na enem mestu«**: vse formule na eni do dveh straneh, kot list za pred izpitom
- A4 in pripravljeno za tisk

## Zasebnost in cena

- 🔒 **Prepis teče lokalno na tvojem računalniku** (Whisper). Posnetek ne gre nikamor na splet.
- 💸 Prepis je zastonj. Zapiske nato napiše Claude v tvojem pogovoru, zato porabi nekaj tvoje Claude kvote.

---

## Namestitev (enkrat, ~10 minut)

### Kaj potrebuješ

| | Zakaj | Kje |
|---|---|---|
| **Claude Code** (aplikacija Claude za namizje → zavihek *Code*, ali `claude` v terminalu) | poganja skill | [claude.com/download](https://claude.com/download) |
| **Python 3.10+** | prepis in izdelava PDF-ja | [python.org](https://www.python.org/downloads/) (pri namestitvi obkljukaj *Add to PATH*) |
| **Edge ali Chrome** | tiskanje v PDF | na Windows je Edge že nameščen |
| Node.js *(neobvezno)* | formule delujejo brez interneta | [nodejs.org](https://nodejs.org) |

> ⚠️ Skill potrebuje Claude **Code** (namizna aplikacija ali terminal), ker poganja Python na tvojem računalniku. Na navadnem claude.ai v brskalniku ne deluje.

### 1. Prenesi skill

**Z gitom (priporočeno, posodobitve dobiš z `git pull`):**

```bash
git clone https://github.com/<uporabnik>/mp3-to-pdf.git ~/.claude/skills/mp3-to-pdf
```

Na Windows v PowerShellu namesto `~` uporabi `$env:USERPROFILE`.

**Brez gita:** na GitHubu klikni *Code → Download ZIP*, razširi ga in mapo preimenuj v `mp3-to-pdf`. Nato jo premakni sem:

- **Windows:** `C:\Users\<tvoje-ime>\.claude\skills\mp3-to-pdf`
- **macOS / Linux:** `~/.claude/skills/mp3-to-pdf`

Mapa `.claude` je skrita. V Raziskovalcu vklopi *Pogled → Skriti elementi* ali v naslovno vrstico prilepi `%USERPROFILE%\.claude\skills`. Če mapa `skills` ne obstaja, jo ustvari. Datoteka `SKILL.md` mora biti neposredno v mapi `mp3-to-pdf`, ne v podmapi.

### 2. Namesti knjižnice

V terminalu (PowerShell na Windows, Terminal na Macu):

```bash
python ~/.claude/skills/mp3-to-pdf/scripts/setup.py
```

Na Windows v PowerShellu namesto `~` uporabi `$env:USERPROFILE`. Na Macu uporabi `python3`. Skripta sama namesti, kar manjka, in na koncu izpiše `setup ok`.

Ob **prvem prepisu** se samodejno prenese govorni model (~1,6 GB, samo enkrat).

### 3. Preveri

Odpri Claude Code in napiši:

```
Kateri skilli so ti na voljo?
```

Na seznamu mora biti `mp3-to-pdf`.

---

## Uporaba

Pošlji posnetek in povej, za kateri predmet gre:

```
Tukaj je posnetek predavanja Matematika 1, tema odvodi: C:\Users\jaz\Downloads\mat1_predavanje5.mp3
```

Ali še krajše: samo povleci MP3 v pogovor. Skill se sproži sam.

**Za še boljši rezultat** dodaj zraven:
- 📑 **prosojnice** (PDF): formule in izrazi so potem natančni,
- 📸 **fotke table**: rešijo mesta, kjer je profesor samo pokazal »tole tukaj«,
- 🏷️ nekaj **ključnih izrazov** predmeta, da jih prepis pravilno zapiše.

### Koliko traja?

| Posnetek | Prepis (prenosnik, CPU) | Zapiski + PDF |
|---|---|---|
| 45 min | ~8–15 min | nekaj minut |
| 90 min | ~15–30 min | nekaj minut |

Prepis teče v ozadju, Claude te sproti obvešča o napredku.

### Kaj podpira

- Formati: `mp3`, `m4a` (diktafon na iPhonu), `wav`, `ogg`, `opus`, `webm`, `mp4` (video posnetek predavanja)
- Jeziki: privzeto slovenščina. Deluje tudi angleščina in ~100 drugih jezikov (»predavanje je v angleščini«).
- Vsi predmeti: matematika, fizika, statistika, programiranje (koda v blokih), ekonomija, pravo …

### Kje so rezultati?

Ob posnetku se ustvarita:

```
mat1_predavanje5.mp3
mat1_predavanje5_work/
    transcript.txt         ← celoten prepis s časi (uporaben za iskanje)
    notes.md               ← vir zapiskov (lahko popraviš in ponovno zgradiš)
    low_confidence.txt     ← mesta, kjer je bil prepis negotov
Matematika1_05_Odvodi.pdf  ← 🎯 to natisneš
```

---

## Nasveti za dober posnetek

- 🎙️ **Telefon čim bližje profesorju**, prva vrsta ali na katedri. Razdalja je največji dejavnik kakovosti.
- 🔇 Brez šumenja papirja ali tipkanja ob mikrofonu.
- ✈️ Telefon v letalskem načinu: brez motenj in brez prekinitev snemanja.
- ✅ Snemaj samo, če profesor to dovoli.

## Pogoste težave

| Težava | Rešitev |
|---|---|
| `python` ni prepoznan | Python ni v PATH. Ponovno namesti in obkljukaj *Add to PATH*, ali uporabi `py`. |
| Prepis je zelo počasen | Normalno na starejših računalnikih. Pusti, da teče v ozadju. Za hitrejši, a slabši prepis: »uporabi model small«. |
| Veliko napačnih izrazov | Claudu povej ime predmeta in nekaj ključnih izrazov ali mu daj prosojnice. |
| Formule v PDF-ju so rdeče | Claude to sam zazna in popravi. Če ostane, reci »popravi formule in ponovno zgradi PDF«. |
| PDF se ne ustvari | Potrebuješ Edge ali Chrome. Odpri `.html` datoteko ob PDF-ju in jo natisni v PDF ročno (Ctrl+P). |
| Skill se ne sproži | Napiši izrecno: »uporabi skill mp3-to-pdf«. |

## Kaj je v mapi

```
mp3-to-pdf/
├── SKILL.md                    navodila za Claude (kako iz govora narediti zapiske)
├── README.md                   ta datoteka
├── scripts/
│   ├── setup.py                namestitev in preverjanje
│   ├── transcribe.py           posnetek → prepis s časi (faster-whisper, lokalno)
│   └── build.py                zapiski → PDF (KaTeX formule, Edge/Chrome)
├── references/
│   ├── writing-rules.md        pravila: iz govora v zapiske, branje formul
│   └── content-format.md       oblika zapiskov (okvirji, formule, naloge)
├── theme/theme.css             videz PDF-ja (barve, pisave)
└── examples/                   primer zapiskov in PDF-ja
```

Želiš drugo barvo za svoj predmet? Claudu reci »uporabi zeleno barvo« (polje `accent`), ali spremeni `theme/theme.css`.

---

<sub>Prepis: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (OpenAI Whisper large-v3-turbo) · Formule: [KaTeX](https://katex.org) · Zapiski: Claude. Zapiski so pripomoček za učenje: preveri označena nejasna mesta in jih ne jemlji kot nadomestilo za predavanja.</sub>

# mp3-to-pdf

**Posnetek predavanja → PDF, iz katerega se res lahko naučiš.**

Claudu pošlješ MP3 s predavanja, nazaj dobiš urejen PDF za tiskanje: formule zapisane kot prava matematika, definicije v okvirjih, do konca izpeljani zgledi, rešene naloge, označeno vse, kar je profesor rekel o izpitu, in na koncu list z vsemi formulami. Ob vsakem poglavju je časovna oznaka, da takoj najdeš pravo mesto v posnetku.

> **Primer rezultata:** [`examples/primer.pdf`](examples/primer.pdf)

---

## Zakaj ne samo »prepis«?

Navaden prepis 90-minutnega predavanja ima okoli 13.000 besed ponavljanja, »ne?« in »torej«, najpomembnejšega dela, tistega na tabli, pa v njem sploh ni. Ta skill zato ne prepisuje, ampak **rekonstruira predavanje**, kot bi ga profesor napisal:

| Navaden prepis                                       | mp3-to-pdf                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| »ef od gje od iks črtica je ef črtica …«             | $(f\circ g)'(x) = f'(g(x))\cdot g'(x)$ v zelenem okvirju _Formula_ |
| zgled napol izpeljan, ker je bil preostanek na tabli | zgled izpeljan do konca, vsak korak z imenom pravila               |
| »za domačo nalogo pa …« izgine med ostalim besedilom | okvir _Naloga_ + prostor za reševanje + rešitev                    |
| »to bo na izpitu« se izgubi                          | rdeč okvir **Za izpit** s časovno oznako                           |
| napake prepisa (»lagranž«, »ajgen«)                  | popravljeni strokovni izrazi                                       |
| nejasna mesta so tiho napačna                        | siv okvir _Nejasno v posnetku_ + čas, da veš, kaj preveriti        |

## Kaj dobiš v PDF-ju

- **Naslovnica s kazalom** (predmet, tema, predavatelj, datum, dolžina posnetka)
- **Oštevilčena poglavja** v vrstnem redu predavanja, vsako s časovno oznako `[34:12]`
- **Barvni okvirji:** Definicija · Formula · Izrek · Pravilo · Zgled · Naloga + Rešitev · Ideja · Pozor · **Za izpit** · Nejasno v posnetku
- **Prostor za reševanje** pod vsako nalogo (črte, primerno za tisk)
- **Povzetek** na koncu in **»Formule na enem mestu«**: vse formule na eni do dveh straneh, kot list za pred izpitom
- A4 in pripravljeno za tisk

## Zasebnost in cena

- **Prepis teče lokalno na tvojem računalniku** (Whisper). Posnetek ne gre nikamor na splet.
- Prepis je zastonj. Zapiske nato napiše Claude v tvojem pogovoru, zato porabi nekaj tvoje Claude kvote.

---

## Namestitev (enkrat, ~5 minut)

### Kaj potrebuješ

|                                                                       | Zakaj                     | Kje                                                                                      |
| --------------------------------------------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------- |
| **Aplikacija Claude za namizje** (zavihek _Code_) ali **Claude Code** | poganja skill             | [claude.com/download](https://claude.com/download)                                       |
| **Python 3.10+**                                                      | prepis in izdelava PDF-ja | [python.org](https://www.python.org/downloads/) (pri namestitvi obkljukaj _Add to PATH_) |
| **Edge ali Chrome**                                                   | tiskanje v PDF            | na Windows je Edge že nameščen                                                           |

> **Pozor:** skill uporabljaj v zavihku **Code** (ali v Claude Code v terminalu), ker prepis teče na tvojem računalniku. V navadnem klepetu na claude.ai v brskalniku ne deluje.

### 1. Prenesi skill

Prenesi **[mp3-to-pdf.skill](https://github.com/<uporabnik>/mp3-to-pdf/releases/latest/download/mp3-to-pdf.skill)**.

### 2. Naloži ga v Claude

V aplikaciji Claude odpri **Nastavitve → Capabilities → Skills** (v novejših verzijah **Customize → Skills**), klikni **Upload skill** in izberi preneseni `mp3-to-pdf.skill`. Skill se prikaže na seznamu, preveri samo, da je vklopljen.

Če ti kdo pošlje `mp3-to-pdf.skill` kar v pogovoru s Claudom, je še lažje: na kartici datoteke klikni **Save skill**.

To je vse. Ob prvi uporabi Claude sam namesti, kar še manjka (Python knjižnice, KaTeX za formule), in prenese govorni model (~1,6 GB, samo enkrat).

### Posodobitev

Prenesi nov `mp3-to-pdf.skill` s iste povezave, v Skills izbriši staro verzijo in naloži novo.

<details>
<summary>Namestitev z gitom (za razvijalce)</summary>

```bash
git clone https://github.com/<uporabnik>/mp3-to-pdf.git ~/.claude/skills/mp3-to-pdf
```

Na Windows v PowerShellu namesto `~` uporabi `$env:USERPROFILE`. Posodobitev: `git pull` v tej mapi. Tak skill vidi samo Claude Code na tem računalniku.

</details>

---

## Uporaba

Pošlji posnetek in povej, za kateri predmet gre:

```
Tukaj je posnetek predavanja Matematika 1, tema odvodi: C:\Users\jaz\Downloads\mat1_predavanje5.mp3
```

Ali še krajše: samo povleci MP3 v pogovor. Skill se sproži sam.

**Za še boljši rezultat** dodaj zraven:

- **prosojnice** (PDF): formule in izrazi so potem natančni,
- **fotke table**: rešijo mesta, kjer je profesor samo pokazal »tole tukaj«,
- nekaj **ključnih izrazov** predmeta, da jih prepis pravilno zapiše.

### Koliko traja?

| Posnetek | Prepis (prenosnik, CPU) | Zapiski + PDF |
| -------- | ----------------------- | ------------- |
| 45 min   | ~8–15 min               | nekaj minut   |
| 90 min   | ~15–30 min              | nekaj minut   |
| 180 min  | ~40–60 min              | nekoliko dlje |

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
Matematika1_05_Odvodi.pdf  ← to natisneš
```

---

## Pogoste težave

| Težava                    | Rešitev                                                                                                           |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `python` ni prepoznan     | Python ni v PATH. Ponovno namesti in obkljukaj _Add to PATH_, ali uporabi `py`.                                   |
| Prepis je zelo počasen    | Normalno na starejših računalnikih. Pusti, da teče v ozadju. Za hitrejši, a slabši prepis: »uporabi model small«. |
| Veliko napačnih izrazov   | Claudu povej ime predmeta in nekaj ključnih izrazov ali mu daj prosojnice.                                        |
| Formule v PDF-ju so rdeče | Claude to sam zazna in popravi. Če ostane, reci »popravi formule in ponovno zgradi PDF«.                          |
| PDF se ne ustvari         | Potrebuješ Edge ali Chrome. Odpri `.html` datoteko ob PDF-ju in jo natisni v PDF ročno (Ctrl+P).                  |
| Nalaganje skilla ne uspe  | Uporabi `mp3-to-pdf.skill` s povezave zgoraj (ne GitHubovega _Code → Download ZIP_). |
| Skill se ne sproži        | Napiši izrecno: »uporabi skill mp3-to-pdf«.                                                                       |

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

<sub>Prepis: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (OpenAI Whisper large-v3-turbo) · Formule: [KaTeX](https://katex.org) · Zapiski: Claude.</sub>

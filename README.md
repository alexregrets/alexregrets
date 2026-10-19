<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cournot-dark.svg">
  <img src="assets/cournot-light.svg" alt="Cournot best-response diagram, with reaction functions meeting at Nash equilibrium" width="760">
</picture>

# Alexander Sotnik

### Economics × code

Economics undergraduate at the Financial University, Moscow · Class of 2028

[![Python](https://img.shields.io/badge/Python-2b2b2b?style=flat-square&logo=python&logoColor=ffd43b)](https://www.python.org/)
[![Econometrics](https://img.shields.io/badge/Econometrics-2b2b2b?style=flat-square&logo=wolfram&logoColor=d9a441)](https://github.com/alexregrets)
[![Moscow](https://img.shields.io/badge/Moscow-2b2b2b?style=flat-square&logo=googlemaps&logoColor=d9a441)](https://github.com/alexregrets)

</div>

---

I build things at the seam between econometrics and code. The combination is the point: I want to understand both how a system works and how to measure what it does.

Heading toward **causal inference**. Estimating a coefficient and identifying an effect are different jobs.

## Selected work

<table>
<tr>
<td width="50%" valign="top">

### [Econometrics Championship](https://github.com/alexregrets/econ-championship)

A Cournot oligopoly tournament that leaves a panel dataset behind for students to analyze.

&#96;Python&#96; &#96;SQLAlchemy&#96; &#96;aiogram&#96; &#96;Streamlit&#96;

</td>
<td width="50%" valign="top">

### [quiet-transcript](https://github.com/alexregrets/quiet-transcript)

A desktop app that turns audio, video and links into clean Markdown notes.

&#96;Tauri&#96; &#96;React&#96; &#96;Rust&#96;

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [university-analysis](https://github.com/alexregrets/university-analysis)

14.5k observations × 27 features. OLS and a difference-in-differences analysis of COVID.

&#96;Python&#96; &#96;statsmodels&#96;

</td>
<td width="50%" valign="top">

### [uni_mail_bot](https://github.com/alexregrets/uni_mail_bot)

Forwards a shared university mailbox into Telegram. Running on a VPS.

&#96;Python&#96; &#96;aiogram&#96;

</td>
</tr>
</table>

<details>
<summary><b>More projects</b></summary>

<br>

| Project | What it does | Stack |
|---|---|---|
| [caviarshow](https://github.com/alexregrets/caviarshow) | Bilingual, dual-theme landing page for the family business | HTML · CSS · JS |
| [sc-linkbot](https://github.com/alexregrets/sc-linkbot) | SoundCloud link in, tagged MP3 out | Python |
| [learning](https://github.com/alexregrets/learning) | Open log of relearning to program, failures included | — |

</details>

## Inside the tournament

<details>
<summary><b>How the Cournot game becomes an econometrics lab</b></summary>

<br>

Student teams run firms in a shared Cournot market for several rounds. Linear inverse demand &#96;P = a − b·Q&#96;, interior Nash at &#96;q* = (a − c) / b(n+1)&#96;, plus an asymmetric engine for firm-specific costs. Market parameters are inverted from the Russian oil market in 2013, so the numbers have a source.

Every round writes one row per team. By the end, the course has a panel of teams × rounds, and students run regressions on data they generated themselves. They know the data-generating process because they were inside it.

Mechanics switch on at chosen rounds for chosen teams, which makes treatment timing a design decision rather than something to recover from noise.

Each student has a role, sees only part of the picture and holds a personal KPI that conflicts with the others. Marketing is paid on market share; finance on margin. Someone has to settle the argument instead of averaging it.

**248 tests.** Everything under &#96;core/&#96; is pure and deterministic, written test-first, because a plausible-but-wrong formula looks exactly like a correct one.

</details>

## How I work

- Nothing counts without a run. Predict the output, run the code, then reconcile the difference.
- One open problem at a time. The failure mode was never difficulty; it was holding three half-finished things at once.
- In &#96;learning/&#96;, I track hours spent writing code separately from hours a model spent writing it. Both matter; they measure different things.

## Current focus

- Econometrics Championship
- Causal inference: identification, IV, DiD, RDD
- A paper on deliberate AI use among university students
- Preparing for a master's in Europe, 2028

---

<div align="center">

Moscow · [Telegram](https://t.me/rutorsup) · sanek2OO6@mail.ru

</div>

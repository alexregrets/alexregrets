<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cournot-dark.svg">
  <img src="assets/cournot-light.svg" alt="Cournot best-response diagram: two reaction functions crossing at the Nash equilibrium" width="100%">
</picture>

### Alexander Sotnik

Economics undergraduate at the Financial University, Moscow. Class of 2028.

I build things at the seam between econometrics and code. Not an ML engineer who
picked up some economics, and not an economist who picked up some Python — the
combination is the point, and it is rare because it costs you both halves.
Heading for causal inference: estimating a coefficient and identifying an effect
are different jobs, and only one of them is hard to hire for.

---

| | | |
|---|---|---|
| [**econ-championship**](https://github.com/alexregrets/econ-championship) | Cournot oligopoly tournament that generates a panel dataset for an econometrics course to regress on | Python · SQLAlchemy · aiogram · Streamlit |
| [**quiet-transcript**](https://github.com/alexregrets/quiet-transcript) | Desktop app turning audio, video and links into clean Markdown notes | Tauri · React · Rust |
| [**university-analysis**](https://github.com/alexregrets/university-analysis) | 14.5k observations × 27 features; OLS and a difference-in-differences read on COVID | Python · statsmodels |
| [**uni_mail_bot**](https://github.com/alexregrets/uni_mail_bot) | IMAP poller forwarding a shared university mailbox into Telegram. Live on a VPS | Python · aiogram |
| [**caviarshow**](https://github.com/alexregrets/caviarshow) | Landing page for the family business. Bilingual, dual-theme, no build step | HTML · CSS · JS |
| [**sc-linkbot**](https://github.com/alexregrets/sc-linkbot) | SoundCloud link in, tagged MP3 out | Python |
| [**learning**](https://github.com/alexregrets/learning) | Open log of relearning to program, failures included | — |

---

<details>
<summary><b>What the tournament actually does</b></summary>

<br>

Student teams run firms in a shared Cournot market for several rounds. Linear
inverse demand `P = a − b·Q`, interior Nash at `q* = (a − c) / b(n+1)`, plus an
asymmetric engine for firm-specific costs. Market parameters are not invented —
they are inverted out of the Russian oil market in 2013, so the numbers have a
source.

Every round writes one row per team. By the end the course holds a panel of
teams × rounds, and the same students then have to run regressions on data they
generated themselves, knowing exactly how the data-generating process works
because they were inside it.

Mechanics switch on at chosen rounds for chosen teams, which makes treatment
timing a design decision rather than something to be recovered from noise. That
is the part I care about.

Each student holds a role seeing only a slice of the truth, with a personal KPI
that conflicts with the others — marketing is paid on market share, finance on
margin. Someone has to settle the argument instead of averaging it.

248 tests. Everything under `core/` is pure and deterministic, written test-first,
because a plausible-but-wrong formula looks exactly like a correct one.

</details>

<details>
<summary><b>How I work</b></summary>

<br>

Nothing counts without a run. Correct reasoning plus an inability to write the
code means the topic is not known — predict the output first, then run it, then
reconcile the difference. The gap is the part worth studying.

One open problem at a time. The failure mode was never difficulty, it was
holding three half-finished things at once.

`learning/` tracks two separate columns: hours I spent writing code, and hours
a model spent writing it for me. The second is legitimate and it does not make
me better at the first, so mixing them makes the record worthless.

</details>

<details>
<summary><b>Currently</b></summary>

<br>

- Getting the tournament to a working prototype for the September 2026 semester
- Causal inference: identification, IV, DiD, RDD
- A paper on deliberate AI use among university students
- Preparing for a masters in Europe, 2028

</details>

---

Moscow · [@rutorsup](https://t.me/rutorsup) · sanek2OO6@mail.ru

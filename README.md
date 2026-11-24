# Hypothesis Ledger

**An autonomous quantitative research agent that searched 11,514 pre-registered
hypotheses for a tradable edge and found none — and the interesting part is why
that zero is trustworthy.**

→ **[Open the live page](https://maugarza2809-crypto.github.io/quant-research-agent/)**

Most backtesting write-ups show you the one strategy that worked. This one shows
the apparatus that makes it impossible to fool yourself, and then reports the
negative result it produced. The search is closed; what is here is its record, plus
a bench and a terminal that still run on the same engine and the same data. Three tabs:

| Tab | What it is |
|---|---|
| **Method** | Nine interactive figures reconstructing the measurements: the multiplicity bar, the cost law, the selection penalty, effective replication, the bug ledger |
| **Test bench** | A backtest engine running in your browser over 547,569 real H1 bars — build a strategy from 28 indicators, measure it, then put it through Monte Carlo, a parameter surface, a volatility surface and seven statistical critics |
| **Terminal** | Order flow, a liquidity map, an implied-volatility surface and dealer gamma, replayed over real broker candles |

---

## The headline numbers

| | |
|---|---|
| Hypotheses pre-registered | **11,514** — each with a written prediction and a hash, before the first number |
| Configurations measured | **50,794** — the N that sets the multiplicity bar |
| Bailey bar for that N | **t ≥ 4.24**, not the customary t ≈ 2 |
| Survivors | **0** |

The bar is the Deflated Sharpe Ratio of
[Bailey & López de Prado (2014)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551):

```
SR₀ = √Var(SR) · [ (1−γ)·Z⁻¹(1−1/N) + γ·Z⁻¹(1−1/(N·e)) ]
```

with γ the Euler–Mascheroni constant and Var(SR) measured at 0.005706 rather than
approximated by 1/T — the 1/T shortcut understates the bar. The best Sharpe per
trade the search ever produced was 0.0149, a long way under what chance alone
yields at that N. The page lets you move N and T and watch the bar move.

## Three results worth more than the zero

**The law of cost.** Across fourteen instruments, net performance tracks execution
cost almost perfectly: `Rx = −1.16·cost + 0.0046`, R² = 0.993, replicated at
R² = 0.874 on two independent sweeps. Hand the cost back and all fourteen points
collapse onto zero. The signal is not *below* the friction — it is not there.

**Picking the best is worse than picking at random.** Ranking 3,528 rules by a long
in-sample period and keeping the top k gives worse out-of-sample returns than
drawing one at random. Selection is not free.

**Fourteen instruments are not fourteen tests.** At a measured mean correlation of
ρ = 0.423, `n_eff = k/(1+(k−1)ρ)` makes fourteen instruments worth **2.2** independent
ones. Under an independence assumption the same data looked like 129 tests.

## Discipline that makes the zero mean something

- **Pre-registration.** Every hypothesis is written down with its prediction and
  hashed before it is measured. You cannot retrofit a story onto a result.
- **A three-way partition.** In-sample up to 2021-12-31, search from 2022-01-01 to
  2026-02-28, and a sealed slice from 2026-03-01 that each hypothesis may touch
  **once** in its life.
- **A frozen engine.** The agent proposed signals; it could not touch the cost model
  or the execution assumptions.
- **Multiplicity under dependence.** Romano–Wolf and SPA over a block bootstrap,
  because the hypotheses are correlated and treating them as independent is how a
  search finds "edges" that are not there.
- **A published bug ledger.** Six measurement bugs that each inflated a result,
  what they did, and what the number became once fixed. They are on the page.

## The data is real

547,569 H1 bars across 22 instruments — indices, currencies, metals, crypto and
equities — exported from MetaTrader 5, 2021 to 2026, plus nine months of raw M5 for
the terminal. No synthetic prices, no vendor proxy. Every execution cost carries its
provenance: *measured* from the broker's own spread, *declared* from a conservative
table, or *assumed* where no measurement exists — and the assumed ones are editable
in the interface, because they should be argued with.

What is modelled is labelled as modelled: a CFD publishes no option chain and no
per-level prints, so the implied-volatility surface and the buy/sell split inside a
candle are stated models over real underlying data. The volume is MetaTrader's tick
volume — real and measured, but not traded contracts.

## Running it

The page is a single self-contained HTML file. No build step, no dependencies, no
server-side anything.

```bash
git clone https://github.com/maugarza2809-crypto/quant-research-agent.git
cd quant-research-agent
python3 -m http.server 8000     # any static server; a file:// open blocks the fetches
```

Then open <http://localhost:8000>.

Saving and comparing strategies needs the Claude Artifacts database and is inert on a
static host — the panel hides itself rather than failing. Everything else, including
every backtest and the whole terminal, runs locally in the browser.

## Layout

```
index.html        the page, generated — do not edit by hand
src/page.html     the real source (the body published as a Claude Artifact)
data/             indice.json + one file per instrument, lazily fetched
tools/build.py    src/page.html → index.html: adds the document skeleton, repoints the fetches
tools/extract.py  broker M5 → compact H1, delta-encoded in integer ticks
tools/extract_term.py   nine months of raw M5 for the terminal
```

`tools/extract*.py` need pandas and NumPy and the broker's own CSV exports, which are
not in the repo. The JSON they produce is.

## Why there is no strategy here

Because the search did not find one, and the system is built so it cannot pretend
otherwise. What this project demonstrates is the apparatus: pre-registration,
multiplicity control under dependence, a single-use holdout, self-audit, and the
habit of publishing the defects. The zero is the result, not a failure to report one.

## License

MIT — see [LICENSE](LICENSE).

"""extract_term.py — raw M5 for the terminal, one file per instrument.

The test bench uses H1 from 2021 to 2026 because it needs history; the terminal
does not: it replays a few hundred bars and aggregates them on the fly. From the last
few months of M5 the browser can build M5, M10, M15, M30, H1, H2 and H4. Nine months
of M5 for an index weigh 1.2 MB; the full 5.6 years would weigh 7 MB per instrument
and add nothing here.
"""
import os, json
import pandas as pd, numpy as np

SRC = os.path.expanduser("~/trading ago/mql5/datos")
OUT = os.path.dirname(os.path.abspath(__file__))
MESES = 9
SIMS = [("US100.cash", 0.01,  "index"),
        ("GER40.cash", 0.01,  "index"),
        ("US500.cash", 0.01,  "index"),
        ("XAUUSD",     0.01,  "metal"),
        ("EURUSD",  0.00001,  "fx"),
        ("BTCUSD",     0.01,  "crypto"),
        ("NVDA",       0.01,  "stock")]

idx, peso = {}, 0
for SIM, TICK, CLASE in SIMS:
    f = os.path.join(SRC, f"barras_{SIM}_M5.csv")
    if not os.path.exists(f):
        print(f"{SIM:12s} NO ESTÁ"); continue
    d = pd.read_csv(f)
    t = pd.to_datetime(d["datetime"], format="%Y.%m.%d %H:%M:%S")
    d = d.assign(t=t).set_index("t").sort_index()
    d = d[~d.index.duplicated(keep="first")]
    d = d[d.index >= d.index.max() - pd.DateOffset(months=MESES)]
    d = d[d["volume"] > 0]
    if len(d) < 3000:
        print(f"{SIM:12s} only {len(d)} bars, skipped"); continue
    o  = np.round(d.open.to_numpy()/TICK).astype(np.int64)
    hi = np.round(d.high.to_numpy()/TICK).astype(np.int64)
    lo = np.round(d.low.to_numpy()/TICK).astype(np.int64)
    c  = np.round(d.close.to_numpy()/TICK).astype(np.int64)
    v  = d.volume.to_numpy().astype(np.int64)
    ts = d.index.values.astype("datetime64[s]").astype("int64")
    prev = np.concatenate([[c[0]], c[:-1]])
    pq = {"tick":TICK,"tf":300,"t0":int(ts[0]),"n":int(len(d)),"base":int(c[0]),
          "v0":int(v[0]),
          "dt":",".join(map(str,(np.diff(ts,prepend=ts[0])//300).tolist())),
          "o":",".join(map(str,(o-prev).tolist())),
          "h":",".join(map(str,(hi-o).tolist())),
          "l":",".join(map(str,(lo-o).tolist())),
          "c":",".join(map(str,(c-o).tolist())),
          "v":",".join(map(str,np.diff(v,prepend=v[0]).tolist()))}
    p = os.path.join(OUT, f"t_{SIM}.json")
    json.dump(pq, open(p,"w"), separators=(",",":"))
    kb = os.path.getsize(p)/1024; peso += kb
    idx[SIM] = {"clase":CLASE,"n":int(len(d)),
                "desde":str(d.index[0].date()),"hasta":str(d.index[-1].date())}
    print(f"{SIM:12s} {len(d):>7,} velas M5  {d.index[0].date()} → {d.index[-1].date()}  {kb:>7.0f} kB")

json.dump(idx, open(os.path.join(OUT,"term.json"),"w"),
          separators=(",",":"), ensure_ascii=False)
print(f"\n{len(idx)} instrumentos · {peso/1024:.2f} MB (carga perezosa, uno cada vez)")

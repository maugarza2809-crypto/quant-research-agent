"""extract.py — the broker's M5 candles → compact H1, one file per instrument.

Encoding: prices as integer ticks, delta against the previous close; time in hours
since the previous bar. Almost every number fits in 2-4 characters.

Lazy loading: `indice.json` carries only the catalogue (about 2 kB) and each
instrument travels in its own file, fetched when it is picked. That is how twenty fit
without the page load paying for the nineteen nobody opens.

COST. It is the number that rules everything else — the project's regression gives
R²=0.993 of Rx against cost — which is why every figure carries its provenance:
  measured · spread sampled from the broker during the project
  declared · conservative table from the project's own cost module
  assumed  · no measurement; in equities the round turn runs from 1.3 to 58 bp, and
             what goes here is the 8 bp the agent used by default for an unknown
             symbol. It is editable in the interface, and worth moving.
"""
import os, json
import pandas as pd, numpy as np

SRC = os.path.expanduser("~/trading ago/mql5/datos")
OUT = os.path.dirname(os.path.abspath(__file__))
DESDE = "2021-01-01"

# (symbol, tick, class, round-turn cost in bp, provenance)
SIMS = [
 ("US100.cash", 0.01,  "index", 0.498, "measured"),
 ("US500.cash", 0.01,  "index", 0.68,  "declared"),
 ("US30.cash",  0.01,  "index", 0.68,  "declared"),
 ("GER40.cash", 0.01,  "index", 0.62,  "measured"),
 ("UK100.cash", 0.01,  "index", 0.90,  "declared"),
 ("JP225.cash", 0.01,  "index", 0.90,  "declared"),
 ("EURUSD",  0.00001,  "fx",     0.387, "measured"),
 ("GBPUSD",  0.00001,  "fx",     0.60,  "declared"),
 ("USDJPY",    0.001,  "fx",     0.60,  "declared"),
 ("USDCHF",  0.00001,  "fx",     0.60,  "declared"),
 ("AUDUSD",  0.00001,  "fx",     0.60,  "declared"),
 ("USDCAD",  0.00001,  "fx",     0.60,  "declared"),
 ("XAUUSD",     0.01,  "metal",  1.034, "measured"),
 ("XAGUSD",    0.001,  "metal",  2.50,  "declared"),
 ("BTCUSD",     0.01,  "crypto", 8.00,  "assumed"),
 ("ETHUSD",     0.01,  "crypto", 6.00,  "declared"),
 ("SOLUSD",     0.01,  "crypto", 12.0,  "assumed"),
 ("NVDA",       0.01,  "stock", 8.00,  "assumed"),
 ("AAPL",       0.01,  "stock", 8.00,  "assumed"),
 ("TSLA",       0.01,  "stock", 8.00,  "assumed"),
 ("META",       0.01,  "stock", 8.00,  "assumed"),
 ("AMZN",       0.01,  "stock", 8.00,  "assumed"),
]

def cargar(s):
    d = pd.read_csv(os.path.join(SRC, f"barras_{s}_M5.csv"))
    t = pd.to_datetime(d["datetime"], format="%Y.%m.%d %H:%M:%S")
    d = d.assign(t=t).set_index("t").sort_index()
    d = d[~d.index.duplicated(keep="first")]
    d = d[d.index >= DESDE]
    h = d.resample("1h").agg({"open":"first","high":"max","low":"min",
                              "close":"last","volume":"sum"}).dropna()
    return h[h.volume > 0]

idx, total, peso = {}, 0, 0
for s, tick, clase, coste, orig in SIMS:
    f = os.path.join(SRC, f"barras_{s}_M5.csv")
    if not os.path.exists(f):
        print(f"{s:12s} NO ESTÁ"); continue
    h = cargar(s)
    if len(h) < 2000:
        print(f"{s:12s} only {len(h)} bars, skipped"); continue
    o  = np.round(h.open.to_numpy()/tick).astype(np.int64)
    hi = np.round(h.high.to_numpy()/tick).astype(np.int64)
    lo = np.round(h.low.to_numpy()/tick).astype(np.int64)
    c  = np.round(h.close.to_numpy()/tick).astype(np.int64)
    ts = h.index.values.astype("datetime64[s]").astype("int64")
    dth = np.diff(ts, prepend=ts[0])//3600
    prev = np.concatenate([[c[0]], c[:-1]])
    vol = h.volume.to_numpy().astype(np.int64)      # volumen de TICK, no negociado
    pq = {"tick":tick,"t0":int(ts[0]),"n":int(len(h)),"base":int(c[0]),
          "v":",".join(map(str, np.diff(vol, prepend=vol[0]).tolist())),
          "v0":int(vol[0]),
          "dt":",".join(map(str, dth.tolist())),
          "o":",".join(map(str, (o-prev).tolist())),
          "h":",".join(map(str, (hi-o).tolist())),
          "l":",".join(map(str, (lo-o).tolist())),
          "c":",".join(map(str, (c-o).tolist()))}
    p = os.path.join(OUT, f"d_{s}.json")
    json.dump(pq, open(p,"w"), separators=(",",":"))
    kb = os.path.getsize(p)/1024; peso += kb; total += len(h)
    idx[s] = {"clase":clase,"coste_pb":coste,"origen":orig,"tick":tick,
              "n":int(len(h)),"desde":str(h.index[0].date()),"hasta":str(h.index[-1].date())}
    print(f"{s:12s} {len(h):>7,} velas  {h.index[0].date()} → {h.index[-1].date()}"
          f"  {kb:>7.0f} kB  {coste:>6.3f} pb {orig}")

json.dump(idx, open(os.path.join(OUT,"indice.json"),"w"),
          separators=(",",":"), ensure_ascii=False)
print(f"\n{len(idx)} instrumentos · {total:,} velas H1 · {peso/1024:.2f} MB en total")
print(f"indice.json {os.path.getsize(os.path.join(OUT,'indice.json'))/1024:.1f} kB")

"""Helium chrome color (dark: Secondary T12, light: Neutral T98) per Material variant, seeded with each Scene theme background.
Usage: python3 material-vs-themes.py Themes"""
import json,glob,os,sys,statistics
sys.path.insert(0,os.path.dirname(__file__))
from material_roles import palettes, argb, hexs, dE, lab
V=["tonal","neutral","vibrant","expressive"]
rows=[];agg={(v,m):[] for v in V for m in ("dark","light")}
for f in sorted(glob.glob(sys.argv[1]+"/*/theme.json")):
    t=json.load(open(f))
    for mode,var in t.get("variants",{}).items():
        bg=var["palette"]["background"]; out=[]
        for v in V:
            q=palettes(bg,v)
            chrome=hexs(q['s'].tone(12)) if mode=="dark" else hexs(q['n'].tone(98))
            d=dE(chrome,bg); agg[(v,mode)].append(d); out.append(f"{v[:4]} {chrome} {d:4.1f}")
        rows.append(f"{os.path.basename(os.path.dirname(f)):14} {mode:5} bg {bg}  T{lab(bg)[0]:3.0f} | "+" | ".join(out))
print("\n".join(rows))
for k,v in agg.items(): print(k, "median dE %.1f  max %.1f  n=%d"%(statistics.median(v),max(v),len(v)))

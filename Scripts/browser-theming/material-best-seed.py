"""Best seed role and Material variant per Scene theme (lowest dE to the background).
Usage: python3 material-best-seed.py Themes"""
import json,glob,os,sys,statistics,collections
sys.path.insert(0,os.path.dirname(__file__))
from material_roles import palettes, hexs, dE
V=["tonal","neutral","vibrant","expressive"]; R=["background","surface","overlay","border","accent","muted"]
best={"dark":[],"light":[]}; pick=collections.Counter(); fixed=collections.defaultdict(list)
for f in sorted(glob.glob(sys.argv[1]+"/*/theme.json")):
    t=json.load(open(f))
    for mode,var in t["variants"].items():
        p=var["palette"]; bg=p["background"]; cands=[]
        for r in R:
            for v in V:
                q=palettes(p[r],v); c=hexs(q['s'].tone(12)) if mode=="dark" else hexs(q['n'].tone(98))
                d=dE(c,bg); cands.append((d,r,v,c)); fixed[(mode,r,v)].append(d)
        d,r,v,c=min(cands); best[mode].append(d); pick[(mode,r,v)]+=1
for m in best: print(m,"oracle median dE %.1f max %.1f"%(statistics.median(best[m]),max(best[m])))
print(pick.most_common(8))
for m in ("dark","light"):
    print(m, sorted(((statistics.median(v),k[1],k[2]) for k,v in fixed.items() if k[0]==m))[:5])

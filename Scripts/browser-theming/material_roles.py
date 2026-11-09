"""Chromium 157 Material roles for a seed color (ui/color/dynamic_color/palette_factory.cc, sys_color_mixer.cc).
Usage: python3 material_roles.py "#RRGGBB"   (needs: pip install materialyoucolor)"""
import sys
from materialyoucolor.hct import Hct
from materialyoucolor.palettes.tonal_palette import TonalPalette
def hexs(a): return "#%06X" % (a & 0xFFFFFF)
def argb(h): return 0xFF000000 | int(h.lstrip('#'),16)
def lookup(m, h):
    ks=sorted(m); 
    for k in ks:
        if h < k: return m[k]
    return m[ks[0]]
def palettes(seed, variant):
    hct=Hct.from_int(argb(seed)); h=hct.hue
    P=lambda hue,c: TonalPalette.from_hue_and_chroma(hue % 360, c)
    if variant=="tonal": return dict(p=P(h,40),s=P(h,16),n=P(h,6))
    if variant=="neutral":
        c = 12 if h<260 else (20 if h<315 else 12)  # flat_map lower_bound: first key >= hue
        return dict(p=P(h,c),s=P(h,8),n=P(h,2))
    if variant=="vibrant": return dict(p=P(h,200),s=P(h+lookup({0:18,41:15,61:10,101:12,131:15,181:18,251:15,301:12,360:12},h),24),n=P(h,8))
    if variant=="expressive": return dict(p=P(h-90,40),s=P(h+lookup({0:45,21:95,51:45,121:20,151:45,191:90,271:45,321:45,360:45},h),24),n=P(h,8))
def roles(seed, variant, dark):
    q=palettes(seed,variant)
    if dark: return dict(header=q['s'].tone(12), toolbar=q['s'].tone(25), omnibox=q['s'].tone(15))
    return dict(header=q['s'].tone(90), toolbar=q['n'].tone(98), omnibox=q['n'].tone(94))
def lab(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    X=(0.4124*c[0]+0.3576*c[1]+0.1805*c[2])/0.95047;Y=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];Z=(0.0193*c[0]+0.1192*c[1]+0.9505*c[2])/1.08883
    f=lambda t:t**(1/3) if t>0.008856 else 7.787*t+16/116
    return 116*f(Y)-16,500*(f(X)-f(Y)),200*(f(Y)-f(Z))
def dE(a,b): return sum((x-y)**2 for x,y in zip(lab(a),lab(b)))**.5
if __name__=="__main__":
    seed=sys.argv[1]; h=Hct.from_int(argb(seed)); print(seed, "hue %.0f chroma %.0f tone %.0f"%(h.hue,h.chroma,h.tone))
    for v in ["tonal","neutral","vibrant","expressive"]:
        for d in (False,True):
            print(f"  {v:10} {'dark ' if d else 'light'}", {k:hexs(x) for k,x in roles(seed,v,d).items()})

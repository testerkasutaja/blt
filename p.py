from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint

m = analyze('tõrjumine')
pprint(m)

p=analyze('dein')
pprint(p)

k = analyze('tõrjuvaks')
pprint(k)

h = analyze('aber')
pprint(h)

from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint

m = analyze('1940.')
pprint(m)

p=analyze('puudesse')
pprint(p)

k = analyze('sai')
pprint(k)

pprint(synthesize('tema', form = 'sg ad'))

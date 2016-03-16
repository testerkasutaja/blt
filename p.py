from pyvabamorf import analyze
from pyvabamorf import synthesize
from pprint import pprint

m = analyze('...')
pprint(m)

p=analyze('puudesse')
pprint(p)

k = analyze('sai')
pprint(k)

pprint(synthesize('tema', form = 'sg ad'))

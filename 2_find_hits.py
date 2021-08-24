"""
Makes index-time maps of bursts.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

scannrs_111_200 = range(74,139+1)
scannrs_220 = range(180, 204+1)

# lists of tuples (scannr, repeat)
hits_111 = []
hits_200 = []
hits_220 = []

def find_hits(data, coarse=10, ratio=50):
    # finds hits from a map of maximum masked-frame values,
    # shaped as (repeat, burst index)
    assert (data.shape[-1] % coarse == 0)
    chunked = np.reshape(data, (data.shape[0], -1, coarse)).sum(axis=-1)
    maxima = chunked.max(axis=1)
    baselines = np.median(chunked, axis=1)
    hits = np.where(maxima / baselines > ratio)[0]
    return list(hits)

for i, scannr in enumerate(scannrs_111_200[0:]):
    dct = np.load('map_%u.npz'%scannr)
    data111 = dct['data111']
    data200 = dct['data200']
    for h in find_hits(data111, ratio=140):
        hits_111.append((scannr, h))
    for h in find_hits(data200, ratio=320):
        hits_200.append((scannr, h))

for i, scannr in enumerate(scannrs_220[0:]):
    dct = np.load('map_%u.npz'%scannr)
    data220 = dct['data220']
    for h in find_hits(data220):
        hits_220.append((scannr, h))

counts = tuple(len(a) for a in (hits_111, hits_200, hits_220))
print('Found this many hits: \n (111): %u,\n (200): %u,\n (220): %u\n' % counts)
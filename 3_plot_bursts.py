"""
This script shows animated movies of spontaneous rocking curves,
using hits found by a preliminary search. The hit indices are
only examples, and by no means exhaustive.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

# 111 peaks
#scan, burst = (111, 15) # smeared
#scan, burst = (112, 15) # smeared
#scan, burst = (118, 52) # truncated
#scan, burst = (119, 61)
#scan, burst = (124, 37) # a little smeared?
#scan, burst = (124, 42)
#scan, burst = (126, 56)
#scan, burst = (137, 48) # rocking curve truncated
#scan, burst = (137, 53) # rocking curve a little truncated
#scan, burst = (139, 60)

# 200 peaks
#scan, burst = (84, 2)
#scan, burst = (84, 58) # rocking curve a little truncated
#scan, burst = (86, 2)
#scan, burst = (91, 49)
#scan, burst = (99, 40) # incomplete rocking curve
#scan, burst = (114, 25)
#scan, burst = (129, 32)
#scan, burst = (130, 37) # smeared
#scan, burst = (132, 18)

# 220 peaks
#scan, burst = 180, 26
#scan, burst = 180, 93
#scan, burst = 197, 89
scan, burst = 198, 89
#scan, burst = 201, 135 # smeared

Nb = 1000
inpath = '/data/visitors/nanomax/20200372/2021062308/raw/sample/'
pattern = 'scan_%06u_merlin.hdf5'
hdfpath = 'entry/measurement/Merlin/data'
maskfile = '/data/visitors/nanomax/common/masks/merlin/latest.h5'

with h5py.File(maskfile, 'r') as fp:
    mask = fp['mask'][:]

with h5py.File(inpath+pattern%scan, 'r') as fp:
    data = fp[hdfpath][burst*Nb:(burst+1)*Nb,:,:]
data[:] = data * mask

#fig, ax = plt.subplots(nrows=2, )
fig, ax = plt.subplots(nrows=2, gridspec_kw={'height_ratios':[.4,1]}, figsize=(7,12)) 
plt.subplots_adjust(hspace=.1, top=.99, bottom=.1, right=.95, left=.05)
ax[0].plot(data.max(axis=(1,2)))

l = ax[0].axvline(0)
data = np.log10(data)
center = np.argmax(data.max(axis=(1,2)))
begin = max(0, center-100)
mx = data.max()
for i in range(begin, data.shape[0]):
    ax[1].clear()
    ax[1].imshow(data[i], vmax=mx, cmap='jet')
    l.remove()
    l = ax[0].axvline(i)
    ax[0].set_title('frame %u'%i)
    plt.pause(.001)

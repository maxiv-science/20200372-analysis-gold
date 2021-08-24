"""
Makes index-time maps of bursts.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

scannrs = range(74,139+1) # 79 is shorter, maybe skip it
burst_n = 1000
inpath = '/data/visitors/nanomax/20200372/2021062308/raw/sample/'
pattern = 'scan_%06u_merlin.hdf5'
hdfpath = 'entry/measurement/Merlin/data'
i0pattern = '/data/visitors/nanomax/20200372/2021062308/raw/sample/%06u.h5'
maskfile = '/data/visitors/nanomax/common/masks/merlin/latest.h5'

with h5py.File(maskfile, 'r') as fp:
    mask = fp['mask'][:]

fig, ax = plt.subplots(ncols=len(scannrs), nrows=2)

for i, scannr in enumerate(scannrs[0:]):
    try:
        dct = np.load('map_%u.npz'%scannr)
        data111 = dct['data111']
        data200 = dct['data200']
    except FileNotFoundError:
        print('loading scan %u'%scannr)
        with h5py.File(inpath + pattern % scannr, 'r') as fp:
            data111 = np.zeros(fp[hdfpath].shape[0], dtype=int)
            data200 = np.zeros(fp[hdfpath].shape[0], dtype=int)
            for j,im in enumerate(fp[hdfpath]):
                im[:] = im * mask
                data111[j] = im[:257].max()
                data200[j] = im[257:].max()
                if j%1000 == 0:
                    print('#%u: %u/%u'%(scannr, j, data111.shape[0]*burst_n))
            data111 = data111.reshape((-1, burst_n))
            data200 = data200.reshape((-1, burst_n))
            np.savez('map_%u.npz'%scannr, data111=data111, data200=data200)
#    data = data / i0
    ax[0, i].imshow(data200, aspect='auto')
    ax[1, i].imshow(data111, aspect='auto')
    ax[0, i].set_title('scan #%u'%scannr)
ax[0, 0].set_ylabel('(200)')
ax[1, 0].set_ylabel('(111)')


# same thing for (220)\
scannrs = range(180, 204+1)
fig, ax = plt.subplots(ncols=len(scannrs), nrows=1)
for i, scannr in enumerate(scannrs[0:]):
    try:
        dct = np.load('map_%u.npz'%scannr)
        data220 = dct['data220']
    except (FileNotFoundError, KeyError):
        print('loading scan %u'%scannr)
        with h5py.File(inpath + pattern % scannr, 'r') as fp:
            data220 = np.zeros(fp[hdfpath].shape[0], dtype=int)
            for j,im in enumerate(fp[hdfpath]):
                im[:] = im * mask
                data220[j] = im.max()
                if j%1000 == 0:
                    print('#%u: %u/%u'%(scannr, j, data111.shape[0]*burst_n))
            data220 = data220.reshape((-1, burst_n))
            np.savez('map_%u.npz'%scannr, data220=data220)
#    data = data / i0
    ax[i].imshow(data220, aspect='auto')
    ax[i].set_title('scan #%u'%scannr)
ax[0].set_ylabel('(220)')

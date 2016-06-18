from matplotlib.collections import RegularPolyCollection
import numpy as np

def plotHexagon(center, size, axes):

    offsets = center

    collection = RegularPolyCollection(
        # fig.dpi,
        6,  # a hexagon
        rotation=(np.pi / 180) * 30,  # rotated 30 degrees [in radians]
        sizes=(size,),
        facecolors='w',
        edgecolors='black',
        linewidths=(2,),
        offsets=offsets,
        transOffset=axes.transData,
    )
    axes.add_collection(collection)

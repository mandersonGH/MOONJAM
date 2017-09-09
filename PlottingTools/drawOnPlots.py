import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection

from resources import EA_data
import plottingTools as pT

colorForLines = 'aqua'
lw = 2


def addCrossHairs(axes, plate_IFU, Re, hex_at_Cen):
    ##### ON other axis ######

    majX, majY, minX, minY = pT.axisEndpoints(plate_IFU, Re, hex_at_Cen)

    plt.plot(majX, majY, colorForLines, linewidth=lw)
    plt.plot(minX, minY, colorForLines, linewidth=lw)


def addReCircles(axes):
    circle1 = plt.Circle((0, 0), 1, color=colorForLines,
                         fill=False, linewidth=lw)
    axes.add_artist(circle1)
    circle2 = plt.Circle((0, 0), 2, color=colorForLines,
                         fill=False, linewidth=lw)
    axes.add_artist(circle2)
    circle3 = plt.Circle((0, 0), 3, color=colorForLines,
                         fill=False, linewidth=lw)
    axes.add_artist(circle3)


def plotHexagon(axes, plate_IFU, scale=1):
    IFU = plate_IFU.split("-")[1]
    fiberNo = int(IFU[:IFU.find('0')])

    size = float(EA_data.hexSizeDict[fiberNo]) / scale
    center = [0, 0]
    x1, x2 = axes.get_xlim()
    y1, y2 = axes.get_ylim()
    center[0] = np.mean([x1, x2])
    center[1] = np.mean([y1, y2])

    patch_list = []
    patch_list.append(RegularPolygon(
        xy=center,
        numVertices=6,
        radius=size,
        orientation=(np.pi / 180) * 30,  # rotated 30 degrees [in radians]
        facecolor='none',
        edgecolor='magenta',
        lw=2
    ))

    pc = PatchCollection(patch_list, match_original=True)

    # collection = RegularPolyCollection(
    #     # fig.dpi,
    #     6,  # a hexagon
    #     rotation=(np.pi / 180) * 30,  # rotated 30 degrees [in radians]
    #     sizes=(size,), # area of surrounding circle
    #     facecolors='none',
    #     edgecolors='magenta',
    #     linewidths=(2,),
    #     offsets=center,
    #     transOffset=axes.transData,
    # )
    # collection.set_facecolors(None)
    axes.add_collection(pc)

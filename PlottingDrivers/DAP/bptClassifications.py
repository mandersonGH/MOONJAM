"""
BPT classifications

for diagram 1: [OII]/H-beta on the y and [NII]/H-alpha on the x
    Note: included "Composite" section
for diagram 2: [OII]/H-beta on the y and [SII]/ H-alpha on the x
for diagram 3: [OII]/H-beta on the y and [OI] / H-alpha on the x

we have multiple wavelengths for some of these emission lines. Use:
[NII] = 6585
[OI] = 6302
[SII] = THE SUM OF both 6732 and 6718. ( I dunno why though. Just one of those stupid things.)
"""

def isStarForming(plotType, x, y):
    if isComposite(plotType, x, y):
        return False

    xmin, xmax = maxStarburstClassificationLineXBounds(plotType)
    return xmin < x and x < xmax\
           and y < maxStarburstClassificationLine(plotType, x)

def isSeyfert(plotType, x, y):
    if isStarForming(plotType, x, y):
        return False

    xmin, xmax = seyfertLinerClassificationLineXBounds(plotType)
    return xmin < x and x < xmax\
           and y > seyfertLinerClassificationLine(plotType, x)

def isComposite(plotType, x, y):
    if not plotType.endswith('[NII]'):
        return False

    xmin, xmax = pureStarformingClassificationLineXBounds(plotType)
    return xmin < x and x < xmax\
           and y < pureStarformingClassificationLine(plotType, x)

def isLINER(plotType, x, y):
    if isStarForming(plotType, x, y):
        return False

    xmin, xmax = seyfertLinerClassificationLineXBounds(plotType)
    return xmin < x and x < xmax\
           and y < seyfertLinerClassificationLine(plotType, x)

def maxStarburstClassificationLineXBounds(plotType):
    if not plotType.startswith('BPT'):
        print(jello) # TODO replace with exception

    if plotType.endswith('[NII]'):
        return (None, 0.05)

    if plotType.endswith('[SII]'):
        return (None, 0.32)

    if plotType.endswith('[OI]'):
        return (-2, -0.6)

    print(jello)

def maxStarburstClassificationLine(plotType, x):
    """
    Values below this return value are star-forming.
    In other words, this is top-right of a circle and
    points within the circle are star-forming

    ke01 in L. J. Kewley et al
    """
    if not plotType.startswith('BPT'):
        print(jello) # TODO replace with exception

    if plotType.endswith('[NII]'):
        return 0.61 / (x - 0.05) + 1.3

    if plotType.endswith('[SII]'):
        return 0.72 / (x - 0.32) + 1.3

    if plotType.endswith('[OI]'):
        return 0.73 / (x - 0.59) + 1.33

    print(jello)

def pureStarformingClassificationLineXBounds(plotType):
    if not plotType.startswith('BPT') and not plotType.endswith('[NII]'):
        print(jello) # TODO replace with exception

    return (-1.2805,  0.47)

def pureStarformingClassificationLine(plotType, x):
    """
    lower bound of "Composite"

    ka03 in L. J. Kewley et al
    """
    if not plotType.startswith('BPT') and not plotType.endswith('[NII]'):
        print(jello) # TODO replace with exception

    return 0.61 / (x - 0.47) + 1.19

def seyfertLinerClassificationLine(plotType, x):
    """
    Above are seyfert, below are liners
    """
    if not plotType.startswith('BPT'):
        print(jello) # TODO replace with exception

    if plotType.endswith('[NII]'):
        return 1.89 * x + 0.76 # TODO get real value

    if plotType.endswith('[SII]'):
        return 1.89 * x + 0.76

    if plotType.endswith('[OI]'):
        return 1.18 * x + 1.3

    print(jello)

def seyfertLinerClassificationLineXBounds(plotType):
    if not plotType.startswith('BPT'):
        print(jello) # TODO replace with exception

    if plotType.endswith('[NII]'):
        return (-0.26, 10)

    if plotType.endswith('[SII]'):
        return (-0.33, 10)

    if plotType.endswith('[OI]'):
        return (-1.14646, 10) # 46 repeating

    print(jello)

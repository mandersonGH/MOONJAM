# generic directory functions
import os
import fnmatch


def setupNewDir(filename, newFolderName, typeStr):
    # ensures new folder
    # sets up folder path for new files
    fileLs = filename.split('/')
    # newFldrNme = fileLs[-1]
    del fileLs[-1]

    newFldrPath = '/'.join(fileLs) + '/Figures/' + \
        newFolderName + typeStr + '/'
    assure_path_exists(newFldrPath)

    return newFldrPath


def assure_path_exists(path):
    # from
    # https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("New directory made {" + dir + "/}")


def locate(pattern, subBin, rootD=os.curdir):
    matches = []
    if subBin is True:
        for root, dirnames, filenames in os.walk(rootD):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
    else:
        pattern = pattern[1:len(pattern)]
        for file in os.listdir(rootD):
            if file.endswith(pattern):
                matches.append(rootD + file)
    return matches

# generic directory functions
import os


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

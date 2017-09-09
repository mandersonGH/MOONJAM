# generic directory functions
import os
import fnmatch


def getFilename(fullFilePath):
    fileVec = fullFilePath.split("\\")
    filename = fileVec[-1]
    return filename


def assure_path_exists(path):
    # from
    # https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("New directory made {" + dir + "/}")

    return(path)


def locate(endOfFilename, subBin, rootD=os.curdir):
    pattern = '*' + endOfFilename
    matches = []
    print(rootD)
    if subBin is True:
        #         print(rootD)
        for root, dirnames, filenames in os.walk(rootD):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
    else:
        pattern = pattern[1:len(pattern)]
        for file in os.listdir(rootD):
            if file.endswith(pattern):
                matches.append(rootD + file)
    return matches

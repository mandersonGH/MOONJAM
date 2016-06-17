

def setupNewDir(filename, newName):
    # ensures new folder
    # sets up folder path for new files
    # print(filename)
    fileLs = filename.split('/')
    # print(fileLs)
    del fileLs[-1]

    newFldrPath = '/'.join(fileLs) + '/Figures/' + newName + '/'
    # print(newFldrPath)
    assure_path_exists(newFldrPath)

    return newFldrPath
    
    
def assure_path_exists(path):
    # from
    # https://justgagan.wordpress.com/2010/09/22/python-create-path-or-directories-if-not-exist/
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("New directory made {" + dir + "/}")

import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Main.Controller import Controller

'''
Created on Sep 8, 2017

@author: Mande
'''


def main():
    controller = Controller(sys.argv)
    # inputs = ['', r'C:\Users\Mande\Desktop\E + A Directory' + "\\", 'mpl4','pipe3d', 'requested','elines','lum_fracs','indices.cs']
    # controller = Controller(inputs)
    controller.run()


if __name__ == '__main__':
    main()

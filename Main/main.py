import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import argparse

from Main.Controller import Controller

'''
Created on Sep 8, 2017

@author: Mande
'''


def main():
    args = parse_args()
    print(args)
    
    controller = Controller(args.eaDirectory,
                            args.dataVersions,
                            args.requestedPlots)
    controller.run()

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-ead', "--eaDirectory", type=str, required=True,
                        help="path to 'E + A Directory' with fits files")

    parser.add_argument('-dv', "--dataVersions", action='append', required=True,
                        help="data versions (mpl4, mpl5, pipe3d)")

    parser.add_argument('-plt', "--requestedPlots", action='append', required=True,
                        help="plots to create for each data version specified")

    return parser.parse_args()

if __name__ == '__main__':
    main()

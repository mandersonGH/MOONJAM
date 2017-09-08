from Controller import Controller
import sys

'''
Created on Sep 8, 2017

@author: Mande
'''

def main():
    #controller = Controller(sys.argv)
    inputs = ['', r'C:\Users\Mande\Cloud Storage\Google Drive\2016 MOONJAM PROJECT\E + A Directory' + "\\",'mpl4','emlines_gflux']
    controller = Controller(inputs)
    controller.run()
    

if __name__ == '__main__':
    main()

    


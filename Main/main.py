from Controller import Controller
import sys

'''
Created on Sep 8, 2017

@author: Mande
'''

def main():
    #controller = Controller(sys.argv)
    inputs = ['', r'C:\Users\Mande\Desktop\E + A Directory' + "\\",'mpl5','whan']
    controller = Controller(inputs)
    controller.run()
    

if __name__ == '__main__':
    main()

    


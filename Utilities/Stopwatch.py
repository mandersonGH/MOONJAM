'''
Created on Sep 8, 2017

@author: Mande
'''

import time

class Stopwatch:
    
    def start(self):
        self._start = time.time()
        
    def stop(self):
        self._end = time.time()
        
    def _calculateDuration(self):
        self._duration = self._end - self._start
        
    def reportDuration(self):
        self._calculateDuration()
        print("The time elapsed is " + str(round(self._duration, 2)) + " seconds")
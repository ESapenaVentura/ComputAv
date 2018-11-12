#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 18:05:49 2018

@author: qq
"""
from time import sleep

def cuentaAtras(inicio, fin, sleepy = None):
    paso = 1
    if (inicio > fin):
        paso *= -1
    for i in range(inicio, fin, paso):
        if sleepy:
            sleep(5)
        continue
    
def Main():
    cuentaAtras(10**6, 0, True)
if __name__ == "__main__":
    Main()
    
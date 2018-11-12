#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 18:15:54 2018

@author: qq
"""
from math import sqrt
from threading import Thread, Event
from queue import Queue, Empty

class Hilo(Thread):
    def __init__(self, input_div, output_div):
        super(Hilo, self).__init__()
        self.input = input_div
        self.output = output_div
        self.end = Event()
        
        
    def run(self):
        while (not self.end.isSet()):
            try:
                parametros = self.input.get(True, 0.05)
                numero = parametros[0]
                ini = parametros[1]
                fin = parametros[2]
                self.output.put(encuentraDivisores(numero, ini, fin))
            except Empty:
                continue
        
    def join(self, timeout = None):
        self.end.set()
        super(Hilo,self).join(timeout)
        
def encuentraDivisores(numero, ini, fin):
    lista = []
    i = ini
    while(i < fin + 1):
        if (numero % i == 0):
            lista.append(i)
            numero = numero // i
            lista.append(numero)
            i = ini
        i += 1
    return lista

def divideProblema(numero, hilos):
    lista = []
    numero_a = 2
    div = int(sqrt(numero)) // hilos
    for i in range(hilos):
        lista.append([numero, numero_a, numero_a + div])
        numero_a += div
    lista[hilos - 1][2] = int(sqrt(numero)) + 1
    return lista

def Main():
    input_Queue = Queue()
    output_Queue = Queue()
    numero = 215517917
    hilos = 4
    lista = divideProblema(numero, hilos)
    print(lista)
    
    pool = [Hilo(input_Queue, output_Queue) for i in range(hilos)]
    
    for thread in pool:
        thread.start()
        
    for i in range(hilos):
        input_Queue.put(lista[i])
    
    res = []
    for i in range(hilos):
        pool[i].join()
        res += output_Queue.get(True, 0.05)
    if res:
        print(res)

if __name__ == "__main__":
    Main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 19:32:07 2018

@author: qq
"""

from time import time, sleep
from threading import Thread
from multiprocessing import Process, Queue, Event
from queue import Empty
import math

class EscribirHilo (Thread):
    def __init__ (self, input_q, output_q):
        super(EscribirHilo, self).__init__(self)
        self.input = input_q
        self.output = output_q
        self.end = Event()

def run (self):        
	factoresParallel(self.numero, self.ini, self.fin, self.res)

class factoresParallel (Process):   
	def __init__ (self, input_q, output_q):
        super(factoresParallel, self).__init__(self)
        self.input = input_q
        self.output = output_q
        self.end = Event()
	def run (self):
        while not self.end.isSet():
            try:
                parametros = self.input.get(True, 0.05)
                numero = parametros[0]
                ini = parametros[1]
                fin = parametros[2]
                res = []
                factoresParallel(numero, ini, fin, res)
                self.output.put(res)
            except Empty:
                continue

    def join(self, timeout = None):
        self.end.set()
        super(Hilo,self).join(timeout)
        
    


def factoresParallel(numero, ini, fin, res):
	for i in range(ini, fin):
		if (numero % i == 0):
			res.append(i)
	return res

def factores(numero):
	lista = []
	for i in range(2, numero-1):
		if (numero % i == 0):
			lista.append(i)
	return lista

def main():
    numero = int(input("Dame un número:"))
    output_q = Queue()
    hilos = int(input("Cuantos procesos:"))
    aux = math.ceil((numero/2)/hilos)
    input_q = Queue()

    resultado = []
    listaHilos = []
    a = time()
    for i in range(hilos):
         = 2+aux*i+i #
		fin = ini+aux
		print(ini,fin)
		resHilo = []
		resultado.append(resHilo)
 input_q.put((numero, ini, fin))
		listaHilos.append(Thread(target = factoresParallel, args = (input_q, output_q)))
		listaHilos[i].start()

	for i in range(hilos):
		listaHilos[i].join()
        print(output_q.get())

for
	print(resultado)
	b = time()
	print(b-a)
	#factoresParallel(numero, 2, numero, res)
	#factores(numero)

if __name__ == '__main__':
	main()
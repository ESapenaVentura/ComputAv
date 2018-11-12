# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 09:00:32 2018

@author: Enrique
"""
import sys

from math import sqrt
from threading import Thread, Event
from queue import Queue, Empty

CURRENT_VERSION = sys.version_info
REQUESTED_VERSION = (3, 7)



if (CURRENT_VERSION >= REQUESTED_VERSION):
    from time import time_ns
else:
    from time import time as time_ns



class Hilo(Thread):
    
    def __init__(self, input_Hilos, output_Hilos, run = True):
        super(Hilo, self).__init__()
        self.input = input_Hilos
        self.output = output_Hilos
        self.stoprequest = Event()

    def run(self):
        
        while not self.stoprequest.isSet():
            try:
                para_Funcion = self.input.get(True, 0.05)
                num = para_Funcion[0]
                i_Inicial = para_Funcion[1]
                i_Final = para_Funcion[2]
                
                Primo = self._es_Primo(num, i_Inicial, i_Final)
                self.output.put(Primo)
            except Empty:
                continue
    
    def join(self, timeout=None):
        self.stoprequest.set()
        super(Hilo, self).join(timeout)
        
    
    def suma_Digitos(self, num):
        suma = 0
        while True:
            for Digito in str(num):
                suma += int(Digito)
            else:
                if len(str(suma)) == 1:
                    break
                else:
                    num = suma
                    suma = 0
        return suma

    def ajustar_Indice_Inicial(self, i):
        if (i < 7):
            return 7
        else:
            ultimo_char = str(i)[-1]
            if (ultimo_char ==  '4'):
                i += 2
            elif (ultimo_char in ["0", "2", "5", "6", "8"]):
                i += 1
        return i    
    
    def _es_Primo(self, num, i_Inicial, i_Final):
        if (i_Inicial < 7):
           if str(num)[-1] in ["0", "2", "4", "5", "6", "8"]:
               return False
           elif self.suma_Digitos(num) % 3 == 0:
               return False
        
        i_Inicial = self.ajustar_Indice_Inicial(i_Inicial)
           
        mult_3 = i_Inicial % 3
        if (mult_3 == 2):
            mult_3 = 1
        elif (mult_3 == 1):
            mult_3 = 2
            
        mult_5 = i_Inicial % 10
        if (mult_5 > 5):
            mult_5 = (mult_5 - 5)/2
        else:
            mult_5 = (mult_5 + 5)/2
        
        for i in iter(range(i_Inicial, i_Final, 2)):
            if self.stoprequest.isSet():
                break
            if (mult_3 == 0 or mult_5 == 0):
                mult_5 += 1
                mult_3 += 1
                continue
            if (num % i == 0):
                return False
            
            mult_3 += 1
            mult_5 += 1
            if (mult_3 == 3):
                mult_3 = 0
            if (mult_5 == 5):
                mult_5 = 0
                    
        else:
            return True
        return False
        
def repartir_Indices(numero, hilos):

    num_anadir = 0
    divisor = int(sqrt(numero)) // hilos
    args = []
    for i in range(hilos):
        temp = []
        temp.append(numero)
        temp.append(num_anadir)
        num_anadir += divisor
        if (i == hilos - 1):
            num_anadir += divisor % hilos
            
        temp.append(num_anadir)
        args.append(temp)
    return args
    
   
def main():
    hilos = 4
    t_i = time_ns()
    numero = 495176015483567808823531
    input_Hilos = Queue()
    output_Hilos = Queue()
    
    pool = [Hilo(input_Hilos = input_Hilos, output_Hilos = output_Hilos) for i in range(hilos)]
    
    args = repartir_Indices(numero, hilos)
    
    for thread in pool:
        thread.start()
        
   
    for lista_Args in args:
        input_Hilos.put(lista_Args)
    while hilos > 0:
        resultados = output_Hilos.get()
        hilos -= 1
        if (resultados == False):
            print("No es primo")
            t_f = time_ns()
            print("Tiempo = {} s".format((t_f - t_i)))
            for thread in pool:
                thread.join()
            return
        
    print("Es primo")
    t_f = time_ns()
    print("Tiempo = {} s".format((t_f - t_i)))
    for thread in pool:
        thread.join()
            
    
    
        
    
        
if __name__ == '__main__':
    main()

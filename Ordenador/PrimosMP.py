# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 14:56:59 2018

@author: Enrique
"""
import sys
from math import sqrt
from multiprocessing import Pool,Manager
from queue import Empty

CURRENT_VERSION = sys.version_info
REQUESTED_VERSION = (3, 7)



if (CURRENT_VERSION >= REQUESTED_VERSION):
    from time import time_ns
else:
    from time import time as time_ns


def suma_Digitos(num):
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

def ajustar_Indice_Inicial(i):
    if (i < 7):
        return 7
    else:
        ultimo_char = str(i)[-1]
        if (ultimo_char ==  '4'):
            i += 2
        elif (ultimo_char in ["0", "2", "5", "6", "8"]):
            i += 1
    return i


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
        temp = []
    return args

    

def es_Primo(num, i_Inicial, i_Final, evento, terminado):
    if (i_Inicial < 7):
       if str(num)[-1] in ["0", "2", "4", "5", "6", "8"]:
           evento.set()
           return
       elif suma_Digitos(num) % 3 == 0:
           evento.set()
           return
    
    i_Inicial = ajustar_Indice_Inicial(i_Inicial)
       
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
        if (evento.is_set()):
            break
        if (mult_3 == 0 or mult_5 == 0):
            mult_5 += 1
            mult_3 += 1
            continue
        if (num % i == 0):
            evento.set()
            return
        
        mult_3 += 1
        mult_5 += 1
        if (mult_3 == 3):
            mult_3 = 0
        if (mult_5 == 5):
            mult_5 = 0
    terminado.set()

def Main():
    t_i = time_ns()
    numero = 524287
    procesos = 8
    args = repartir_Indices(numero, procesos)

    mana = Manager()
    noPrimo = mana.Event()
    terminado = [mana.Event() for i in range(len(args))]
    
    for i in range(len(args)):
        args[i].append(noPrimo)
        args[i].append(terminado[i])
    
    workers = Pool(procesos)
    workers.starmap(es_Primo, args)
    
    while (True):
        lista = []
        for i in range(len(args)):
            if terminado[i].is_set():
                lista.append(True)
        if (len(lista) == len(args)):
            break
        if (noPrimo.is_set()):
            break
    
    workers.terminate()
    if (noPrimo.is_set()):
        print("No es primo")
    else:
        print("Es primo")
    """
    if (procesos == 0):
        workers.terminate()
        print("Es primo")
        """
    
    t_f = time_ns()
    print("Tiempo final: {}s".format((t_f - t_i)))
    return
    
    
    
if __name__ == "__main__":
    Main()

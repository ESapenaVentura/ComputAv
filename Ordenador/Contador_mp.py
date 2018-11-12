# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 19:15:43 2018

@author: Enrique
"""
from time import time_ns, sleep
from multiprocessing import Pool

def cuentaAtras(ini, fin, tiempo_espera = False):
    for i in range(ini, fin, -1):
      if tiempo_espera:
        sleep(tiempo_espera)
        
def repartirParametros(cuenta_atras, tiempo_espera, hilos):
  lista_args = []
  div = cuenta_atras // hilos
  resto = cuenta_atras % hilos
  for i in range(hilos):
    if i == hilos -1:
      lista_args.append((div * (i + 1) + resto, div * i, tiempo_espera))
    else:
      lista_args.append((div * (i+1), div * i, tiempo_espera))
      
  return lista_args
  
  
def Main():
  t_i = time_ns()
  procesos = 4
  tiempo_cuenta_atras = 10 ** 6 + 7
  tiempo_espera = False
  
  args = repartirParametros(tiempo_cuenta_atras, tiempo_espera, procesos)
  print(args)
  with Pool(procesos) as p:
    p.starmap(cuentaAtras, args)
  
  print("Tiempo final: {}".format((time_ns() - t_i)/10**9))
  
if __name__ == "__main__":
  Main()
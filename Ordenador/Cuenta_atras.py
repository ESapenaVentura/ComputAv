# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 10:44:33 2018

@author: Enrique
"""

from time import time_ns, sleep
from threading import Thread, Event
from queue import Queue, Empty

class HiloCuentaAtras(Thread):
  
  def __init__(self, input_q):
    super(HiloCuentaAtras, self).__init__()
    self.input = input_q
    self.end_event = Event()
    
    
  def run(self):
    while not self.end_event.isSet():
      try:
        parametros = self.input.get(True, 0.05)
        inicio = parametros[0]
        fin = parametros[1]
        tiempo_espera = parametros[2]
        self.cuentaAtras(inicio, fin, tiempo_espera)
      except Empty:
        continue
      
  def join(self, timeout = None):
    self.end_event.set()
    super(HiloCuentaAtras, self).join(timeout)
    

  def cuentaAtras(self, ini, fin, tiempo_espera = False):
    for i in range(ini, fin, -1):
      if tiempo_espera:
        sleep(tiempo_espera)
        
def repartirParametros(cuenta_atras, tiempo_espera, hilos, input_q):
  div = cuenta_atras // hilos
  resto = cuenta_atras % hilos
  for i in range(hilos):
    if i == hilos -1:
      input_q.put((div * (i + 1) + resto, div * i, tiempo_espera))
    else:
      input_q.put((div * (i+1), div * i, tiempo_espera))
  
  
def Main():
  t_i = time_ns()
  hilos = 4
  tiempo_cuenta_atras = 10 ** 6 + 7
  tiempo_espera = None
  input_q = Queue()
  repartirParametros(tiempo_cuenta_atras, tiempo_espera, hilos, input_q)
  
  pool = [HiloCuentaAtras(input_q) for i in range(hilos)]
  
  for thread in pool:
    thread.start()
  
  for thread in pool:
    thread.join()
  print("Tiempo final: {}".format((time_ns() - t_i)/10**9))
  
if __name__ == "__main__":
  Main()
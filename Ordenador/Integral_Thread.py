# -*- coding: utf-8 -*-
"""
Cuestionario de Programación y Técnicas Computacionales Avanzadas en 
Bioinformática

Cuestionario 1: Script concurrente(Hilos)

@Autor: Enrique Sapena Ventura
@Fecha: 8/10/2018
@Version 1.0

@Python_version = 3.7.0
"""

from threading import Thread, Event
from queue import Queue, Empty

import sys
REQUESTED_VERSION = (3,7)
CURRENT_VERSION = sys.version_info

if (REQUESTED_VERSION <= CURRENT_VERSION):
    from time import time_ns #Solo disponible en python 3.7+
else:
    from time import time as time_ns


"""/**
Crea un generador entre start y stop, siguiendo el intervalo step.

\pre step != 0
\pre if(start > stop) step < 0

\param[in] (double||float||int) start Principio del rango.
\param[in] (double||float||int) stop Final del rango (Por defecto None).
\param[in] (double||float||int) step Intervalo de saltos (Por defecto None).

\returns generator object con valores entre start y stop.

\note Similar a numpy.arange(), pero se ha decidido crear esta función debido
      a que numpy no se ejecuta en Python 3.7
"""
def frange(start, stop = None, step = None):
    # Si stop y step son nulos, start = 0.0 y step = 1.0
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
        
    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield (start) # Generador de numeros flotantes
        start = start + step
        
"""/**
Reparte los valores para calcular las "sub-integrales".

\pre hilos > 0
\pre p_i > p_f
\pre step > 0

\param[in] hilos    Numero de hilos. No está garantizado que hilos == numero
                    de hilos creados. Mirar las notas para más detalle.
\param[in] p_i      Punto x_i de la integral definida.
\param[in] p_f      Punto Final de la integral definida.
\param[in] step     Intervalo de saltos.

\returns (lista) @args{
                       (tupla)@{
                               (double||float||int) x_i       Valor inicial.
                               (double||float||int) x_f       Valor final.
                               (double||float||int) step      Intervalo.
                               }
                      }
                    
\note Debido a que los valores se reparten para que los cuadrados sean iguales
      y en los intervalos deseados, hay veces que, si el numero de divisiones 
      es mayor al número de hilos, no se podrán crear los suficientes hilos. 
      Por lo tanto, el número de hilos siempre será <= hilos deseados.
"""
def repartirParam(hilos, p_i, p_f, step):
    args = []
    x_i = p_i
    divisor = (p_f - p_i) / hilos
    for x_f in frange(p_i, p_f, step):
      if x_f >= (divisor + x_i):
        args.append((x_i, x_f, step))
        x_i = x_f
    else:
      args.append((x_i, p_f, step))
    return args


"""/**
Esta clase inicia un hilo para la realización de una "sub-integral" definida.

\param[in] (Queue Object) input_hilo_sub_integral Cola en la que entrará el 
                          input con el que trabajaran los hilos
\param[in] (Queue Object) output_hilo_sub_integral Cola en la que se almacena
                          el output.
                          
\note Los hilos se comunican entre sí mediante la función join() interna: 
      una vez llamada, se ejecuta el evento de finalización para todos los
      hilos.
"""
class HiloSubIntegral(Thread):
  
  def __init__(self, input_hilo_sub_integral, output_hilo_sub_integrals, 
               run = True):
      super(HiloSubIntegral, self).__init__()
      self.input = input_hilo_sub_integral
      self.output = output_hilo_sub_integrals
      self.stoprequest = Event()

  """/**
  Inicio del trabajo del hilo.
  """
  def run(self):
      while not self.stoprequest.isSet():
          try:
              #Coge parámetros de la cola compartida, y realiza la función.
              para_funcion = self.input.get(True, 0.05)
              i_a = para_funcion[0]
              i_b = para_funcion[1]
              step = para_funcion[2]
              
              Area = self.resolverIntegral(i_a, i_b, step)
              self.output.put(Area)
          except Empty:
              continue
          """except:
            self.join()"""
  
  """/**
  LLamada a finalizar el hilo.
  
  \param[in] timeout Tiempo para declarar un timeout.
  """
  def join(self, timeout = None):
      self.stoprequest.set()
      super(HiloSubIntegral, self).join(timeout)
      
  
  """/**
  f(x) para la función x**2 + 2x + 1
  
  \param[in] (double||float||int) x Valor de la "x" para calcular f(x)
  
  \returns (float) Valor de f(x)
  """
  def f(self, x):
      return x**2 + 2*x + 1

  """/**
  Dado un valor de x, valor inicial de x en el rectángulo y el intervalo, 
  calcula el área del mismo
  
  \param[in] (double||float||int) base_rectangulo Base del rectángulo.
  \param[in] (double||float||int) x_i Valor inicial de x en el rectángulo.
  
  \returns (float) Valor del área del rectángulo
  """
  def calcArea(self, base_rectangulo, x_i):
      return base_rectangulo * self.f(x_i + base_rectangulo)

    
  """/**
  Dado un punto inicial, un punto final, y un intervalo, calcula una integral
  definida.
  
  \param[in] (double||float||int) p_i   Punto Inicial de la integral definida
  \param[in] (double||float||int) p_f   Punto Final de la integral definida
  \param[in] (double||float||int) step  Intervalo de cálculo de los rectángulos
  
  \returns (float) area Suma del área de todos los rectángulos de la integral
                        definida entre p_i y p_f con rectángulos de base step.
  """
  def resolverIntegral(self, p_i, p_f, step):
      area = 0
      for x_i in frange(p_i, p_f, step):
        area += self.calcArea(step, x_i) #step == base del rectángulo
      return area

##############################################################################
#                                                                            #
#                                   MAIN()                                   #
#                                                                            #
##############################################################################
def Main():
  input("Este script servirá para realizar la integral definida de la "
        "función 'f(x) = x**2 + 2x + 1', usando una aproximación por "
        "rectángulos entre dos puntos (inicial > final) con un intervalo, "
        "que el usuario definirá, indicando el número de divisiones."
        "Además, se emplearán hilos para acelerar el cálculo."
        "\nPresione <Intro> para continuar")
  
  #Introducción de parámetros y checkeo de errores.
  while True:
    try:
      hilos = int(input("Introduzca el número de hilos: "))
      p_i = float(input("Introduzca el parámetro de inicio: "))
      p_f = float(input("Introduzca el parámetro final: "))
      divisiones = int(input("Introduzca el numero de sub-integrales "
                             "que desea calcular: "))
      
      if (p_i < p_f) and divisiones > 0 and hilos > 0: #Todo correcto
        break
      else:
        input("Valores no correctos. El primer parámetro ha de ser "
            "inferior al segundo. Además, no se acepta un número de "
            "divisiones o de hilos menor a 1\n\nPresione <Intro> y vuelva a "
            "introducirlos.\n")
    except ValueError:
      print ("Por favor, introduzca enteros para los hilos, flotante "
             "o entero para los puntos, y entero para divisiones")

      
  t_i = time_ns()     #Tiempo inicial.
  step = (p_f - p_i) / divisiones  #Base de los rectángulos
  
  #Reparto de argumentos y creación de las colas y el pool para los hilos.
  args = repartirParam(hilos, p_i, p_f, step)
  if (hilos != len(args)):
      hilos = len(args)
      print("Se ha cambiado el número de hilos para ajustar el cálculo. "
            "Procediendo con {} hilo(s).\n".format(hilos))
  input_q = Queue()
  output_q = Queue()
  pool = [HiloSubIntegral(input_q, output_q) 
          for i in range(hilos)]
  
  #Comienzan los hilos y se les asignan trabajos.
  for thread in pool:
      thread.start()
  for lista_Args in args:
      input_q.put(lista_Args)
  
  #Se recoge el trabajo de los hilos y se suma a la variable "area"
  area = 0 #Area de los rectángulos
  count_hilos = hilos
  while count_hilos > 0:
      area += output_q.get()
      count_hilos -= 1
  
  #Una vez terminado, se cierran los hilos.
  for thread in pool:
      thread.join()
  
  #Se imprime el área a stdout
  print("El área es: {}".format(area))
  
  #Ajuste requerido por versión de Python
  if (REQUESTED_VERSION > CURRENT_VERSION):
      div = 1
  else:
      div = 10 ** 9
  print("Tiempo de ejecución: {} segundos".format((time_ns() - t_i) / div))
      
if __name__ == "__main__":
  Main()
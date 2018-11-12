# -*- coding: utf-8 -*-
"""
Cuestionario de Programación y Técnicas Computacionales Avanzadas en 
Bioinformática

Cuestionario 1: Script paralelo(Procesos)

@Autor: Enrique Sapena Ventura
@Fecha: 8/10/2018
@Version 1.0

@Python_version = 3.7.0
"""

from multiprocessing import Pool
from multiprocessing import cpu_count

import sys
REQUESTED_VERSION = (3,7)
CURRENT_VERSION = sys.version_info

if (REQUESTED_VERSION <= CURRENT_VERSION):
    from time import time_ns #Solo disponible en python 3.7+
else:
    from time import time as time_ns


def frange(start, stop = None, step = None):
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
f(x) para la función x**2 + 2x + 1

\param[in] (double||float||int) x Valor de la "x" para calcular f(x)

\returns (float) Valor de f(x)
"""
def f(x):
    return x**2 + 2*x + 1


"""/**
Dado un valor de x, el valor inicial de la x y el intervalo, calcula el área 
del rectángulo

\param[in] (double||float||int) base_rectangulo Base del rectángulo.
\param[in] (double||float||int) x_i Valor inicial de x en el rectángulo.

\returns (float) Valor del área del rectángulo
"""
def calcArea(base_rectangulo, x_i):
    return base_rectangulo * f(x_i + base_rectangulo)


"""/**
Dado un punto inicial, un punto final, y un intervalo, calcula una integral
definida.

\param[in] (double||float||int) p_i   Punto Inicial de la integral definida
\param[in] (double||float||int) p_f   Punto Final de la integral definida
\param[in] (double||float||int) step  Intervalo de cálculo de los rectángulos

\returns (float) area Suma del área de todos los rectángulos de la integral
                      definida entre p_i y p_f con rectángulos de base step.
"""
def resolverIntegral(p_i, p_f, step):
    area = 0
    for x_i in frange(p_i, p_f, step):
      area += calcArea(step, x_i) #step == base del rectángulo
    return area


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
                 Lista con "procesos" número de tuplas
                    
\note Debido a que los valores se reparten para que los cuadrados sean iguales
      y en los intervalos deseados, hay veces que, si el numero de divisiones 
      es mayor al número de hilos, no se podrán crear los suficientes hilos. 
      Por lo tanto, el número de hilos siempre será <= hilos deseados.
"""
def repartirParam(procesos, p_i, p_f, step):
    args = []
    divisor = (p_f - p_i) / procesos
    for i in range(procesos):
      x_i = p_i + divisor * i
      x_f = x_i + divisor
      args.append((x_i, x_f, step))
      
    return args
  
  
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
        "Además, se emplearán procesos para acelerar el cálculo."
        "\nPresione <Intro> para continuar")
    
  #Introducción de parámetros y checkeo de errores.
  while True:
    try:
      procesos = int(input("Introduzca el número de procesos: "))
      p_i = float(input("Introduzca el parámetro de inicio: "))
      p_f = float(input("Introduzca el parámetro final: "))
      divisiones = int(input("Introduzca el numero de sub-integrales "
                             "que desea calcular: "))
      
      if (p_i < p_f) and divisiones > 0 and procesos > 0: #Todo correcto
        break
      else:
        input("Valores no correctos. El primer parámetro ha de ser "
            "inferior al segundo. Además, no se acepta un número de "
            "divisiones o procesos menor a 1\n\nPresione <Intro> y vuelva a "
            "introducirlos.\n")
    except ValueError:
      print ("Por favor, introduzca enteros para los procesos, flotante "
             "o entero para los puntos, y entero para divisiones")
      
  #Ajuste del número de procesos
  if (divisiones < procesos):
    procesos = divisiones
    print("Se ha cambiado el número de procesos para ajustar el cálculo. "
          "Procediendo con {} proceso(s).".format(procesos))
  elif (procesos > cpu_count()):
    procesos = cpu_count()
    print("Numero de procesos introducidos mayor al número de procesos "
          "que pueden ejecutarse simultáneamente en tu ordenador. Procediendo "
          "con {} procesos\n".format(procesos))

  t_i = time_ns()                  #Tiempo inicial.
  step = (p_f - p_i) / divisiones  #Base de los rectángulos
  
  #Reparto de argumentos y creación de las colas y el pool para los procesos.
  args = repartirParam(procesos, p_i, p_f, step)
      
  #Creación del pool de procesos y asignación de funciones y parámetros.
  with Pool(procesos) as p:
    area = p.starmap(resolverIntegral, args)
    
  #Envío a stdout del área
  print("Area: {}".format(round(sum(area), 3)))
  
  #Ajuste requerido por versión de Python
  if (REQUESTED_VERSION > CURRENT_VERSION):
      div = 1
  else:
      div = 10 ** 9
  print("Tiempo de ejecución: {} segundos".format((time_ns() - t_i) / div))
  
if __name__ == "__main__":
    Main()
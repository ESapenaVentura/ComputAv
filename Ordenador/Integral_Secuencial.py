# -*- coding: utf-8 -*-
"""
Cuestionario de Programación y Técnicas Computacionales Avanzadas en 
Bioinformática

Cuestionario 1: Script secuencial

@Autor: Enrique Sapena Ventura
@Fecha: 8/10/2018
@Version 1.0

@Python_version = 3.7.0
"""

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


def f(x):
  """/**
  f(x) para la función x**2 + 2x + 1
  
  \param[in] (double||float||int) x Valor de la "x" para calcular f(x)
  
  \returns (float) Valor de f(x)
  """
  return x**2 + 2*x + 1


def calcArea(base_rectangulo, x_i):
  """/**
  Dado un valor de x, el contador n y el intervalo, calcula el área del 
  rectángulo
  
  \param[in] (double||float||int) base_rectangulo Base del rectángulo.
  \param[in] (double||float||int) x_i Valor inicial de x en el rectángulo.
  
  \returns (float) Valor del área del rectángulo
  """
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
          "\nPresione <Intro> para continuar")
    
    #Introducción de parámetros y checkeo de errores
    while True:
        try:
            p_i = float(input("Introduzca el punto inicial: "))
            p_f = float(input("Introduzca el punto final: "))
            divisiones = int(input("Introduzca el numero de sub-integrales "
                                   "que desea calcular: "))
            print("\n")
            if (p_i < p_f) and divisiones > 0:
                break
            else:
                input("Valores no correctos. El primer parámetro ha de ser "
                  "inferior al segundo. Además, no se acepta un número de "
                  "divisiones < 1\n\nPresione <Intro> y vuelva a "
                  "introducirlos.\n")
        except ValueError:
            print ("Por favor, introduzca enteros > 0 para el número de "
                   "divisiones, float o int para el resto de parámetros")
    
    step = (p_f - p_i) / divisiones #Calculo del intervalo
    t_i = time_ns()
    
    #Cálculo y envío a stdout del área de la integral definida.
    area = resolverIntegral(p_i, p_f, step)
    print("El área es: {}".format(round(area, 3))) #Redondeado a 3 decimales
    
    #Ajuste requerido por versión de Python
    if (REQUESTED_VERSION > CURRENT_VERSION):
        div = 1
    else:
        div = 10 ** 9
    print("Tiempo de ejecución: {} segundos".format((time_ns() - t_i) / div))
    
    
if __name__ == "__main__":
    Main()
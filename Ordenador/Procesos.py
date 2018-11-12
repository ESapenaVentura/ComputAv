# -*- coding: utf-8 -*-
"""
Cuestionario de Programación y Técnicas Computacionales Avanzadas en 
Bioinformática

Cuestionario grupal 1: Script concurrente(Procesos)

@Autors: -Alejandro Cebrián del Valle
         -Enrique Sapena Ventura
         -Héctor Badenes Tur
         -Pedro Salguero TremendoMaquina
@Fecha: 18/10/2018
@Version 1.0

@Python_version = 3.5.2
"""

import signal
import sys

from math import ceil
from multiprocessing import cpu_count, Process
from time import time, sleep


def contadorParallel(ini, fin, espera):
    """/**
    Cuenta atrás de ini a fin, step 1, con tiempo de espera condicional.
    
    \pre        ini > fin
    
    \param[in] (int) ini        Numero inicial de la cuenta atrás
    \param[in] (int) fin        Numero final de la cuenta atrás
    \param[in] (int) espera     0 = sin sleep, 1 = con sleep de 5 ms
    """
    while fin > ini:
        fin -= 1
        if (espera == 1):
          sleep(5)


def repartir_param(numero, procesos, espera):
    """/**
    Reparte los parámetros para el número de procesos especificados.
    
    \pre        procesos > 0
    
    \param[in] (int)    numero       Número de inicio de la cuenta atrás
    \param[in] (int)    procesos     Número de procesos
    \param[in] (int)    espera       == espera en función contadorParallel
    
    \returns   (Lista)  param     lista de listas con argumentos para 
                                  contadorParallel
    """
    aux = ceil(numero / procesos)  #Divisor de la cuenta atrás
    param = []
    for i in range(procesos):
        ini = i * aux
        fin = ini + aux
        param.append([ini, fin, espera])
    else:
        #Para asegurar que el último fin sea igual a countdown
        param[i][1] = numero
    return param


def signal_handler(signal, frame):
    """/**
    Caza señal de interrupción y termina el script.
    
    \param[in] (Class)  signal   Señal mandada por el usuario (p.ej., SIGINT)
    \param[in] (Class)  frame    Frame de ejecución, apunta al frame que 
                                 interrumpe la señal.
    """
    print("\nPrograma terminado por interrupción del usuario.")
    sys.exit(1)

##############################################################################
#                                                                            #
#                                   MAIN()                                   #
#                                                                            #
##############################################################################
def main():
    input("Este script se encargará de realizar una cuenta atrás de manera "
          "concurrente, con el número de procesos que el usuario le proporcione, "
          "desde 10^6 hasta 0. Presione <Intro> para continuar")
    
    numero = 1000000
    
    #Decisión de parámetros y comprobación de errores
    while True:
        try:
            espera = int(input("¿Desea introducir un tiempo de espera de 5 ms "
                               "entre los ciclos de la cuenta atrás?"
                               "\n0-No\n1-Si\n"))
            procesos = int(input("Número de procesos: "))
            #espera entre 0 y 1 y numero de procesos mayor a 0
            if (not 0 <= espera <= 1 and not procesos > 0):
                raise ValueError
            else:
                break
        #Checkeo de errores
        except ValueError:
            print("Por favor, introduzca 0 o 1 para el parámetro de espera, "
                  "y un numero entero positivo mayor a 0 para los procesos.")
            
    #Ajuste de CPU si excede el máximo permitido
    if (procesos > cpu_count()):
        procesos = cpu_count()
        print("El número de procesos excede el permitido. Se procederá con "
              "el máximo para su computador: {}".format(procesos))
    
                                         
    parametros = repartir_param(numero, procesos, espera)#Reparto de parámetros
    t_i = time()                                         #Tiempo inicial
    
    listaProcesos = []
    #Ejecución de la cuenta atrás con un pool de procesos
    for i in range(procesos):
        listaProcesos.append(Process(target = contadorParallel, args = parametros[i],))
        listaProcesos[i].start()

    for i in range(procesos):
        listaProcesos[i].join()
        
    t_f = time() #Tiempo final
    
    #Se envía el resultado a stdout
    print("Tiempo de ejecución: {}".format(t_f - t_i))
  
if __name__ == "__main__":
    #Se establece la captura de señales
    signal.signal(signal.SIGINT, signal_handler)
    main()
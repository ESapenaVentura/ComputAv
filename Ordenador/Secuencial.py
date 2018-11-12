# -*- coding: utf-8 -*-
"""
Cuestionario de Programación y Técnicas Computacionales Avanzadas en 
Bioinformática

Cuestionario grupal 1: Script secuencial

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

from time import sleep, time

def contador(numero, espera = 0):
    """/**
    Cuenta atrás con tiempo de espera condicional.
  
    \param[in] (int)      numero   Numero de inicio de la cuenta atrás
    \param[in] (Boolean)  espera   False = No sleep, True = sleep de 5 ms
  
    \note   No tiene return
    """
    while numero > 0:
        numero -= 1
        if (espera == 1):
            sleep(5)

def signal_handler(signal, frame):
    """/**
    Caza señal de interrupción y termina el script.
    
    \param[in] (Class)  signal   Señal mandada por el usuario (p.ej., SIGINT)
    \param[in] (Class)  frame    Frame de ejecución, apunta al frame que 
                                 interrumpe la señal.
    """
    input("\nPrograma terminado por interrupción del usuario.")
    sys.exit(1)

##############################################################################
#                                                                            #
#                                   MAIN()                                   #
#                                                                            #
##############################################################################
def main():
    input("Este script se encargará de realizar una cuenta atrás de manera "
          "secuencial, desde 10^6 hasta 0. Presione <Intro> para continuar")
    
    numero = 10 ** 6
    
    #Decisión del parámetro de tiempo de espera entre ciclos
    while True:
        try:
            espera = int(input("¿Desea introducir un tiempo de espera de 5 ms "
                               "entre los ciclos de la cuenta atrás?"
                               "\n0-No\n1-Si\n"))
            if (not 0 <= espera <= 1): #No es 0 ni 1
                raise ValueError
            else:
                break
        #Checkeo de errores
        except ValueError:
            print("Por favor, introduzca 0 o 1")
    
    #Tiempo y ejecución de la función de cuenta atrás.
    t_i = time()
    contador(numero, espera)
    t_f = time()
    
    #Se envía el resultado a stdout.
    print("Tiempo de ejecución: {}".format(t_f - t_i))
  
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler) #Se establece la señal
    main()
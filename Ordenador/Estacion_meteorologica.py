#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 18:12:24 2018

@authors: -Alejandro Cebrian del Valle
          -Enrique Sapena Ventura
          -Pedro Salguero García
          -Raúl Pérez Moraga
"""

from multiprocessing import Process, Pipe
from random import randint, random
import datetime
from time import sleep, time

def enviar(conexion):
    marca = 11
    while True:
        if (marca == 24):
            marca = 0
        ts = datetime.datetime.fromtimestamp(time()).strftime("%Y-%m-%d "
                                                              "%H:%M:%S")
        conexion.send((ts,round(randint(25, 30) + random(),3),
                       randint(30, 75),randint(10, 15)))
        marca += 1
        sleep(0.1)

def main():
    padre, hijo = Pipe()
    hijo_p = Process(target=enviar, args=(hijo,))
    datos = []
    hijo_p.start()
    contador = 0
    while contador < 5:
        datos.append(padre.recv())
        sleep(0.15)
        contador += 0.15
    hijo_p.terminate()
    for resultados in datos:
        print("Tiempo: {} horas, Temperatura: {}ºC, {}% de humedad, Viento: "
              "{} km/h".format(*resultados))
    print("Hijo terminado, a continuación se mostrará lo que falta por "
          "imprimir")
    while(padre.poll()):
        resSobrantes = padre.recv()
        print("Tiempo: {} horas, Temperatura: {}ºC, {}% de humedad, "
              "Viento: {} km/h".format(*resSobrantes))
        continue
    padre.close()
    hijo.close()
    print("Terminado")
    
    
if __name__ == "__main__":
    main()
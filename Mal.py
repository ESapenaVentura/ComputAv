#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 18:19:26 2018

@author: qq
"""

def encontrarDivisores(numero):
    lista = []
    for i in range(2, numero-1):
        if (numero % i == 0):
            lista.append(i)
    return lista

def Main():
    numero = int(input("Introduzca numero: "))
    resultado = encontrarDivisores(numero)
    print(resultado, sep=", ")

if __name__ == "__main__":
    Main()
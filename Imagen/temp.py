# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
import numpy as np
from multiprocessing import Array, cpu_count, Process
from time import time


class NotPPM(Exception):
    """/**
    Excepción para poder salir del programa en caso de que la imagen no sea un 
    ppm tipo "ASCII" (Número mágico == P3). Se añade como subclase de 
    "Exception".
    """
    def __init__(self,*args,**kwargs):
        """/**
        Inicializador de la clase.
        """
        Exception.__init__(self,*args,**kwargs)


def lectura_ppm(nom_archivo):
    """/**
    Lectura de un archivo ppm.
    
    \pre        import numpy as np
    
    
    \param[in]  (str)           nom_archivo     Nombre del archivo.
    
    \returns:   (NumPy vector)  ppm             Vector(1xN) con la imagen.
                (lista)         firstrows      Primeras 3 filas de la imagen.
        
    """
    ppm = np.loadtxt(nom_archivo, dtype = int, skiprows = 3)
    ppm = ppm.reshape(-1) #Reestructuración a dimensión 1xN
    
    firstrows = []
    with open(nom_archivo, "r") as f:
        for _ in range(3):
            firstrows.append(f.readline()) #3 Primeras filas
    
    return ppm, firstrows


def ind_division(n_procesos, long_vector):
    """\**
    Cálculo de índices de división del vector para multiproceso.
    
    \param[in]  (int)       n_procesos      Número de procesos
    \param[in]  (int)       long_vector     Longitud del vector a dividir.
    
    \returns:   (lista)     indices         @{
                                             (int) ini Indice de inicio
                                             (int) fin Indice Final
                                             }
    """
    indices = []
    divisor = long_vector // n_procesos
    for i in range(n_procesos):
        ini = divisor * i
        fin = ini + divisor
        indices.append([ini, fin])
    else:
        #Al último "fin" se le da el valor de longitud del vector
        indices[i][1] = long_vector     
    
    return indices
    

def busqueda_maxmin(ini, fin, img_vector, mini, maxi):
    """\**
    Búsqueda de máximos y mínimos para cada color (RGB).
    
    \param[in]  (int)       ini     Indice inicial del vector para buscar.
    \param[in]  (int)       fin     Indice final del vector para buscar.
    \param[in]  (Multiprocess Array) img_vector  Vector que contiene la imagen.
    \param[in]  (Multiprocess Array) mini        Vector que contendrá el valor 
                                                 mínimo para cada pixel.
    \param[in]  (Multiprocess Array) maxi        Vector que contendrá el valor 
                                                 máximo para cada pixel.
                                                 
    \note       No hay return, puesto que se va escribiendo en los Arrays
                de máximos y mínimos.
    """
    for i in range(ini, fin):
        if img_vector[i] < mini[i % 3]:
            mini[i % 3] = img_vector[i]
        if img_vector[i] > maxi[i % 3]:
            maxi[i % 3] = img_vector[i]
        
def precalc(mini, maxi):
    """\**
    Función dedicada al precálculo de todos los valores posibles entre el
    valor más bajo del array "mini" y el valor más alto del array "maxi",
    aplicando la fórmula "int ( (val_ori – min) / (max – min) * 256)", siendo
    "val_ori" el valor de i para cada iteración.
    
    \param[in]  (Multiprocess Array) mini        Vector que contiene el valor 
                                                 mínimo para cada pixel.
    \param[in]  (Multiprocess Array) maxi        Vector que contiene el valor 
                                                 máximo para cada pixel.
                                                 
    \returns:    (list)    precalc_vector        Vector con todos los valores
                                                 posibles entre mini y maxi
    
    \note   Por lo general, hacer un precalculo de todos los valores posibles 
            es más eficiente que aplicar la fórmula para todos los valores del
            vector de imagen. En este caso en particular (lena), la imagen es
            de 2133 x 2133, con una profundidad de color de 255. Por lo tanto,
            en el peor de los casos (hay un pixel con valor 0 y otro con valor
            255), se harían 256 * 3 (R, G y B) = 768 cálculos, frente a 
            2133 * 2133 * 3 = 13649067 cálculos. Puede darse el caso de que la 
            imagen no sea muy grande (p.ej, 200 * 200) y la profundidad de color
            sí lo sea (max. de 65536 y mínimo de 0), en cuyo caso sí que sería 
            más eficiente hacer los cálculos sobre el vector de imagen, pero 
            es un caso muy raro.
    """
    divisor = [(maxi[i] - mini[i]) / 256 for i in range(3)] #divisor común
    precalc_vector = [0] * (max(maxi) + 1)
    for i in range(min(mini), max(maxi) + 1):
        #Para cada valor de i le corresponde una lista de valores en el vector
        precalc_vector[i] = [int((i - mini[j]) / divisor[j]) for j in range(3)]
    
    return precalc_vector
        
  
def better_img(img_vector, ini, fin, precalc_vector):
    """\**
    Corrección de imagen mediante ampliación del histograma de colores.
    
    \param[in]  (int)       ini     Indice inicial del vector para buscar.
    \param[in]  (int)       fin     Indice final del vector para buscar.
    \param[in]  (Multiprocess Array) img_vector  Vector que contiene la imagen.
    \param[in]  (lista)     precalc_vector  Vector con todos los valores 
                                            posibles de corrección de la 
                                            imagen.
                                            
    \note       No hay return, puesto que se escribe en el Array de la imagen.
    """
    for i in range(ini, fin):
        img_vector[i] = precalc_vector[img_vector[i]][i % 3]

def escribe_img(nom_archivo, vector_img, firstrows):
    """/**
    Escritura de la imagen en formato PPM tipo "ASCII".
    
    \pre        import numpy as np
    
    
    \param[in]  (str)           nom_archivo     Nombre del archivo.
    \param[in]  (Multiprocess Array) vector_img Vector que contiene la imagen.
    \param[in]  (lista)         firstrows       Lista que contiene las 3 
                                                primeras filas de la imagen.

    \note   Para una escritura más sencilla, se emplea una función de numpy 
            que copia vectores y matrices a archivos.
    """
    #Conversión a matriz de las dimensiones de la imagen original
    dim_img = (int(firstrows[1].split()[0]), int(firstrows[1].split()[1]))
    matrix = np.array(vector_img)
    matrix.reshape((dim_img[0], dim_img[1] * 3))
    
    #Escritura
    np.savetxt(nom_archivo[:-4] + "_mejorada.ppm", matrix, fmt="%d", 
               header = "".join(firstrows), comments = "")


def main():
    while True:
        #nom_archivo = input("Introduzca el nombre del archivo: ")
        nom_archivo = "lena_brillante.ppm"
        if not nom_archivo.endswith(".ppm"):
            print("Por favor, introduzca un fichero con extensión .ppm")
            continue
        try:
            #n_procesos = int(input("Introduzca el número de procesos: "))
            n_procesos = 1
            if n_procesos > cpu_count():
                print("Ha introducido un número de procesos superior al "
                      "permitido por su ordenador. Se ha cambiado a {} "
                      .format(cpu_count()))
                n_procesos = cpu_count()
        except ValueError:
            print("Por favor, introduzca un número de procesos válido "
                  "(Número entero). Para su ordenador, el número máximo de "
                  "procesos es {}".format(cpu_count()))
            continue
        break
    ppm, firstrows = lectura_ppm(nom_archivo)
    if not firstrows[0].startswith("P3"):
        raise NotPPM
    indices = ind_division(n_procesos, len(ppm))
    
    #Creación de los Arrays
    array_img = Array("i", ppm, lock = False)
    min_array = Array("i", [ppm[0]] * 3, lock = False)
    max_array = Array("i", [ppm[0]] * 3, lock = False)
    
    #Creación del pool de procesos, asignación de trabajo y finalización.
    pool = [Process(target = busqueda_maxmin, 
                    args = (*indices[i], array_img,min_array, max_array)) 
                    for i in range(n_procesos)]
    for worker in pool:
        worker.start()
    for worker in pool:
        worker.join()
        
    #Pre-cálculo de los valores.
    precalc_vector = precalc(min_array, max_array)

    #Creación del pool de procesos, asignación de trabajo y finalización.
    pool = [Process(target = better_img, 
                    args = (array_img, *indices[i], precalc_vector)) 
                    for i in range(n_procesos)]
    for worker in pool:
        worker.start()
    for worker in pool:
        worker.join()

    #Escritura de la imagen.
    escribe_img(nom_archivo, array_img, firstrows)
    
    

if __name__ == "__main__":
    try:
        t_i = time()
        main()
        print("Tiempo final: {} s".format(time() - t_i))
    except NotPPM:
        input("No es un archivo de imagen PPM con un número mágico \"P3\". "
              "Revisalo y vuelve a lanzar el programa. Presione <intro> "
              "para salir.")
#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

# CONSTANTES


import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from random import uniform



class LayoutGraph:

    def __init__(self, grafo, iters, refresh, c1, c2, verbose = False):
        '''
        Parametros de layout:
        iters: cantidad de iteraciones a realizar
        refresh: Numero de iteraciones entre actualizaciones de pantalla.
        0 -> se grafica solo al final.
        c1: constante usada para calcular la repulsion entre nodos
        c2: constante usada para calcular la atraccion de aristas
        '''

        # Guardo el grafo
        self.grafo = grafo
        self.vertices = grafo[0]
        self.aristas = grafo[1]

        # Inicializo estado
        # Completar
        self.posicion_x = {}  # Diccionario, la clave es el vertice el valor la posición x
        self.posicion_y = {}  # Diccionario, la clave es el vertice el valor la posición y
        self.fuerzas = {}
        self.acum_x = {}
        self.acum_y = {}
        self.t = 1
        self.ancho = 10000
        self.epsilon = 0.005
        self.g = 0.1  # Constante de gravedad

        # Guardo opciones
        self.iters = iters
        self.verbose = verbose
        # TODO: faltan opciones
        self.refresh = refresh
        self.c1 = c1
        self.c2 = c2


    def posiciones_random(self):
        for vertice in self.vertices:
            self.posicion_x[vertice] = uniform(0, self.ancho)
            self.posicion_y[vertice] = uniform(0, self.ancho)

    def distancia(self, vertice0, vertice1):
        d = sqrt((self.posicion_x[vertice0] - self.posicion_x[vertice1])**2 + (self.posicion_y[vertice0] - self.posicion_y[vertice1])** 2)
        return d

    def mul_escalar(self, vector, e):
        v1 = (vector[0] * e, vector[1] * e)
        return v1

    def fuerza_atraccion(self, d):
        k = self.c2 * sqrt(self.ancho*self.ancho / len(self.vertices))
        f = d**2 / k
        return f

    def fuerza_repulsion(self, d):  #Está bien
        k = self.c1 * sqrt(self.ancho*self.ancho / len(self.vertices))
        return k**2 / d

    def inicializar_acumuladores(self): #Está bien
        for vertice in self.vertices:
            self.acum_x[vertice] = 0
            self.acum_y[vertice] = 0

    def calcular_fuerza_atraccion(self):  #Está bien
        for arista in self.aristas:
            d = self.distancia(arista[0], arista[1])
            mod_fa = self.fuerza_atraccion(d)

            # Consideramos el caso de divisiones por 0
            while (d < 0):
                f = random.random()
                self.posicion_x[arista[0]] += f
                self.posicion_y[arista[0]] += f
                self.posicion_x[arista[1]] -= f
                self.posicion_y[arista[1]] -= f
                d = dist(arista[0], arista[1])

            mod_fa = self.fuerza_atraccion(d)
            fx = (mod_fa * (self.posicion_x[arista[1]] - self.posicion_x[arista[0]])) / d
            fy = (mod_fa * (self.posicion_y[arista[1]] - self.posicion_y[arista[0]])) / d

            self.acum_x[arista[0]] += fx
            self.acum_y[arista[0]] += fy
            self.acum_x[arista[1]] -= fx
            self.acum_y[arista[1]] -= fy

    def calcular_fuerza_repulsion(self): #Está bien
        for vertice1 in self.vertices:
            for vertice2 in self.vertices:
                    if vertice1 != vertice2:
                        d = self.distancia(vertice1, vertice2)

                        # Consideramos el caso de divisiones por 0
                        while (d < self.epsilon):
                            f = random.random()
                            self.posicion_x[vertice1] += f
                            self.posicion_y[vertice1] += f
                            self.posicion_x[vertice2] -= f
                            self.posicion_y[vertice2] -= f
                            d = distancia(vertice1, vertice2)

                        mod_fa = self.fuerza_repulsion(d)
                        fx = (mod_fa * (self.posicion_x[vertice2] - self.posicion_x[vertice1])) / d
                        fy = (mod_fa * (self.posicion_y[vertice2] - self.posicion_y[vertice1])) / d

                        self.acum_x[vertice1] -= fx
                        self.acum_y[vertice1] -= fy
                        self.acum_x[vertice2] += fx
                        self.acum_y[vertice2] += fy



    def actualizar_posiciones(self):  #Está bien, pero pensar si funciona cuando se va de los límites de la pantalla.
        for vertice in self.vertices:

            f = (self.acum_x[vertice], self.acum_y[vertice])
            modulo_f = sqrt(f[0]**2 + f[1]**2)
            if modulo_f > self.t:
                f = (f[0] / modulo_f * self.t , f[1] / modulo_f * self.t)
                (self.acum_x[vertice], self.acum_y[vertice]) = f

            self.posicion_x[vertice] = self.posicion_x[vertice] + self.acum_x[vertice]
            self.posicion_y[vertice] = self.posicion_y[vertice] + self.acum_y[vertice]



    def calcular_fuerza_gravedad(self):  #Está bien.
        centro = self.ancho / 2
        for vertice in self.vertices:

            d = sqrt((self.posicion_x[vertice] - centro)**2 + (self.posicion_y[vertice] - centro)** 2)

            #Consideramos el caso de divisiones por 0
            while d < self.epsilon:
                while (d < self.epsilon):
                    f = random.random()
                    self.posicion_x[vertice] += f
                    self.posicion_y[vertice] += f
                    d = sqrt((self.posicion_x[vertice] - centro)**2 + (self.posicion_y[vertice] - centro)** 2)

                fx = ((self.g * (pos_x - self.posicion_x[vertice])) / d)
                fy = ((self.g * (pos_y - self.posicion_y[vertice])) / d)
                self.acum_x[vertice] -= fx
                self.acum_y[vertice] -= fy

    def actualizar_temperatura(self):  #Está bien.
        self.t = self.t * self.g  # Multiplicamos por la constante definida.

    def step(self):
        self.inicializar_acumuladores()
        self.calcular_fuerza_atraccion()
        self.calcular_fuerza_repulsion()
        self.calcular_fuerza_gravedad()
        self.actualizar_posiciones()
        self.actualizar_temperatura()

    def show_graph(self):
        plt.pause(0.0001)
        x = [self.posicion_x[i] for i in self.grafo[0]]
        y = [self.posicion_y[i] for i in self.grafo[0]]
        plt.clf()

        plt.scatter(x, y)  # dibuja los puntos.

        for arista in self.aristas:
            vertice1 = arista[0]
            vertice2 = arista[1]
            plt.plot((self.posicion_x[vertice1], self.posicion_x[vertice2]),
                     (self.posicion_y[vertice1], self.posicion_y[vertice2]))

    def layout(self):
        '''
        Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
        un layout
        '''
        self.posiciones_random()
        plt.ion()
        for i in range(self.iters):
            if self.refresh != 0 and i % self.refresh == 0:  #Ya que imprime cada determinadas iteraciones.
                    self.step()
                    self.show_graph()
        if self.refresh == 0:
            self.show_graph()
        plt.ioff()  # lo cierra
        plt.show()  # lo muestra

def main():
    # Definimos los argumentos de linea de comando que aceptamos
    parser = argparse.ArgumentParser()

    # Verbosidad, opcional, False por defecto
    parser.add_argument(
        '-v', '--verbose',
        action = 'store_true',
        help = 'Muestra mas informacion al correr el programa'
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '--iters',
        type = int,
        help = 'Cantidad de iteraciones a efectuar',
        default = 50
    )
    # Temperatura inicial
    parser.add_argument(
        '--temp',
        type = float,
        help = 'Temperatura inicial',
        default = 100.0
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help = 'Archivo del cual leer el grafo a dibujar'
    )

    args = parser.parse_args()

    # Descomentar abajo para ver funcionamiento de argparse
    print(args.verbose)
    print(args.iters)
    print(args.file_name)
    print(args.temp)
    # return

    # TODO: Borrar antes de la entrega
    grafo1 = ([1, 2, 3, 4, 5, 6, 7],
              [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])

    # Creamos nuestro objeto LayoutGraph
    layout_gr = LayoutGraph(
        grafo1,  # TODO: Cambiar para usar grafo leido de archivo
        iters = args.iters,
        refresh = 1,
        c1 = 0.1,
        c2 = 5.0,
        verbose = args.verbose
    )

    # Ejecutamos el layout
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  criacaoAmostras.py
import numpy as np
from shapely.geometry import Polygon, Point


class Poligono(object):
    """Classe para a geração de polígonos"""
    def __init__(self, id, nome, cor):
        self.eixoX = np.asarray([])
        self.eixoY = np.asarray([])
        self.poligono = 0
        self.id = id
        self.nome = nome
        self.cor = cor

    def criarPoligono(self, coordenadas):
        for i in range(len(coordenadas)):
            self.eixoX = np.append(self.eixoX, coordenadas[i][0])
            self.eixoY = np.append(self.eixoY, coordenadas[i][1])
        self.poligono = Polygon(coordenadas)

    def verificaCoordenadaPoligono(self, ponto):
        return self.poligono.contains(Point(ponto))

    def getPontosQuadradoQuadrado(self):
        # self.poligono.bounds = (minx, miny, maxx, maxy)
        return self.poligono.bounds

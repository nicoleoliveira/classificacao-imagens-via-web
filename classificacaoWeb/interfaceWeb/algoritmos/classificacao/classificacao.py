#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  classificacao_4.py
import numpy as np
from osgeo import gdal
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from interfaceWeb.algoritmos.classificacao.criacaoAmostras import Poligono

class Classificador(object):
    """Classe que traz as operações que devem ser feitas sobre a imagem que será classificada"""
    def __init__(self, imagem):
        self.imagem = imagem
        self.matrizImagem = []
        self.matrizClasses = []
        self.poligonos = []
        self.coordenadasPoligonos = [None, None]
        self.linhas = 0
        self.colunas = 0
        self.bandas = 0

    def getLinhaColunaBanda(self):
        self.linhas = self.matrizImagem.shape[0]
        self.colunas = self.matrizImagem.shape[1]
        self.bandas = self.matrizImagem.shape[2]

    def imagemParaMatriz(self):
        raster_dataset = gdal.Open(self.imagem, gdal.GA_ReadOnly)
        geo_transform = raster_dataset.GetGeoTransform()
        proj = raster_dataset.GetProjectionRef()

        for b in range(1, raster_dataset.RasterCount+1):
            banda = raster_dataset.GetRasterBand(b)
            self.matrizImagem.append(banda.ReadAsArray())

    def empilhamentoBandas(self):
        self.matrizImagem = np.dstack(self.matrizImagem)

    def criarPoligonos(self, listaAmostras):
        for amostra in listaAmostras:
            id = amostra['id']
            nome = amostra['label']
            cor = self.convertHexParaRGB(amostra['color'])
            poligono = Poligono(id, nome, cor)
            poligono.criarPoligono(amostra['points'])
            self.poligonos.append(poligono)

    def convertHexParaRGB(self, cor):
        hex = cor.lstrip('#')
        return tuple(int(hex[i: i+2], 16) for i in (0, 2 ,4))

    def getCoordenadasPoligonos(self):
        self.matrizClasses = np.zeros((self.colunas, self.linhas))
        coordX = []
        coordY = []

        for idPoligono, poligono in enumerate(self.poligonos):

            bordas = poligono.getPontosQuadradoQuadrado()

            for idX in range(int(bordas[0]), int(bordas[2]+1)):
                for idY in range(int(bordas[1]), int(bordas[3]+1)):
                    ponto = (idX,idY)
                    if poligono.verificaCoordenadaPoligono(ponto):
                        self.matrizClasses[idX][idY] = poligono.id
                        coordX.append(idX)
                        coordY.append(idY)

        self.coordenadasPoligonos[1] = np.asarray(coordX)
        self.coordenadasPoligonos[0] = np.asarray(coordY)
        self.matrizClasses = self.matrizClasses.transpose()

    def desempilharBandas(self):
        numeroAmostras = self.linhas * self.colunas
        self.matrizImagem = self.matrizImagem.reshape((numeroAmostras, self.bandas))

def classificacaoInit(imagem, amostras):
    classificacao = Classificador(imagem)
    classificacao.criarPoligonos(amostras)
    classificacao.imagemParaMatriz()
    classificacao.empilhamentoBandas()
    classificacao.getLinhaColunaBanda()
    classificacao.getCoordenadasPoligonos()
    classificador = RandomForestClassifier(n_jobs=2)
    amostras = classificacao.matrizImagem[classificacao.coordenadasPoligonos]
    classes = classificacao.matrizClasses[classificacao.coordenadasPoligonos]
    classificador.fit(amostras, classes)
    classificacao.desempilharBandas()
    resultado = classificador.predict(classificacao.matrizImagem)
    imagemClassificada = resultado.reshape((classificacao.linhas, classificacao.colunas))
    return imagemClassificada

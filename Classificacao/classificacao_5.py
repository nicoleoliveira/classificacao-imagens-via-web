#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  classificacao_4.py
import numpy as np
from osgeo import gdal
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from criacaoAmostras import Poligono
from coordenadasTeste import coordenadasXYVegetacao, coordenadasXYVegetacaoSecundaria, coordenadasXYRio, coordenadasXYSoloAberto

class Classificador(object):
    """Classe que traz as operações que devem ser feitas sobre a imagem que será classificada"""
    def __init__(self, imagem):
        self.imagem = imagem
        self.matrizImagem = []
        self.matrizImagemEmpilhada = None
        self.matrizClasses = []
        self.poligonos = []
        self.coordenadasPoligonos = [None, None]
        self.linhas = 0
        self.colunas = 0
        self.bandas = 0

    def getLinhaColunaBanda(self):
        self.linhas = self.matrizImagemEmpilhada.shape[0]
        self.colunas = self.matrizImagemEmpilhada.shape[1]
        self.bandas = self.matrizImagemEmpilhada.shape[2]

    def imagemParaMatriz(self):
        raster_dataset = gdal.Open(self.imagem, gdal.GA_ReadOnly)
        geo_treoansform = raster_dataset.GetGeoTransform()
        proj = raster_dataset.GetProjectionRef()

        for b in range(1, raster_dataset.RasterCount+1):
            banda = raster_dataset.GetRasterBand(b)
            self.matrizImagem.append(banda.ReadAsArray())
        #~ print (bands_data[1][683][138])

    def empilhamentoBandas(self):
        self.matrizImagemEmpilhada = np.dstack(self.matrizImagem)

    def criarPoligonos(self, listaAmostras):
        for amostra in listaAmostras:
            coordenadas = amostra[0]
            id = amostra[1]
            nome = amostra[2]
            poligono = Poligono(id, nome)
            poligono.criarPoligono(coordenadas)
            self.poligonos.append(poligono)

    def getCoordenadasPoligonos(self):
        self.matrizClasses = np.zeros((self.linhas, self.colunas))
        coordX = []
        coordY = []

        for idPoligono, poligono in enumerate(self.poligonos):

            bordas = poligono.getPontosQuadradoQuadrado()
            # subMatriz = self.matrizImagem[0][bordas[0]:(bordas[2]+1), bordas[1]:(bordas[3]+1)]
            for idX in range(int(bordas[0]), int(bordas[2]+1)):
                for idY in range(int(bordas[1]), int(bordas[3]+1)):
                    ponto = (idX,idY)
                    if poligono.verificaCoordenadaPoligono(ponto):
                        self.matrizClasses[idX][idY] = poligono.id
                        coordX.append(idX)
                        coordY.append(idY)

        self.coordenadasPoligonos[0] = np.asarray(coordX)
        self.coordenadasPoligonos[1] = np.asarray(coordY)


if __name__ == "__main__":
    classificacao = Classificador("itinga2.tif")
    listaAmostras = [coordenadasXYVegetacao(), coordenadasXYVegetacaoSecundaria(), coordenadasXYRio(), coordenadasXYSoloAberto()]
    classificacao.criarPoligonos(listaAmostras)
    classificacao.imagemParaMatriz()
    classificacao.empilhamentoBandas()
    classificacao.getLinhaColunaBanda()
    classificacao.getCoordenadasPoligonos()
    classificador = RandomForestClassifier(n_jobs=2)
    classificador.fit(classificacao.matrizImagemEmpilhada[classificacao.coordenadasPoligonos], classificacao.matrizClasses[classificacao.coordenadasPoligonos])
    resultado = classificador.predict(classificacao.matrizImagem)
    imagemClassificada = resultado.reshape((classificacao.linhas, classificacao.colunas))

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import os
from PIL import Image
from scipy.ndimage import imread
from scipy.misc import imresize
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

def img_para_matriz_redimensionando(arquivo, tamanho_amostras_padrao):
    matriz = imread(arquivo, True)
    matriz = imresize(matriz, tamanho_amostras_padrao)
    return matriz

def rotulos_e_imagens(img_dir):
    imagens = []
    rotulos = []
    for f in os.listdir(img_dir):
        imagens.append(img_dir + f)
        rotulos.append(f.split(".")[0])
    return imagens, rotulos


def amostras_tamanho_imagem(imagem_matriz, linha, coluna, tamanho_amostras_padrao):
    m_temp = np.zeros((linha, coluna))
    for i in range(tamanho_amostras_padrao):
        for j in range(tamanho_amostras_padrao):
            m_temp[i][j] = imagem_matriz[i][j]

    return m_temp


def main():
    tamanho_amostras_padrao = (200, 200)
    imagem_para_prever = imread("imagem_grande_para_cortar.jpg", True)
    linhas, colunas = imagem_para_prever.shape
    qtd_amostras_imagem_prever = linhas * colunas

    img_dir = "amostras/"
    images, rotulos = rotulos_e_imagens(img_dir)
    qtd_amostras = len(rotulos)

    data = []
    for image in images:
        img = img_para_matriz_redimensionando(image, tamanho_amostras_padrao)
        amostra = amostras_tamanho_imagem(img, linhas, colunas, tamanho_amostras_padrao[0])
        data.append(amostra)
    
    data = np.array(data)
    data = data.reshape((qtd_amostras, -1))

    flat_pixels = imagem_para_prever.reshape((qtd_amostras_imagem_prever))
    print(flat_pixels)
    print("#######################")
    print(len(data[0]))
    classificador =  RandomForestClassifier(n_jobs=4, n_estimators=10)

    classificador.fit(data, rotulos)
    previsto = classificador.predict(flat_pixels)
    #~ classificacao = previsto.reshape((linhas, colunas))
    print(previsto)

if __name__ == "__main__":
    main()

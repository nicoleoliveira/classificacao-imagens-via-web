#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  raster_em_matriz.py
#  
#  Copyright 2017 Nicole <aluno@desktop-fabrica>
#  

import numpy as np
import os
from PIL import Image
from scipy.ndimage import imread
from scipy.misc import imresize
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier


TAMANHO_PADRAO = (200, 200)

def img_para_matriz(arquivo):
    matriz = imread(arquivo, True)
    matriz = imresize(matriz, TAMANHO_PADRAO)
    return matriz


def rotulos_e_imagens(img_dir):
    imagens = []
    rotulos = []
    for f in os.listdir(img_dir):
        imagens.append(img_dir + f)
        rotulos.append(f.split(".")[0])
    return imagens, rotulos

img_dir = "amostras/"
images, rotulos = rotulos_e_imagens(img_dir)
qtd_amostras = len(rotulos)

data = []
for image in images:
    img = img_para_matriz(image)
    data.append(img)

data = np.array(data)
data = data.reshape((qtd_amostras, -1))

imagem_para_prever = imread("imagem_grande_para_cortar.jpg", True)
linhas, colunas = imagem_para_prever.shape
qtd_amostras_imagem_prever = linhas * colunas
flat_pixels = imagem_para_prever.reshape((qtd_amostras_imagem_prever, -1))
print(flat_pixels)
print("#######################")
print(len(data[0]))
classificador =  RandomForestClassifier(n_jobs=4, n_estimators=10)

classificador.fit(data, rotulos)
previsto = classificador.predict(data[0])
#~ classificacao = previsto.reshape((linhas, colunas))
print(previsto)


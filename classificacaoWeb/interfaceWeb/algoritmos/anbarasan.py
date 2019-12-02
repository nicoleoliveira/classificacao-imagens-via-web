#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  anbarasan.py
# Código adaptado de http://stackoverflow.com/questions/28870504/converting-tiff-to-jpeg-in-python
#  
#  Copyright 2017 Nicole
import os
from PIL import Image

def converterTifJpg(imagem, caminho):    
    imagem_extensao = imagem.split(".")
    imagem_sem_extensao = imagem_extensao[0]
    extensao = imagem_extensao[1]
    
    if (extensao == "tif" or extensao == "tiff"):
        if os.path.isfile(imagem_sem_extensao + ".jpg"):
            print ("A jpeg file already exists for %s" % imagem_sem_extensao)

        else:
            saida = imagem_sem_extensao + ".jpg"
            im = Image.open(caminho + imagem)
            print ("Generating jpeg for %s" % imagem_sem_extensao)
            return im
            # im.save(saida, "JPEG", quality=100)
    else:
        print("Formato de imagem inválido!")


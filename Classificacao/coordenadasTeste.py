#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  coordenadasTeste.py
#
#  Copyright 2017 Nicole <aluno@desktop-fabrica>
#
import  PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow


def coordenadasXYVegetacao():
    xy = [(683,138), (465,272), (673,368), (1034,189)]
    return (xy, 1, "vegetação")

def coordenadasXYVegetacaoSecundaria():
    xy = [(663,101), (444,327), (616,463), (917,214)]
    return ( xy, 2, "vegetação secundária")

def coordenadasXYRio():
    xy = [(1423,105), (1250,236), (1370,369), (1593,188)]
    return (xy, 3, "rio")

def coordenadasXYSoloAberto():
    xy = [(1646,89), (1352,278), (1450,548), (1807,306)]
    return (xy, 4, "solo aberto")


#~ im = Image.open("itinga2.tif")
#~ draw = ImageDraw.Draw(im)
#~ draw.polygon(coordenadasXYRio(), fill=255)
#~ im.show()

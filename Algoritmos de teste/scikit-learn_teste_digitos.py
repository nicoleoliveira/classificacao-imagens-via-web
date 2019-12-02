#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  scikit-learn_teste_digitos.py
#  
#  Copyright 2017 Nicole <aluno@desktop-fabrica>
#  
import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics

digitos = datasets.load_digits()

imagens_e_rotulos = list(zip(digitos.images, digitos.target))

#~ for index, (imagem, rotulo) in enumerate(imagens_e_rotulos[:4]):
    #~ plt.subplot(2, 4, index + 1)
    #~ plt.axis('off')
    #~ plt.imshow(imagem, cmap=plt.cm.gray_r, interpolation='nearest')
    #~ plt.title('Treinando: %i' % rotulo)

qtd_amostras = len(digitos.images)
dados = digitos.images.reshape((qtd_amostras, -1))

classificador = svm.SVC(gamma=0.001)

print(digitos.target)
classificador.fit(dados[:qtd_amostras/2], digitos.target[:qtd_amostras/2])

esperado = digitos.target[qtd_amostras/2:]
previsto = classificador.predict(dados[qtd_amostras/2:])


#~ print("Classification report for classifier %s:\n%s\n"
      #~ % (classificador, metrics.classification_report(esperado, previsto)))
#~ print("Confusion matrix:\n%s" % metrics.confusion_matrix(esperado, previsto))

#~ imagens_e_previsoes = list(zip(digitos.images[qtd_amostras / 2:], previsto))
#~ for index, (image, prediction) in enumerate(imagens_e_previsoes[:4]):
    #~ plt.subplot(2, 4, index + 5)
    #~ plt.axis('off')
    #~ plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    #~ plt.title('Prediction: %i' % prediction)

#~ plt.show()

#~ print(classificador.predict(digitos.data[1])) # ele irá aparecer na tela [1]


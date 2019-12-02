#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  scikit-learn_teste_iris.py
#  
#  Copyright 2017 Nicole <aluno@desktop-fabrica>
#  
from sklearn import datasets
from sklearn.svm import SVC

iris = datasets.load_iris()
clf = SVC()
clf.fit(iris.data, iris.target)

print(iris.data)
print(list(clf.predict(iris.data[:3])))
clf.fit(iris.data, iris.target_names[iris.target])  
print(list(clf.predict(iris.data[:3])))

#coding: utf-8
import numpy as np
import os

from osgeo import gdal
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt

# A list of "random" colors (for a nicer output)
COLORS = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941"]


def create_mask_from_vector(vector_data_path, cols, rows, geo_transform,
                            projection, target_value=1):
    """Rasterize the given vector (wrapper for gdal.RasterizeLayer)."""
    data_source = gdal.OpenEx(vector_data_path, gdal.OF_VECTOR) # abre um arquivo raster ou vetorial como um GdalDataset
    layer = data_source.GetLayer(0) # returna o nome da camada
    driver = gdal.GetDriverByName('MEM')  # returna o driver
    target_ds = driver.Create('', cols, rows, 1, gdal.GDT_UInt16) #returna um conjunto de dados com este drive
    target_ds.SetGeoTransform(geo_transform) # calcula as coordenadas
    target_ds.SetProjection(projection) # coloca a projeção 
    gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[target_value]) #transforma o vetor em um raster
    return target_ds #retorna o raster do treinamento


def vectors_to_raster(file_paths, rows, cols, geo_transform, projection):
    """Rasterize all the vectors in the given directory into a single image."""
    #np.zeros returna um array de zeros
    labeled_pixels = np.zeros((rows, cols))
    print(labeled_pixels)
    for i, path in enumerate(file_paths):
        # i é o iterador, path é o caminho de cada arquivo
        label = i+1
        ds = create_mask_from_vector(path, cols, rows, geo_transform,
                                     projection, target_value=label)
        # ds é o treinamento rasterizado
        band = ds.GetRasterBand(1) #objeto gdal acesso aos dados do raster
        # ReadAsArray --> ler raster como um array
        labeled_pixels += band.ReadAsArray()
        ds = None
    print(labeled_pixels[0])
    return labeled_pixels


def write_geotiff(fname, data, geo_transform, projection):
    """Create a GeoTIFF file with the given data."""
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = data.shape
    dataset = driver.Create(fname, cols, rows, 1, gdal.GDT_Byte)
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    dataset = None  # Close the file


raster_data_path = "../data/image/2298119ene2016recorteTT.tif"
output_fname = "classification.tiff"
train_data_path = "../data/train"
validation_data_path = "../data/test"

#~ raster_data_path = "../itinga/Itinga20160513_Orthomosaic_export_TueMar21-b.jpg"
#~ output_fname = "classification.tiff"
#~ train_data_path = "../itinga"
#~ validation_data_path = "../data/test"


raster_dataset = gdal.Open(raster_data_path, gdal.GA_ReadOnly) # abrindo imagem raster
geo_transform = raster_dataset.GetGeoTransform() # calcular a localização de pixels de uma coordenada geoespacial
proj = raster_dataset.GetProjectionRef() # retorna o sistema de coordenadas
bands_data = []
# a função raster_dataset.RasterCount, conta o número de bandas. Neste exmplo, o número de bandas é igual a sete.

for b in range(1, raster_dataset.RasterCount+1):
    band = raster_dataset.GetRasterBand(b) # returna um objeto de banda
    bands_data.append(band.ReadAsArray()) # ler raster como um array, o que era um objeto, agora é um matriz com 7 dimensões

bands_data = np.dstack(bands_data) #empilha o array em outra dimensao
# bands_data.shape retorna uma tupla com: linha, coluna e o numero de dimensões.
rows, cols, n_bands = bands_data.shape

files = [f for f in os.listdir(train_data_path) if f.endswith('.shp')] # returna uma lista com os nomes dos arquivos de treinamento .shp

classes = [f.split('.')[0] for f in files] # returna uma lista com o nome das classes. 
shapefiles = [os.path.join(train_data_path, f) # returna uma lista com o caminho dos arquivos de treinamento
              for f in files if f.endswith('.shp')]

labeled_pixels = vectors_to_raster(shapefiles, rows, cols, geo_transform, proj) # pega os arquivos de treinamento e transforma eles em um vetor
is_train = np.nonzero(labeled_pixels) # retorna o indice dos elementos que não são zeros
training_labels = labeled_pixels[is_train] # é uma lista de rótulos de classes, onde o indice n corresponde ao pixel n da amostra.
training_samples = bands_data[is_train] # é a lista de pixels a serem usados para treinamento.

classifier = RandomForestClassifier(n_jobs=4, n_estimators=10) # n_jobs é a quantidade de núcleos de processador
classifier.fit(training_samples, training_labels)

n_samples = rows*cols # quantidade de pixels da imagem
flat_pixels = bands_data.reshape((n_samples, n_bands))
result = classifier.predict(flat_pixels) # faz a predição dos pixels da imagem band_data


classification = result.reshape((rows, cols))

f = plt.figure()
f.add_subplot(1, 2, 2)
r = bands_data[:,:,3]
g = bands_data[:,:,2]
b = bands_data[:,:,1]
rgb = np.dstack([r,g,b])
f.add_subplot(1, 2, 1)
plt.imshow(rgb/255)
f.add_subplot(1, 2, 2)
plt.imshow(classification)
plt.imsave(fname='classificationNicole3.jpg',
                          arr=classification)

#~ write_geotiff(output_fname, classification, geo_transform, proj)

#~ shapefiles = [os.path.join(validation_data_path, "%s.shp"%c) for c in classes]
#~ verification_pixels = vectors_to_raster(shapefiles, rows, cols, geo_transform, proj)
#~ for_verification = np.nonzero(verification_pixels)
#~ verification_labels = verification_pixels[for_verification]
#~ predicted_labels = classification[for_verification]

#~ print("Confussion matrix:\n%s" %
      #~ metrics.confusion_matrix(verification_labels, predicted_labels))
#~ target_names = ['Class %s' % s for s in classes]
#~ print("Classification report:\n%s" %
      #~ metrics.classification_report(verification_labels, predicted_labels,
                                    #~ target_names=target_names))
#~ print("Classification accuracy: %f" %
      #~ metrics.accuracy_score(verification_labels, predicted_labels))


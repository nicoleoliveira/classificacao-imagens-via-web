from django.shortcuts import render
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from interfaceWeb.models.imagem import Imagem
from interfaceWeb.models.imagemClassificada import ImagemClassificada
from interfaceWeb.serializers.imagem import ImagemSerializer
from interfaceWeb.serializers.imagemClassificada import ImagemClassificadaSerializer
from interfaceWeb.algoritmos.anbarasan import converterTifJpg

from interfaceWeb.algoritmos.classificacao.classificacao import classificacaoInit

from PIL import Image
import base64
import os.path
import matplotlib.pyplot as plt


class ImagemUploadViewSet(APIView):
    parser_classes = (FormParser, MultiPartParser)
    renderer_classes = (JSONRenderer, )
    caminho = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @csrf_exempt
    def post(self, request, format=None):

        serializer = ImagemSerializer(data={
            'upload': request.data['file']
        })

        if serializer.is_valid():
            serializer.save()
            image = Image.open(self.caminho + serializer.data['upload'])
            image.save(self.caminho + 'teste.jpg', "PNG", quality=100)
            imagemConvert = self.caminho + 'teste.jpg'

            with open(imagemConvert, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            stringSerializer = {'imagem': encoded_string}
            return Response({"id": serializer.data['id'], "data": stringSerializer})
        else:
            return Response(status=404)

class AmostrasViewSet(APIView):
    caminho = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @csrf_exempt
    def post(self, request, format=None):
        amostras = request.data['samples']
        imageUpload = Imagem.objects.get(id=request.data['id'])
        imageClassificada = classificacaoInit(self.caminho + '/media/' + str(imageUpload.upload), amostras)
        plt.imsave(fname='classificadaTemp.png', arr=imageClassificada)
        print('ok')
        
        image = Image.open(self.caminho + '/classificadaTemp.png')

        with open(self.caminho + '/classificadaTemp.png', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

            serializer = ImagemClassificadaSerializer(data={
                'codeBase64': str(encoded_string)
            })

            if serializer.is_valid():
                serializer.save()

                stringSerializer = {'imagem': encoded_string}
                return Response({"id": serializer.data['id'], "imagem": encoded_string})
            else:
                return Response(status=404)

        return Response(status=204)
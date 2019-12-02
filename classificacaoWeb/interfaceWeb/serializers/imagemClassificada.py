from rest_framework import serializers
from interfaceWeb.models.imagemClassificada import ImagemClassificada

class ImagemClassificadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemClassificada
        fields = '__all__'

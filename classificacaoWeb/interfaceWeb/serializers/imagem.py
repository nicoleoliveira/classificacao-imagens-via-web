from rest_framework import serializers
from interfaceWeb.models.imagem import Imagem

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = '__all__'

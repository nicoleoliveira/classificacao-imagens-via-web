from django.db import models

class Imagem(models.Model):
    upload = models.ImageField(upload_to="imagem/")

from rest_framework import serializers

from models.models import *


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'


class SalidaLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalidaLote
        fields = '__all__'


class EntradaLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaLote
        fields = '__all__'



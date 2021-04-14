# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models.models import Producto, Lote, SalidaLote, EntradaLote
from rest.serializers import ProductoSerializer, LoteSerializer, SalidaLoteSerializer, EntradaLoteSerializer



@api_view(['GET'])
def getAll(request):
    articulos = Producto.objects.all()
    print(len(articulos))
    if len(articulos) == 0:
        return Response("No existen articulos disponibles", status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = ProductoSerializer(articulos, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def getPorTipoProducto(request):
    tipo = request.data["tipo"]
    productosByType = Producto.objects.filter(tipo=tipo)
    if len(productosByType) == 0:
        return Response("No existen articulos disponibles", status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = ProductoSerializer(productosByType, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def getLotesByInvima(request):
    invima = request.data["invima"]
    lotesByInvima = Lote.objects.filter(producto=invima)
    if len(lotesByInvima) == 0:
        return Response("No lotes disponibles para este articulo.", status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = LoteSerializer(lotesByInvima, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def getSalidaLotesByInvima(request):
    invima = request.data["invima"]
    salidaLotesByInvima = SalidaLote.objects.filter(lote__producto=invima)
    if len(salidaLotesByInvima) == 0:
        return Response("Este lote no ha presentado salidas.", status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = SalidaLoteSerializer(salidaLotesByInvima, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def getEntradaLotesByInvima(request):
    invima = request.data["invima"]
    entradaLotesByInvima = EntradaLote.objects.filter(producto__producto=invima)
    if len(entradaLotesByInvima) == 0:
        return Response("Este lote no ha presentado entradas.", status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = EntradaLoteSerializer(entradaLotesByInvima, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def registrarEntradas(request):
    if request.method == 'POST':
        if request.data:
            for entrada in request.data:
                producto = Lote.objects.get(id=entrada["producto"])
                EntradaLote.create(entrada["cantidad_entrante"], producto, entrada["descripcion"])
            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response("Datos incorrectos.", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registrarSalidas(request):
    if request.method == 'POST':
        if request.data:
            for salida in request.data:
                producto = Lote.objects.get(id=salida["producto"])
                SalidaLote.create(salida["cantidad_salida"], producto, salida["descripcion"])
            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            return Response("Datos incorrectos.", status=status.HTTP_400_BAD_REQUEST)



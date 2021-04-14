from django.urls import path

from rest.views import getAll,getPorTipoProducto, getLotesByInvima, getSalidaLotesByInvima, getEntradaLotesByInvima, registrarEntradas, registrarSalidas

urlpatterns = [
    path('products-all/', getAll, name="product-all"),
    path('products-byType/', getPorTipoProducto, name="product-byType"),
    path('lote-byInvima/', getLotesByInvima, name="product-getLotes"),
    path('lote-salidas/', getSalidaLotesByInvima, name="product-salidaLote"),
    path('lote-entradas/', getEntradaLotesByInvima, name="product-entradaLote"),
    path('lote-registroEntrada/', registrarEntradas, name="product-registroEntrada"),
    path('lote-registroSalida/', registrarSalidas, name="product-registroSalida"),
]

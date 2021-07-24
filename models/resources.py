from import_export import resources

from models.models import Producto, Lote, SalidaLote, EntradaLote


class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = ('nombre', 'material',
                  'presentacion', 'proveedor',
                  'registro_invima', 'tipo')
        import_id_fields = ('producto_id',)
        exclude = ('descripcion',)


class LoteResource(resources.ModelResource):
    class Meta:
        model = Lote
        fields = ('producto', 'cantidad_entrada',
                  'fecha_ingreso', 'fecha_vencimiento',
                  'lote_del_producto',
                  )
        import_id_fields = ('lote_del_producto',)
        exclude = ('descripcion',)


class LoteEntradaResource(resources.ModelResource):
    class Meta:
        model = EntradaLote
        fields = ('producto', 'cantidad_entrada',
                  'fecha_entrada',
                  )
        import_id_fields = ('producto',)
        exclude = ('descripcion',)


class LoteSalidaResource(resources.ModelResource):
    class Meta:
        model = SalidaLote
        fields = ('producto', 'cantidad_salida',
                  'fecha_salida',
                  )
        import_id_fields = ('producto',)
        exclude = ('descripcion',)

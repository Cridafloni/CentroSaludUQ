from django.test import TestCase 

from models.models import Producto, Lote
from django.utils import timezone


class ProductoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Producto.objects.create(nombre="Guantes", proveedor="Guantes Quindio", registro_invima="No aplica", descripcion="Guantes de goma", material="Goma", presentacion="Caja de 5 pares", tipo="ELEMENTO DE ASEO")
        Producto.objects.create(nombre="Acetaminofen", proveedor="Bayer", registro_invima="JKOA123A", descripcion="10 mg", material="No Aplica", presentacion="5 mg", tipo="MEDICAMENTO")
        Producto.objects.create(nombre="Guantes", proveedor="Guantes Quindio", registro_invima="No aplica", descripcion="Guantes de goma", material="Goma", presentacion="Caja de 5 pares", tipo="ELEMENTO DE ASEO")
        producto1=Producto.objects.get(producto_id=1)
        start = timezone.now().date()
        Lote.objects.create(producto=producto1,cantidad_entrada=3,fecha_ingreso=start,lote_del_producto="asdqwesd")

    def test_nombre_name_label(self):
        producto1=Producto.objects.get(producto_id=1)
        field_label= producto1._meta.get_field("nombre").verbose_name
        self.assertEquals(field_label,"nombre")
    
    def test_proveedor_name_label(self):
        producto2=Producto.objects.get(producto_id=2)
        field_label= producto2._meta.get_field("proveedor").verbose_name
        self.assertEquals(field_label,"proveedor")

    def test_lote_name_lote(self):
        lote1=Lote.objects.get(producto=1)
        field_label= lote1._meta.get_field("lote_del_producto").verbose_name
        self.assertEquals(field_label,"lote del producto")

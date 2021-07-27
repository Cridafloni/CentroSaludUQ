from django.db import models
from django.utils import timezone

# Create your models here.
from django.utils.html import format_html


class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    proveedor = models.CharField(max_length=30)
    registro_invima = models.CharField(max_length=30)
    producto_id = models.AutoField(primary_key=True)
    fecha_registro = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    material = models.CharField(max_length=30, blank=True, null=True)
    presentacion = models.CharField(max_length=30)

    eliminado = models.BooleanField(default=True, verbose_name="En lista")
    fecha_eliminacion = models.DateField(null=True)

    MEDICAMENTO = "MEDICAMENTO"
    ASEO = "ASEO"
    INSUMO = "INSUMO"
    EQUIPO = "EQUIPO"
    SEGURIDAD_EN_EL_TRABAJO = "SEGURIDAD Y SALUD EN EL TRABAJO"
    OPTION_CHOICES = [
        (MEDICAMENTO, "MEDICAMENTO"),
        (ASEO, "ELEMENTO DE ASEO"),
        (INSUMO, "PRODUCTO E INSUMO"),
        (EQUIPO, "EQUIPO"),
        (SEGURIDAD_EN_EL_TRABAJO, "SEGURIDAD Y SALUD EN EL TRABAJO"),
    ]

    tipo = models.CharField(
        choices=OPTION_CHOICES, default=MEDICAMENTO, max_length=100
    )

    def save(self, force_insert=False, force_update=False):
        self.nombre = self.nombre.upper()
        self.proveedor = self.proveedor.upper()
        self.registro_invima = self.registro_invima.upper()
        self.material = self.material.upper()
        self.presentacion = self.presentacion.upper()
        self.tipo = self.tipo.upper()
        super(Producto, self).save(force_insert, force_update)

    def __str__(self):
        return "{} - {} - {}".format(self.tipo, self.nombre, self.presentacion)

    @property
    def lotes_registrados(self):
        lotes = Lote.objects.filter(producto__pk=self.pk)
        return len(lotes)

    @property
    def cantidad_unidades_disponibles(self):
        lotes = Lote.objects.filter(producto__pk=self.pk)
        total = 0
        for lote in lotes:
            total += lote.unidades_restantes
        return total

    class Meta:
        verbose_name_plural = "ARTÍCULO"
        verbose_name = "ARTÍCULOS"


class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_entrada = models.PositiveIntegerField(default=0)
    fecha_ingreso = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    lote_del_producto = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    eliminado = models.BooleanField(default=True, verbose_name="En lista")
    fecha_eliminacion = models.DateField(null=True)

    def save(self, force_insert=False, force_update=False):
        self.lote_del_producto = self.lote_del_producto.upper()
        super(Lote, self).save(force_insert, force_update)

    def __str__(self):
        return self.producto.nombre

    class Meta:
        verbose_name_plural = "LOTE"
        verbose_name = "LOTES"

    @property
    def registro_invima(self):
        invima = self.producto.registro_invima
        return invima

    @property
    def meses_vencimiento(self):
        end = self.fecha_vencimiento
        if end is None:
            return -1
        start = timezone.now().date()
        num_months = (end.year - start.year) * 12 + (end.month - start.month)
        return num_months

    @property
    def _meses_vencimiento(self):
        if self.meses_vencimiento == -1:
            return "NO APLICA"
        return self.meses_vencimiento

    @property
    def dias_vencimiento(self):
        end = self.fecha_vencimiento
        if end is None:
            return -1
        start = timezone.now().date()
        num_days = (
            (end.year - start.year) * 365
            + (end.month - start.month) * 30
            + (end.day - start.day)
        )
        return num_days

    @property
    def _dias_vencimiento(self):
        if self.dias_vencimiento == -1:
            return "NO APLICA"
        return self.dias_vencimiento

    @property
    def semaforizacion(self):
        meses = self.meses_vencimiento
        dias = self.dias_vencimiento
        if meses >= 11:
            return format_html(
                "<div style='width: 100px; \
                    height:15px; background-color:#008f39'>"
            )
        elif meses >= 5 and meses < 11:
            return format_html(
                "<div style='width: 100px; \
                    height:15px; background-color:#FFFF00'>"
            )
        elif meses > 0 and meses < 5 or (meses == 0 and dias >= 0):
            return format_html(
                "<div style='width: 100px; \
                    height:15px; background-color:#cb3234'>"
            )
        elif meses < 0 or (meses == 0 and dias < 0):
            return format_html(
                "<div style='width: 100px; \
                    height:15px; background-color:#000000'>"
            )

    @property
    def estado(self):
        meses = self.meses_vencimiento
        dias = self.dias_vencimiento
        if meses >= 11:
            return "VERDE"
        elif meses >= 5 < 11:
            return "AMARILLO"
        elif meses > 0 and meses < 5 or (meses == 0 and dias >= 0):
            return "ROJO"
        elif meses < 0 or (meses == 0 and dias < 0):
            return "NEGRO"

    @property
    def total_salidas(self):
        lotes = SalidaLote.objects.filter(producto=self.pk)
        return len(lotes)

    @property
    def total_entradas(self):
        lotes = EntradaLote.objects.filter(producto=self.pk)
        return len(lotes)

    @property
    def unidades_restantes(self):
        salidas = SalidaLote.objects.filter(producto=self.pk)
        entradas = EntradaLote.objects.filter(producto=self.pk)
        total_entradas = 0
        total_salidas = 0
        for lote in salidas:
            total_salidas += lote.cantidad_salida
        for lote in entradas:
            total_entradas += lote.cantidad_entrante
        return self.cantidad_entrada + total_entradas - total_salidas


class SalidaLote(models.Model):
    fecha_salida = models.DateField(auto_now_add=True)
    cantidad_salida = models.PositiveIntegerField(default=0)
    producto = models.ForeignKey(Lote, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)

    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "LOTE SALIDA"
        verbose_name = "LOTES SALIDA"

    def __str__(self):
        return "{} - {} - {}".format(
            self.producto.producto.tipo,
            self.producto.producto.nombre,
            self.producto.producto.presentacion,
        )

    @classmethod
    def create(cls, cantidad_salida, producto, descripcion):
        entrada = cls(
            cantidad_salida=cantidad_salida,
            producto=producto,
            descripcion=descripcion,
        )
        entrada.save()
        return entrada


class EntradaLote(models.Model):
    fecha_entrada = models.DateField(auto_now_add=True)
    cantidad_entrante = models.PositiveIntegerField(default=0)
    producto = models.ForeignKey(Lote, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)

    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "LOTE ENTRADA"
        verbose_name = "LOTES ENTRADA"

    @classmethod
    def create(cls, cantidad_entrante, producto, descripcion):
        entrada = cls(
            cantidad_entrante=cantidad_entrante,
            producto=producto,
            descripcion=descripcion,
        )
        entrada.save()
        return entrada

    def __str__(self):
        return "{} - {} - {}".format(
            self.producto.producto.tipo,
            self.producto.producto.nombre,
            self.producto.producto.presentacion,
        )

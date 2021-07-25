from datetime import datetime
from io import BytesIO

import dateutil

# import time
# from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from xlsxwriter.workbook import Workbook

from models.models import *
from models.resources import ProductoResource, LoteResource, LoteSalidaResource


class LoteInline(admin.TabularInline):
    model = Lote
    fields = (
        "producto",
        "cantidad_entrada",
        "fecha_ingreso",
        "fecha_vencimiento",
        "lote_del_producto",
    )
    extra = 1
    classes = ("collapse",)


class ProductoAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    admin.site.disable_action("delete_selected")
    resource_class = ProductoResource
    list_display = (
        "eliminado",
        "nombre",
        "material",
        "presentacion",
        "proveedor",
        "registro_invima",
        "tipo",
        "lotes_registrados",
        "cantidad_unidades_disponibles",
    )
    list_filter = ("tipo", ("fecha_registro", DateRangeFilter), "eliminado")
    ordering = ("fecha_registro",)
    date_hierarchy = "fecha_registro"
    search_fields = (
        "registro_invima",
        "nombre",
    )
    list_per_page = 30
    fields = (
        "tipo",
        "nombre",
        "presentacion",
        "material",
        "registro_invima",
        "proveedor",
        "descripcion",
    )
    summernote_fields = ("descripcion",)
    inlines = (LoteInline,)
    actions = [
        "descargar_base_producto",
        "descargar_registros",
        "eliminar_seleccionados",
        "recuperar_seleccionados",
    ]

    def descargar_base_producto(self, request, queryset):
        output = BytesIO()
        workbook = Workbook(output)
        worksheet = workbook.add_worksheet("Artículo")
        bold = workbook.add_format({"bold": True})
        width = 20
        worksheet.set_column(0, 1, width)
        worksheet.set_column(1, 1, width)
        worksheet.set_column(2, 1, width)
        worksheet.set_column(3, 1, width)
        worksheet.set_column(4, 1, width)
        worksheet.set_column(5, 1, width)
        worksheet.write("A1", "nombre", bold),
        worksheet.write("B1", "material", bold)
        worksheet.write("C1", "proveedor", bold)
        worksheet.write("D1", "registro_invima", bold)
        worksheet.write("E1", "presentacion", bold)
        worksheet.write("F1", "tipo", bold)
        workbook.close()
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=BaseProducto.xlsx"
        return response

    descargar_base_producto.short_description = (
        "Descargar el archivo Base o plantilla."
    )

    def descargar_registros(self, request, queryset):
        lista = list(queryset)
        finalList = []
        finalList.append(
            [
                "Nombre",
                "Presentacion",
                "Proveedor",
                "Registro Invima",
                "Tipo",
                "Uds Disponibles",
            ]
        )
        for producto in lista:
            uno = [
                producto.nombre,
                producto.presentacion,
                producto.proveedor,
                producto.registro_invima,
                producto.tipo,
                producto.cantidad_unidades_disponibles,
            ]
            finalList.append(uno)
        # List of Lists
        data = finalList
        return pdfConfig(data, "Reporte artículos")

    descargar_registros.short_description = "Descargar registros en PDF"

    def eliminar_seleccionados(self, request, queryset):
        queryset.update(eliminado=False)
        queryset.update(fecha_eliminacion=datetime.now())

    eliminar_seleccionados.short_description = "Eliminar los seleccionados"

    def recuperar_seleccionados(self, request, queryset):
        queryset.update(eliminado=True)
        queryset.update(fecha_eliminacion=None)

    recuperar_seleccionados.short_description = "Recuperar los seleccionados"


class ScrapeStatusFilter(SimpleListFilter):
    title = "Semaforizacion"  # a label for our filter
    parameter_name = "Colorometria"  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("verde", "Verde: Más de 11 meses"),
            ("amarillo", "Amarillo: Entre 5 y 11 meses"),
            ("rojo", "Rojo: Menos de 5 meses"),
            ("negro", "Negro: Productos caducados"),
            ("sin caducar", "No caduca."),
        ]

    def queryset(self, request, queryset):
        color = self.value()
        if color == "verde":
            fechafinal = (
                timezone.now().date()
                + dateutil.relativedelta.relativedelta(months=11)
            )
            lotes = Lote.objects.filter(fecha_vencimiento__gte=fechafinal)
            return lotes
        elif color == "amarillo":
            fechafinal = (
                timezone.now().date()
                + dateutil.relativedelta.relativedelta(months=5)
            )
            fechaInicial = (
                timezone.now().date()
                + dateutil.relativedelta.relativedelta(months=11)
            )
            lotes = Lote.objects.filter(
                fecha_vencimiento__lt=fechaInicial,
                fecha_vencimiento__gte=fechafinal,
            )
            return lotes
        elif color == "rojo":
            fechaInicial = (
                timezone.now().date()
                + dateutil.relativedelta.relativedelta(months=5)
            )
            fechafinal = timezone.now().date()
            lotes = Lote.objects.filter(
                fecha_vencimiento__lt=fechaInicial,
                fecha_vencimiento__gte=fechafinal,
            )
            return lotes

        elif color == "negro":
            fechafinal = timezone.now().date()
            lotes = Lote.objects.filter(fecha_vencimiento__lt=fechafinal)
            return lotes

        elif color == "sin caducar":
            lotes = Lote.objects.filter(fecha_vencimiento__isnull=True)
            return lotes


class LoteAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    resource_class = LoteResource
    list_display = (
        "eliminado",
        "producto",
        "semaforizacion",
        "registro_invima",
        "cantidad_entrada",
        "fecha_ingreso",
        "fecha_vencimiento",
        "lote_del_producto",
        "unidades_restantes",
        "total_entradas",
        "total_salidas",
        "_meses_vencimiento",
        "activo",
    )
    raw_id_fields = ("producto",)
    list_filter = (
        "producto__tipo",
        ScrapeStatusFilter,
        "fecha_ingreso",
        "fecha_vencimiento",
        "eliminado",
    )
    ordering = ("fecha_vencimiento",)
    date_hierarchy = "fecha_ingreso"
    search_fields = ("lote_del_producto", "producto__registro_invima")
    summernote_fields = ("descripcion",)
    list_per_page = 30
    fields = (
        "producto",
        "cantidad_entrada",
        "fecha_ingreso",
        "fecha_vencimiento",
        "lote_del_producto",
        "descripcion",
    )
    actions = [
        "descargar_base_lote",
        "descargar_registros",
        "cambiar_estado",
        "eliminar_seleccionados",
        "recuperar_seleccionados",
    ]

    def descargar_base_lote(self, request, queryset):
        output = BytesIO()
        workbook = Workbook(output)
        worksheet = workbook.add_worksheet("Lote")
        bold = workbook.add_format({"bold": True})
        width = 20
        worksheet.set_column(0, 1, width)
        worksheet.set_column(1, 1, width)
        worksheet.set_column(2, 1, width)
        worksheet.set_column(3, 1, width)
        worksheet.set_column(4, 1, width)
        worksheet.write("A1", "producto", bold)
        worksheet.write("B1", "cantidad_entrada", bold)
        worksheet.write("C1", "fecha_ingreso", bold)
        worksheet.write("D1", "fecha_vencimiento", bold)
        worksheet.write("E1", "lote_del_producto", bold)
        workbook.close()
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=BaseLote.xlsx"
        return response

    descargar_base_lote.short_description = (
        "Descargar el archivo Base o plantilla."
    )

    def descargar_registros(self, request, queryset):
        lista = list(queryset)
        finalList = []
        finalList.append(
            [
                "Producto",
                "Proveedor",
                "Presentacion",
                "Registro Invima",
                "Fecha de caducidad",
                "Unidades",
                "Meses por vencer",
                "Estado",
            ]
        )
        for lote in lista:
            uno = [
                lote.producto.nombre,
                lote.producto.proveedor,
                lote.producto.presentacion,
                lote.producto.registro_invima,
                lote.fecha_vencimiento,
                lote.unidades_restantes,
                lote.meses_vencimiento,
                lote.estado,
            ]
            finalList.append(uno)
        # List of Lists
        data = finalList
        return pdfConfig(data, "Reporte Lotes")

    descargar_registros.short_description = "Descargar registros en pdf"

    def cambiar_estado(self, request, quetyset):
        quetyset.update(activo=False)

    cambiar_estado.short_description = "Desactivar lotes"
    descargar_registros.short_description = "Descargar registros en pdf"

    def eliminar_seleccionados(self, request, queryset):
        queryset.update(eliminado=False)
        queryset.update(fecha_eliminacion=datetime.now())

    eliminar_seleccionados.short_description = "Eliminar los seleccionados"

    def recuperar_seleccionados(self, request, queryset):
        queryset.update(eliminado=True)
        queryset.update(fecha_eliminacion=None)

    recuperar_seleccionados.short_description = "Recuperar los seleccionados"


class SalidaLoteAdmin(ImportExportModelAdmin):
    resource_class = LoteSalidaResource
    list_display = (
        "producto",
        "fecha_salida",
        "cantidad_salida",
        "descripcion",
    )
    list_filter = ("producto", "fecha_salida")
    ordering = ("fecha_salida",)
    date_hierarchy = "fecha_salida"
    search_fields = ("producto",)
    list_per_page = 30
    fields = ("cantidad_salida", "producto", "descripcion")
    raw_id_fields = ("producto",)

    actions = ["descargar_base_lote", "descargar_registros"]

    def descargar_registros(self, request, queryset):
        lista = list(queryset)
        finalList = []
        finalList.append(
            ["Producto", "Cantidad salida", "Fecha salida", "Descripcion"]
        )
        for salidaLote in lista:
            uno = [
                salidaLote.producto.producto.nombre
                + " - "
                + salidaLote.producto.producto.presentacion
                + " - "
                + salidaLote.producto.lote_del_producto,
                salidaLote.cantidad_salida,
                salidaLote.fecha_salida,
                salidaLote.descripcion,
            ]
            finalList.append(uno)
        # List of Lists
        data = finalList
        return pdfConfig(data, "Reporte Salida de productos.")


class EntradaLoteAdmin(ImportExportModelAdmin):
    list_display = (
        "producto",
        "fecha_entrada",
        "cantidad_entrante",
        "descripcion",
    )
    list_filter = ("fecha_entrada", "producto")
    ordering = ("fecha_entrada",)
    date_hierarchy = "fecha_entrada"
    search_fields = ("producto",)
    list_per_page = 30
    fields = ("cantidad_entrante", "producto", "descripcion")
    raw_id_fields = ("producto",)

    actions = ["descargar_base_lote", "descargar_registros"]

    def descargar_registros(self, request, queryset):
        lista = list(queryset)
        finalList = []
        finalList.append(
            ["Producto", "Cantidad entrada", "Fecha entrada", "Descripcion"]
        )
        for entradaLote in lista:
            uno = [
                entradaLote.producto.producto.nombre
                + " - "
                + entradaLote.producto.producto.presentacion
                + " - "
                + entradaLote.producto.lote_del_producto,
                entradaLote.cantidad_entrante,
                entradaLote.fecha_entrada,
                entradaLote.descripcion,
            ]
            finalList.append(uno)
        # List of Lists
        data = finalList
        return pdfConfig(data, "Reporte Entrada de Artículos..")

    descargar_registros.short_description = "Descargar registros en pdf"


def pdfConfig(data, nombre):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte.pdf"'

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    canv = Canvas(response, pagesize=letter)

    header = Paragraph(
        "<bold><font size=18>{}</font></bold>".format(nombre), style
    )
    t = Table(data)
    t.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    data_len = len(data)
    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey
        t.setStyle(
            TableStyle([("BACKGROUND", (0, each), (-1, each), bg_color)])
        )
    aW = 5404
    aH = 720
    w, h = header.wrap(aW, aH)
    header.drawOn(canv, 9, aH)
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(canv, 9, aH - h)
    canv.save()
    return response


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Lote, LoteAdmin)
admin.site.register(SalidaLote, SalidaLoteAdmin)
admin.site.register(EntradaLote, EntradaLoteAdmin)

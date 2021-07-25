from django.contrib import admin

# Register your models here.

from django_summernote.utils import get_attachment_model

"""
 """
admin.site.site_url = "/gestion"
admin.site.site_header = "CSU Inventario"
admin.site.site_title = "CSU Inventario"
admin.site.index_title = "CSU Inventario"


admin.site.unregister(get_attachment_model())

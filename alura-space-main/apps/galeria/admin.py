from django.contrib import admin
from apps.galeria.models import Fotografia


class ListarFotografias(admin.ModelAdmin):
    list_display = ("id", "ativo", "nome", "legenda")
    list_display_links = ("id", "nome")
    search_fields = ["nome"]
    list_filter = ("categoria",)
    list_editable = ("ativo",)
    list_per_page = 10

admin.site.register(Fotografia, ListarFotografias)

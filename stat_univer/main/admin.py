from django.contrib import admin
from .models import Institute, Departure, Employee, Conference, FAQ
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class ConferenceResource(resources.ModelResource):
    
    class Meta:
        model = Conference


class ConferenceAdmin(ImportExportActionModelAdmin):
    resource_class = ConferenceResource


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ShortName', 'IdDirector', 'IdDeputeScience')
    list_display_links = ('Name', 'ShortName')
    search_fields = ('Name',)


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Departure)
admin.site.register(Employee)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(FAQ)

admin.site.site_title = 'Админ-панель сайта отдела статистики ГУУ'
admin.site.site_header = 'Админ-панель сайта отдела статистики ГУУ'

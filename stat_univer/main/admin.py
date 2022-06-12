from django.contrib import admin
from .models import Institute, Departure, Employee, Conference, FAQ, VAK, Thesis


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ShortName', 'IdDirector', 'IdDeputeScience')
    list_display_links = ('Name', 'ShortName')
    search_fields = ('Name',)


class VAKAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Year')
    list_display_links = ('Name', 'Year')


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Departure)
admin.site.register(Employee)
admin.site.register(Conference)
admin.site.register(FAQ)
admin.site.register(VAK)
admin.site.register(Thesis)

admin.site.site_title = 'Админ-панель сайта отдела статистики ГУУ'
admin.site.site_header = 'Админ-панель сайта отдела статистики ГУУ'

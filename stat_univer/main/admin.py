from django.contrib import admin
from .models import Institute, Departure, Employee, Conference, FAQ, VAK, Thesis, Monograph


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ShortName', 'IdDirector', 'IdDeputeScience')
    list_display_links = ('Name', 'ShortName')
    search_fields = ('Name',)


class VAKAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'DateCreated')
    list_display_links = ('Name', )
    search_fields = ('Name', 'Author__username')
    

class ThesisAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'DateCreated')
    list_display_links = ('Name', )
    search_fields = ('Name', 'Author__username')
    
    
class MonographAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'DateCreated')
    list_display_links = ('Name', )
    search_fields = ('Name', 'Author__username')


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Departure)
admin.site.register(Employee)
admin.site.register(Conference)
admin.site.register(FAQ)
admin.site.register(VAK, VAKAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Monograph, MonographAdmin)

admin.site.site_title = 'Админ-панель сайта отдела статистики ГУУ'
admin.site.site_header = 'Админ-панель сайта отдела статистики ГУУ'

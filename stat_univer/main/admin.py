from django.contrib import admin
from django.db.models import Count, Q
from django.db.models.functions import Lower

from .models import Institute, Departure, Employee, Conference, FAQ, VAK, Thesis, Monograph, Plan, Income, RID


class DuplicatesFilter(admin.SimpleListFilter):
    title = "Дубликаты"
    parameter_name = 'duplicates'
    
    def lookups(self, request, model_admin):
        return [
            ("dubl", ("Дубликаты")),
            ("single", ("Без дубляжа")),
        ]

    def queryset(self, request, queryset):
        # Получение публикаций, которые имеют дубликаты
        # Приводим название публикации к нижнему регистру и присваеваем этому полю 'lower_name'
        # Группруем по новому полю 'lower_name'
        # Считаем количество публикаций и записываем количество в поле 'count'
        # Фильтруем записи, где 'count' больше 1 (есть дубликаты)
        # Получаем словарь с ключами lower_name и count
        duplicate_names = queryset.annotate(lower_name=Lower('Name')). \
            values('lower_name'). \
            annotate(count=Count('lower_name')). \
            filter(Q(count__gt=1))

        # Формируем список из названием статей, которые хранятся в словаре duplicate_names с ключем 'lower_name'
        list_duplicate = [dn['lower_name'] for dn in duplicate_names]

        if self.value() == 'dubl':
            # Формируем queryset из статей из списка дубляжей, предварительно приводя все названия публикаций к нижнему регистру
            return queryset.annotate(lower_name=Lower('Name')).filter(lower_name__in=list_duplicate)
        elif self.value() == 'single':
            return queryset.annotate(lower_name=Lower('Name')).exclude(lower_name__in=list_duplicate)
        else:
            return queryset


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ShortName', 'IdDirector', 'IdDeputeScience')
    list_display_links = ('Name', 'ShortName')
    search_fields = ('Name',)


class VAKAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'DateCreated', 'Accepted')
    list_display_links = ('Name', )
    list_filter = ('IdDeparture','Author', DuplicatesFilter)
    search_fields = ('Name', 'IdDeparture__Name', 'Author__username')
    

class ThesisAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'DateCreated', 'Accepted')
    list_display_links = ('Name', )
    list_filter = ('IdDeparture','Author', DuplicatesFilter)
    search_fields = ('Name', 'IdDeparture__Name', 'Author__username')
    
    
class MonographAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'DateCreated', 'Accepted')
    list_display_links = ('Name', )
    list_filter = ('IdDeparture','Author', DuplicatesFilter)
    search_fields = ('Name', 'IdDeparture__Name', 'Author__username')


class PlanAdmin(admin.ModelAdmin):
    list_display = ('Departure', 'Name', 'Year', 'Value')
    list_filter = ('Departure', 'Name', 'Year')
    search_fields = ('Departure__Name', 'Name')


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'Year', 'Points')
    list_filter = ('IdDeparture', 'Author', 'Year')
    search_fields = ('Name', 'IdDeparture__Name', )

    
class RIDAdmin(admin.ModelAdmin):
    list_display = ('Name', 'IdDeparture', 'Author', 'Year', 'Points')
    list_filter = ('IdDeparture', 'Author', 'Year')
    search_fields = ('Name', 'IdDeparture__Name', )


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Departure)
admin.site.register(Employee)
admin.site.register(Conference)
admin.site.register(FAQ)
admin.site.register(VAK, VAKAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Monograph, MonographAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(RID, RIDAdmin)

admin.site.site_title = 'Админ-панель сайта отдела статистики ГУУ'
admin.site.site_header = 'Админ-панель сайта отдела статистики ГУУ'

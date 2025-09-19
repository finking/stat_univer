from django.contrib import admin
from django.db.models import Count, Q
from django.db.models.functions import Lower
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import Institute, Departure, Employee, Conference, FAQ, VAK, Thesis, Monograph, Plan, Income, RID
from .utils import PARAMETERNAME


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
    list_display = ('Name', 'ShortName', 'Director', 'DeputeScience')
    list_display_links = ('Name', 'ShortName')
    search_fields = ('Name',)


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Country', 'City', 'Organizer', 'TimeCreate')
    search_fields = ('Name', 'Country', 'City', 'TimeCreate')
    list_filter = ('TimeCreate', 'Organizer', 'City')


class VAKAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Departure', 'Author', 'DateCreated', 'Accepted')
    list_display_links = ('Name', )
    list_filter = ('Departure', 'Accepted', DuplicatesFilter)
    search_fields = ('Name', 'Departure__Name', 'Author__username')
    

class ThesisAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Departure', 'Author', 'DateCreated', 'Accepted')
    list_display_links = ('Name', )
    list_filter = ('Departure', 'Accepted', DuplicatesFilter)
    search_fields = ('Name', 'Departure__Name', 'Author__username')
    
    
class MonographAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Departure', 'Author', 'DateCreated', 'Accepted')
    list_display_links = ('Name', )
    list_filter = ('Departure', 'Accepted', DuplicatesFilter)
    search_fields = ('Name', 'Departure__Name', 'Author__username')


class PlanAdmin(admin.ModelAdmin):
    list_display = ('Departure', 'Name', 'Year', 'Value')
    list_filter = ('Departure', 'Name', 'Year')
    search_fields = ('Departure__Name', 'Name')


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Departure', 'Author', 'Year', 'Points')
    list_filter = ('Departure', 'Author', 'Year')
    search_fields = ('Name', 'Departure__Name', )

    
class RIDAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Departure', 'Author', 'Year', 'Points')
    list_filter = ('Departure', 'Author', 'Year')
    search_fields = ('Name', 'Departure__Name', )


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Departure)
admin.site.register(Employee)
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(FAQ)
admin.site.register(VAK, VAKAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Monograph, MonographAdmin)
# admin.site.register(Plan, PlanAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(RID, RIDAdmin)

admin.site.site_title = 'Админ-панель сайта отдела НТИ ГУУ'
admin.site.site_header = 'Админ-панель сайта отдела НТИ ГУУ'


# Добавление экспорта-импорта из админ-панели с помощью библиотеки django-import-export
class PlanResource(resources.ModelResource):
    Departure = fields.Field(
        column_name='Departure',
        attribute='Departure',
        widget=ForeignKeyWidget(Departure, 'Name')
    )
    
    class Meta:
        model = Plan
        fields = ('Departure', 'Name', 'Year', 'Value')
        import_id_fields = ('Departure', 'Name', 'Year')
        skip_unchanged = True  # Пропускать неизмененные строки
    
    def before_import_row(self, row, **kwargs):
        # Проверка, что Name есть в PARAMETERNAME
        if row['Name'] not in [choice[0] for choice in PARAMETERNAME]:
            raise ValueError(f"Недопустимый параметр: {row['Name']}")


@admin.register(Plan)
class PlanAdmin(ImportExportModelAdmin):
    resource_classes = [PlanResource]


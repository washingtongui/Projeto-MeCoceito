from datetime import date

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils.timezone import now

from api.models import (
    BannerDestaque,
    CardNovidade,
    Category,
    CategorySection,
    FemininoProduct,
    LojaProduct,
    MasculinoProduct,
    NovidadeProduct,
    Product,
    SiteVisit,
    StoreShowcase,
)


class ProductInline(admin.TabularInline):
    model = Product
    fk_name = 'category'
    extra = 1
    fields = ('name', 'price', 'description', 'section', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_object = obj
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'section' and getattr(self, 'parent_object', None):
            kwargs['queryset'] = CategorySection.objects.filter(category=self.parent_object)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    inlines = [ProductInline]

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Produtos'


class SectionProductInline(admin.TabularInline):
    model = Product
    fk_name = 'section'
    extra = 1
    fields = ('name', 'price', 'description', 'button_label', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


class CategorySectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('category',)
    inlines = [SectionProductInline]


CATEGORY_ORIGEM_MAP = {
    'loja': 'LOJA',
    'novidades': 'NOVIDADES',
    'feminino': 'FEMININO',
    'masculino': 'MASCULINO',
}

CATEGORY_NAME_MAP = {
    'loja': 'Loja',
    'novidades': 'Novidades',
    'feminino': 'Feminino',
    'masculino': 'Masculino',
}


class BaseProductProxyAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'price', 'button_label', 'created_at')
    list_filter = ('section__category', 'section')
    search_fields = ('name',)
    fields = ('name', 'price', 'description', 'image_url', 'section')
    ordering = ('name',)
    category_slug = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.category_slug:
            return qs.filter(category__slug=self.category_slug)
        return qs

    def save_model(self, request, obj, form, change):
        if self.category_slug:
            if obj.section:
                obj.category = obj.section.category
            else:
                obj.category, _ = Category.objects.get_or_create(
                    slug=self.category_slug,
                    defaults={'name': CATEGORY_NAME_MAP.get(self.category_slug, self.category_slug.title())},
                )
            obj.origem_pagina = CATEGORY_ORIGEM_MAP.get(self.category_slug, obj.origem_pagina)
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'section' and self.category_slug:
            kwargs['queryset'] = CategorySection.objects.filter(category__slug=self.category_slug)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'category', 'origem_pagina', 'price')
    list_filter = ('origem_pagina', 'section__category')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    fields = (
        'section',
        'name',
        'price',
        'description',
        'image_url',
        'button_label',
        'category',
        'origem_pagina',
    )
    readonly_fields = ('category', 'origem_pagina')
    ordering = ('origem_pagina', 'name')

    def save_model(self, request, obj, form, change):
        if obj.section is not None:
            obj.category = obj.section.category
            obj.origem_pagina = obj.category.origem_pagina
        super().save_model(request, obj, form, change)


class StoreShowcaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'origem_pagina', 'button_label', 'active')
    list_filter = ('origem_pagina', 'active')
    fields = ('title', 'subtitle', 'image_url', 'button_label', 'origem_pagina', 'active')


class BannerDestaqueAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'origem_pagina')
    list_filter = ('origem_pagina',)
    fields = ('titulo', 'subtitulo', 'botao_texto', 'imagem_fundo', 'origem_pagina')


class CardNovidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'origem_pagina', 'preco')
    list_filter = ('origem_pagina',)
    search_fields = ('nome', 'categoria_tag')
    fields = ('nome', 'preco', 'categoria_tag', 'imagem', 'origem_pagina')


class LojaProductAdmin(BaseProductProxyAdmin):
    category_slug = 'loja'


class NovidadeProductAdmin(BaseProductProxyAdmin):
    category_slug = 'novidades'


class FemininoProductAdmin(BaseProductProxyAdmin):
    category_slug = 'feminino'


class MasculinoProductAdmin(BaseProductProxyAdmin):
    category_slug = 'masculino'


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'is_staff',
        'is_active',
        'date_joined',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('-date_joined',)


class CustomAdminSite(AdminSite):
    site_header = 'Me Conceito'
    site_title = 'Admin Me Conceito'
    index_title = 'Painel de Controle'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        User = get_user_model()
        today = now().date()
        month_start = today.replace(day=1)

        extra_context.update(
            {
                'total_users': User.objects.count(),
                'new_users_this_month': User.objects.filter(date_joined__date__gte=month_start).count(),
                'visits_this_month': SiteVisit.objects.filter(created_at__date__gte=month_start).count(),
                'total_visits': SiteVisit.objects.count(),
            }
        )
        return super().index(request, extra_context=extra_context)


custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(get_user_model(), CustomUserAdmin)
custom_admin_site.register(Group, GroupAdmin)
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(CategorySection, CategorySectionAdmin)
custom_admin_site.register(Product, ProductAdmin)
custom_admin_site.register(LojaProduct, LojaProductAdmin)
custom_admin_site.register(NovidadeProduct, NovidadeProductAdmin)
custom_admin_site.register(FemininoProduct, FemininoProductAdmin)
custom_admin_site.register(MasculinoProduct, MasculinoProductAdmin)
custom_admin_site.register(StoreShowcase, StoreShowcaseAdmin)
custom_admin_site.register(BannerDestaque, BannerDestaqueAdmin)
custom_admin_site.register(CardNovidade, CardNovidadeAdmin)
custom_admin_site.register(SiteVisit)

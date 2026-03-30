from django.contrib import admin
from .models import Category, CategorySection, Product, SiteVisit, StoreShowcase


class CategorySectionInline(admin.TabularInline):
    model = CategorySection
    extra = 1
    fields = ('name', 'description')


class ProductInline(admin.TabularInline):
    model = Product
    fk_name = 'section'
    extra = 1
    fields = ('name', 'price', 'description', 'image_url', 'button_label', 'category')
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CategorySectionInline]


@admin.register(CategorySection)
class CategorySectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'origem_pagina', 'price', 'button_label', 'category', 'created_at')
    list_filter = ('origem_pagina', 'category')
    search_fields = ('name',)
    fields = (
        'name',
        'price',
        'description',
        'image_url',
        'button_label',
        'origem_pagina',
        'category',
        'section',
    )


@admin.register(StoreShowcase)
class StoreShowcaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'origem_pagina', 'button_label', 'active')
    list_filter = ('origem_pagina', 'active')
    fields = ('title', 'subtitle', 'image_url', 'button_label', 'origem_pagina', 'active')

    def has_add_permission(self, request):
        return not StoreShowcase.objects.exists()


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('path', 'created_at')

from django.core.exceptions import ValidationError
from django.db import models

ORIGEM_PAGINA_CHOICES = [
    ('LOJA', 'LOJA'),
    ('NOVIDADES', 'NOVIDADES'),
    ('FEMININO', 'FEMININO'),
    ('MASCULINO', 'MASCULINO'),
]


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    hero_title = models.CharField(max_length=150, blank=True)
    hero_image_url = models.URLField(blank=True)
    origem_pagina = models.CharField(
        max_length=12,
        choices=ORIGEM_PAGINA_CHOICES,
        default='LOJA',
        verbose_name='Menu da Navbar',
    )

    class Meta:
        verbose_name = 'Página do Menu'
        verbose_name_plural = '1. Páginas do Menu'

    def __str__(self):
        return self.name


class CategorySection(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='sections',
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = '2. Subcategorias'
        ordering = ['order', 'name']
        unique_together = ('category', 'slug')

    def __str__(self):
        return f'{self.category.name} — {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nome da Peça')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Unitário')
    description = models.TextField(blank=True, verbose_name='Descrição')
    image_url = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Foto do Produto',
        help_text='Dica: Use fotos verticais com fundo neutro',
    )
    button_label = models.CharField(max_length=40, blank=True, default='ADD TO BAG', verbose_name='Texto do Botão')
    origem_pagina = models.CharField(
        max_length=12,
        choices=ORIGEM_PAGINA_CHOICES,
        default='LOJA',
        verbose_name='Origem da Página',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Categoria',
    )
    section = models.ForeignKey(
        CategorySection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Seção',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.section is None:
            raise ValidationError({'section': 'Este produto deve pertencer a uma subcategoria.'})
        if self.category and self.section and self.section.category != self.category:
            raise ValidationError({'category': 'A categoria deve corresponder à seção selecionada.'})

    def save(self, *args, **kwargs):
        if self.section is not None:
            self.category = self.section.category
        if self.category is not None:
            self.origem_pagina = self.category.origem_pagina
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cadastro de Produto'
        verbose_name_plural = '3. Cadastro de Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name


class LojaProduct(Product):
    class Meta:
        proxy = True
        verbose_name = 'Produto Loja'
        verbose_name_plural = 'Produtos Loja'


class NovidadeProduct(Product):
    class Meta:
        proxy = True
        verbose_name = 'Produto Novidades'
        verbose_name_plural = 'Produtos Novidades'


class FemininoProduct(Product):
    class Meta:
        proxy = True
        verbose_name = 'Produto Feminino'
        verbose_name_plural = 'Produtos Feminino'


class MasculinoProduct(Product):
    class Meta:
        proxy = True
        verbose_name = 'Produto Masculino'
        verbose_name_plural = 'Produtos Masculino'


class StoreShowcase(models.Model):
    title = models.CharField(max_length=140)
    subtitle = models.CharField(max_length=180, blank=True)
    image_url = models.URLField(blank=True)
    origem_pagina = models.CharField(
        max_length=12,
        choices=ORIGEM_PAGINA_CHOICES,
        default='LOJA',
        verbose_name='Origem da Página',
    )
    button_label = models.CharField(max_length=60, blank=True, default='SAIBA MAIS')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-active', '-created_at']
        verbose_name = 'Banner de Vitrine'
        verbose_name_plural = 'Banners de Vitrine'

    def __str__(self):
        return self.title


class BannerDestaque(models.Model):
    titulo = models.CharField(max_length=140)
    subtitulo = models.CharField(max_length=180, blank=True)
    botao_texto = models.CharField(max_length=60, blank=True)
    imagem_fundo = models.URLField(blank=True)
    origem_pagina = models.CharField(
        max_length=12,
        choices=ORIGEM_PAGINA_CHOICES,
        default='LOJA',
        verbose_name='Origem da Página',
    )

    class Meta:
        verbose_name = 'Banner de Destaque'
        verbose_name_plural = 'Banners de Destaque'

    def clean(self):
        from django.core.exceptions import ValidationError

        if BannerDestaque.objects.exclude(pk=self.pk).exists():
            raise ValidationError('Só pode existir um único Banner de Destaque.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo or 'Banner de Destaque'


class CardNovidade(models.Model):
    nome = models.CharField(max_length=120)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria_tag = models.CharField(max_length=80)
    imagem = models.ImageField(upload_to='cardnovidades/', blank=True, null=True)
    origem_pagina = models.CharField(
        max_length=12,
        choices=ORIGEM_PAGINA_CHOICES,
        default='LOJA',
        verbose_name='Origem da Página',
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Card de Novidade'
        verbose_name_plural = 'Cards de Novidades'

    def __str__(self):
        return self.nome


class SiteVisit(models.Model):
    path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Visit on {self.created_at:%Y-%m-%d %H:%M:%S}'

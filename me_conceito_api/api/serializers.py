from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    BannerDestaque,
    CardNovidade,
    Category,
    CategorySection,
    Product,
    SiteVisit,
    StoreShowcase,
)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    section = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'description',
            'image_url',
            'button_label',
            'origem_pagina',
            'category',
            'section',
        ]


class CategorySectionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = CategorySection
        fields = ['id', 'name', 'slug', 'description', 'order', 'products']


class CategorySerializer(serializers.ModelSerializer):
    sections = CategorySectionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'hero_title',
            'hero_image_url',
            'sections',
        ]


class StoreShowcaseSerializer(serializers.ModelSerializer):
    hero_title = serializers.CharField(source='title')
    hero_description = serializers.CharField(source='subtitle', allow_blank=True)
    hero_image_url = serializers.URLField(source='image_url', allow_blank=True)
    button_label = serializers.CharField(source='button_label', default='SAIBA MAIS', allow_blank=True)
    origem_pagina = serializers.CharField(source='origem_pagina', read_only=True)

    class Meta:
        model = StoreShowcase
        fields = [
            'id',
            'hero_title',
            'hero_description',
            'hero_image_url',
            'button_label',
            'origem_pagina',
            'active',
        ]


class SiteVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteVisit
        fields = ['id', 'path', 'created_at']
        read_only_fields = ['id', 'created_at']


class BannerDestaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerDestaque
        fields = ['id', 'titulo', 'subtitulo', 'botao_texto', 'imagem_fundo', 'origem_pagina']


class CardNovidadeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='nome')
    price = serializers.DecimalField(source='preco', max_digits=10, decimal_places=2)
    description = serializers.CharField(source='categoria_tag', allow_blank=True)
    image_url = serializers.URLField(source='imagem', allow_blank=True)

    class Meta:
        model = CardNovidade
        fields = ['id', 'name', 'price', 'description', 'image_url', 'origem_pagina']


class UserRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']

    def validate_email(self, value):
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Este e-mail já está em uso.')
        return value

    def create(self, validated_data):
        name = validated_data.get('name', '').strip()
        email = validated_data['email'].strip().lower()
        password = validated_data['password']
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )
        return user

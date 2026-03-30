from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BannerDestaque, CardNovidade, Category, Product, SiteVisit, StoreShowcase
from .serializers import (
    BannerDestaqueSerializer,
    CardNovidadeSerializer,
    CategorySerializer,
    ProductSerializer,
    SiteVisitSerializer,
    StoreShowcaseSerializer,
    UserRegistrationSerializer,
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')
        if not email or not password:
            return Response(
                {'detail': 'Email e senha são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_model = get_user_model()
        user = None
        if '@' in email:
            try:
                user = user_model.objects.get(email__iexact=email)
            except user_model.DoesNotExist:
                user = None
        else:
            try:
                user = user_model.objects.get(username=email)
            except user_model.DoesNotExist:
                user = None

        if user is None:
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=user.username, password=password)
        if user is None:
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class StoreShowcaseView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        origem_pagina = request.query_params.get('origem_pagina')
        showcase = None
        if origem_pagina:
            showcase = StoreShowcase.objects.filter(
                active=True,
                origem_pagina=origem_pagina,
            ).first()
        if showcase is None:
            showcase = StoreShowcase.objects.filter(active=True).first()
        if showcase is None:
            return Response(
                {
                    'hero_title': 'ME CONCEITO',
                    'hero_description': 'Moda premium feita para sua rotina.',
                    'hero_image_url': '',
                    'button_label': 'SAIBA MAIS',
                }
            )
        serializer = StoreShowcaseSerializer(showcase)
        return Response(serializer.data)


class BannerDestaqueView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        origem_pagina = request.query_params.get('origem_pagina')
        banner = None
        if origem_pagina:
            banner = BannerDestaque.objects.filter(origem_pagina=origem_pagina).first()
        if banner is None:
            banner = BannerDestaque.objects.first()
        if banner is None:
            return Response(
                {
                    'titulo': 'Coleção Novidades',
                    'subtitulo': 'Encontre os looks mais recentes',
                    'botao_texto': 'Ver novidades',
                    'imagem_fundo': '',
                }
            )
        serializer = BannerDestaqueSerializer(banner)
        return Response(serializer.data)


class CardNovidadeListView(generics.ListAPIView):
    serializer_class = CardNovidadeSerializer

    def get_queryset(self):
        queryset = CardNovidade.objects.all()
        origem_pagina = self.request.query_params.get('origem_pagina')
        if origem_pagina:
            queryset = queryset.filter(origem_pagina=origem_pagina)
        return queryset


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category')
        origem_pagina = self.request.query_params.get('origem_pagina')
        if origem_pagina:
            queryset = queryset.filter(origem_pagina=origem_pagina)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class SiteVisitCreateView(generics.CreateAPIView):
    queryset = SiteVisit.objects.all()
    serializer_class = SiteVisitSerializer

    def perform_create(self, serializer):
        path = self.request.data.get('path', '')
        serializer.save(path=path)

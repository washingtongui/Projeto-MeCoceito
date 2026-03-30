from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product, CardNovidade, Category


class ProductModelTest(TestCase):
    def test_product_str(self):
        category = Category.objects.create(name='Teste', slug='teste')
        product = Product.objects.create(name='Teste', price=9.90, category=category)
        self.assertEqual(str(product), 'Teste')


class CardNovidadeEndpointTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        CardNovidade.objects.create(
            nome='Bora ve',
            preco=99.90,
            categoria_tag='NOVIDADES',
            imagem='http://127.0.0.1:8000/media/bora-ve.jpg',
            origem_pagina='NOVIDADES',
        )

    def test_cardnovidade_endpoint_returns_card(self):
        response = self.client.get('/api/cardnovidade/?origem_pagina=NOVIDADES')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], 'Bora ve')
        self.assertEqual(data[0]['categoria_tag'], 'NOVIDADES')

    def test_cards_endpoint_returns_card(self):
        response = self.client.get('/api/cards/?origem_pagina=NOVIDADES')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], 'Bora ve')

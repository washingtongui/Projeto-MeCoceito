from django.urls import path
from .views import (
    BannerDestaqueView,
    CardNovidadeListView,
    CategoryListView,
    CategoryDetailView,
    ProductListCreateView,
    SiteVisitCreateView,
    StoreShowcaseView,
    RegisterView,
    LoginView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('cards/', CardNovidadeListView.as_view(), name='card-list'),
    path('cardnovidade/', CardNovidadeListView.as_view(), name='cardnovidade-list'),
    path('banner-destaque/', BannerDestaqueView.as_view(), name='banner-destaque'),
    path('store-showcase/', StoreShowcaseView.as_view(), name='store-showcase'),
    path('visits/', SiteVisitCreateView.as_view(), name='site-visit-create'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
]
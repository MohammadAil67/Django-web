from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product list (all products)
    path('', views.ProductListView.as_view(), name='list'),
    
    # Search (must come before detail to avoid conflicts)
    path('search/', views.ProductSearchView.as_view(), name='search'),
    
    # Category view
    path('category/<slug:category_slug>/', views.CategoryProductListView.as_view(), name='category'),
    
    # Product detail (must be last to avoid catching other URLs)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]
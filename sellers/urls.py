from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('onboarding/', views.SellerOnboardingView.as_view(), name='onboarding'),
    path('dashboard/', views.SellerDashboardView.as_view(), name='dashboard'),
    path('profile/', views.SellerProfileView.as_view(), name='profile'),
    path('products/', views.SellerProductListView.as_view(), name='products'),
    path('products/create/', views.SellerProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.SellerProductUpdateView.as_view(), name='product_edit'),
    path('kyc/', views.KYCUploadView.as_view(), name='kyc_upload'),
    path('store/<slug:slug>/', views.StoreDetailView.as_view(), name='store_detail'),
    path('follow/<int:seller_id>/', views.FollowStoreView.as_view(), name='follow_store'),
    path('unfollow/<int:seller_id>/', views.UnfollowStoreView.as_view(), name='unfollow_store'),
]
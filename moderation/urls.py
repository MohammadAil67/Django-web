from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    #path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('sellers/', views.SellerManagementView.as_view(), name='seller_management'),
    path('sellers/kyc/', views.KYCReviewView.as_view(), name='kyc_review'),
    path('products/', views.ProductModerationView.as_view(), name='product_moderation'),
    path('campaigns/', views.CampaignManagementView.as_view(), name='campaign_management'),
    path('content-flags/', views.ContentFlagView.as_view(), name='content_flags'),
    path('reports/', views.AdminReportsView.as_view(), name='reports'),
]
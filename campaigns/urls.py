from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.CampaignListView.as_view(), name='list'),
    path('<slug:slug>/', views.CampaignDetailView.as_view(), name='detail'),
    path('coupon/apply/', views.ApplyCouponView.as_view(), name='apply_coupon'),
]
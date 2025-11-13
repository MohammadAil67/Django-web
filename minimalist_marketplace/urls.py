from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Q, Count

# Import models
from products.models import Product, Category
from campaigns.models import Campaign
from sellers.models import SellerProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(TemplateView):
    """Custom home view with context data"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get active campaigns
        context['active_campaigns'] = Campaign.objects.filter(
            status='active',
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).prefetch_related('products')[:3]
        
        # Get featured products
        context['featured_products'] = Product.objects.filter(
            is_featured=True,
            status='published',
            is_active=True
        ).select_related('seller', 'category').prefetch_related('images')[:8]
        
        # Get categories
        context['categories'] = Category.objects.filter(
            is_active=True,
            parent=None
        ).annotate(
            product_count=Count('products', filter=Q(products__status='published'))
        )[:12]
        
        # Calculate statistics
        context['total_products'] = Product.objects.filter(
            status='published',
            is_active=True
        ).count()
        
        context['total_sellers'] = SellerProfile.objects.filter(
            is_active=True,
            verification_status='verified'
        ).count()
        
        context['total_buyers'] = User.objects.filter(
            is_active=True
        ).count()
        
        return context


urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('users/', include('users.urls')),
    
    # Home page - Using custom view with context
    path('', HomeView.as_view(), name='home'),
    
    # Authentication
    path('auth/', include('users.urls')),
    
    # Products
    path('products/', include('products.urls')),
    
    # Sellers
    path('sellers/', include('sellers.urls')),

    # Campaigns
    path('campaigns/', include('campaigns.urls')),
    
    # Admin dashboard
    #path('dashboard/', include('moderation.urls')),
    
    # Notifications
    path('notifications/', include('notifications.urls')),
    
    # Multi-language support
    path('i18n/', include('django.conf.urls.i18n')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
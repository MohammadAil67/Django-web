from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import Product, Category, ProductReview
from sellers.models import SellerProfile
from django.views.generic import TemplateView
from django.utils import timezone
from campaigns.models import Campaign
from django.contrib.auth import get_user_model


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.filter(
            status='published', 
            is_active=True
        ).select_related('seller', 'category').prefetch_related('images')
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'popular':
            queryset = queryset.order_by('-view_count', '-wishlist_count')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating', '-review_count')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.filter(is_active=True, parent=None),
        })
        
        # Add user's wishlist product IDs if authenticated
        if self.request.user.is_authenticated:
            from products.models import Wishlist
            context['user_wishlist_ids'] = list(
                Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            )
        else:
            context['user_wishlist_ids'] = []
        
        return context


class CategoryProductListView(ListView):
    model = Product
    template_name = 'products/category_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(
            category=self.category,
            status='published',
            is_active=True
        ).select_related('seller', 'category').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category': self.category,
            'subcategories': self.category.children.filter(is_active=True),
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(
            status='published',
            is_active=True
        ).select_related('seller', 'category').prefetch_related('images', 'reviews')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        context.update({
            'related_products': Product.objects.filter(
                category=product.category,
                status='published',
                is_active=True
            ).exclude(id=product.id)[:8],
            'seller_products': Product.objects.filter(
                seller=product.seller,
                status='published',
                is_active=True
            ).exclude(id=product.id)[:4],
            'reviews': product.reviews.filter(is_reported=False)[:10],
            'is_in_wishlist': False,
            'user_has_reviewed': False,
        })
        
        if self.request.user.is_authenticated:
            from products.models import Wishlist
            # Check if product is in wishlist
            context['is_in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user,
                product=product
            ).exists()
            
            # Check if user has already reviewed this product
            context['user_has_reviewed'] = ProductReview.objects.filter(
                user=self.request.user,
                product=product
            ).exists()
        
        return context


class ProductSearchView(ListView):
    """
    Search view that handles keyword-based product searches.
    Accepts 'q' parameter for search query.
    """
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        
        # If no query, return empty queryset
        if not query:
            return Product.objects.none()
        
        # Base queryset with published products only
        queryset = Product.objects.filter(
            status='published',
            is_active=True
        ).select_related('seller', 'category').prefetch_related('images')
        
        # Search across multiple fields
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__icontains=query) |
            Q(seller__store_name__icontains=query) |
            Q(sku__icontains=query)
        )
        
        # Apply additional filters if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        min_price = self.request.GET.get('min_price')
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        
        max_price = self.request.GET.get('max_price')
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass
        
        # Sorting
        sort = self.request.GET.get('sort', '')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating', '-review_count')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            # Default: sort by relevance (title matches first, then description)
            queryset = queryset.order_by(
                '-rating',  # Higher rated first
                '-view_count',  # More popular first
            )
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        
        context.update({
            'query': query,
            'categories': Category.objects.filter(is_active=True, parent=None),
        })
        
        # Add user's wishlist product IDs if authenticated
        if self.request.user.is_authenticated:
            from products.models import Wishlist
            context['user_wishlist_ids'] = list(
                Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            )
        else:
            context['user_wishlist_ids'] = []
        
        return context
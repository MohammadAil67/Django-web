from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F, Count
from .models import SellerProfile, KYCRequest, StoreFollow
from .forms import SellerProfileForm, KYCRequestForm
from products.models import Product

class SellerOnboardingView(LoginRequiredMixin, TemplateView):
    template_name = 'sellers/onboarding.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_seller:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_profile = self.request.user.seller_profile
        
        context.update({
            'seller_profile': seller_profile,
            'kyc_completed': KYCRequest.objects.filter(seller=seller_profile).exists(),
            'products_count': Product.objects.filter(seller=seller_profile).count(),
        })
        return context

class SellerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'sellers/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_seller:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_profile = self.request.user.seller_profile
        
        # Get recent products with images prefetched
        recent_products = Product.objects.filter(
            seller=seller_profile
        ).select_related('category').prefetch_related('images').order_by('-created_at')[:10]
        
        # Get low stock products with images prefetched
        low_stock_products = Product.objects.filter(
            seller=seller_profile,
            stock_quantity__lte=F('min_stock_level'),
            track_inventory=True
        ).select_related('category').prefetch_related('images')[:10]
        
        context.update({
            'seller_profile': seller_profile,
            'recent_products': recent_products,
            'low_stock_products': low_stock_products,
            'total_products': Product.objects.filter(seller=seller_profile).count(),
            'published_products': Product.objects.filter(
                seller=seller_profile, 
                status='published'
            ).count(),
        })
        return context

class SellerProfileView(LoginRequiredMixin, DetailView):
    model = SellerProfile
    template_name = 'sellers/profile.html'
    context_object_name = 'seller_profile'
    
    def get_object(self, queryset=None):
        return self.request.user.seller_profile

class SellerProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SellerProfile
    form_class = SellerProfileForm
    template_name = 'sellers/profile_edit.html'
    success_url = reverse_lazy('sellers:profile')
    success_message = _('Store profile updated successfully!')
    
    def get_object(self, queryset=None):
        return self.request.user.seller_profile

class SellerProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'sellers/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user.seller_profile
        ).select_related('category').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_profile = self.request.user.seller_profile
        
        context.update({
            'total_products': Product.objects.filter(seller=seller_profile).count(),
            'published_products': Product.objects.filter(
                seller=seller_profile, 
                status='published'
            ).count(),
            'draft_products': Product.objects.filter(
                seller=seller_profile, 
                status='draft'
            ).count(),
            'out_of_stock_products': Product.objects.filter(
                seller=seller_profile, 
                status='published',
                stock_quantity=0
            ).count(),
        })
        return context

class SellerProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'sellers/product_form.html'
    success_message = _('Product created successfully!')
    
    def get_form_class(self):
        from products.forms import ProductForm
        return ProductForm
    
    def form_valid(self, form):
        form.instance.seller = self.request.user.seller_profile
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('sellers:product_edit', kwargs={'pk': self.object.pk})

class SellerProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'sellers/product_form.html'
    success_message = _('Product updated successfully!')
    
    def get_form_class(self):
        from products.forms import ProductForm
        return ProductForm
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user.seller_profile)
    
    def get_success_url(self):
        return reverse_lazy('sellers:product_edit', kwargs={'pk': self.object.pk})

class KYCUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = KYCRequest
    form_class = KYCRequestForm
    template_name = 'sellers/kyc_upload.html'
    success_url = reverse_lazy('sellers:dashboard')
    success_message = _('KYC documents submitted successfully! We will review them within 24-48 hours.')
    
    def form_valid(self, form):
        form.instance.seller = self.request.user.seller_profile
        return super().form_valid(form)

class StoreListView(ListView):
    model = SellerProfile
    template_name = 'sellers/store_list.html'
    context_object_name = 'stores'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        # Store the 'featured' flag from URL kwargs
        self.is_featured = kwargs.pop('featured', False) or request.path.endswith('/featured/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = SellerProfile.objects.filter(
            is_active=True,
            verification_status=SellerProfile.VerificationStatus.VERIFIED
        ).select_related('user').annotate(
            published_products_count=Count(
                'products',
                filter=Q(products__status='published', products__is_active=True)
            )
        )
        
        # Check if we're viewing featured stores
        if self.is_featured:
            queryset = queryset.filter(featured=True)
        
        # Order by featured first, then by rating and follower count
        queryset = queryset.order_by('-featured', '-rating', '-follower_count', 'store_name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_featured'] = self.is_featured
        context['total_stores'] = SellerProfile.objects.filter(
            is_active=True,
            verification_status=SellerProfile.VerificationStatus.VERIFIED
        ).count()
        context['featured_stores_count'] = SellerProfile.objects.filter(
            is_active=True,
            featured=True,
            verification_status=SellerProfile.VerificationStatus.VERIFIED
        ).count()
        return context

class StoreDetailView(DetailView):
    model = SellerProfile
    template_name = 'sellers/store_detail.html'
    context_object_name = 'store'
    slug_field = 'store_slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return SellerProfile.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = self.object
        
        # Get store products
        products = Product.objects.filter(
            seller=store,
            status='published',
            is_active=True
        ).select_related('category').prefetch_related('images')
        
        context.update({
            'products': products[:20],
            'total_products': products.count(),
            'is_following': False,
        })
        
        if self.request.user.is_authenticated:
            context['is_following'] = StoreFollow.objects.filter(
                user=self.request.user,
                seller=store
            ).exists()
        
        return context

class FollowStoreView(LoginRequiredMixin, View):
    def post(self, request, seller_id):
        seller = get_object_or_404(SellerProfile, id=seller_id, is_active=True)
        
        follow, created = StoreFollow.objects.get_or_create(
            user=request.user,
            seller=seller
        )
        
        if created:
            messages.success(request, _('You are now following this store!'))
        else:
            messages.info(request, _('You are already following this store.'))
        
        return redirect('sellers:store_detail', slug=seller.store_slug)

class UnfollowStoreView(LoginRequiredMixin, View):
    def post(self, request, seller_id):
        seller = get_object_or_404(SellerProfile, id=seller_id, is_active=True)
        
        follow = StoreFollow.objects.filter(
            user=request.user,
            seller=seller
        ).first()
        
        if follow:
            follow.delete()
            messages.success(request, _('You have unfollowed this store.'))
        else:
            messages.info(request, _('You were not following this store.'))
        
        return redirect('sellers:store_detail', slug=seller.store_slug)
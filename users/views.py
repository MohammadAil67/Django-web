from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, UpdateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import User
from .forms import (
    UserRegistrationForm, SellerRegistrationForm, 
    UserProfileForm, CustomAuthenticationForm
)
from products.models import Product, Wishlist
from sellers.models import SellerProfile, StoreFollow

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, _('Registration successful! Welcome to our marketplace.'))
        return response

class SellerRegisterView(CreateView):
    model = User
    form_class = SellerRegistrationForm
    template_name = 'users/register_seller.html'
    success_url = reverse_lazy('sellers:onboarding')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = User.Role.SELLER
        user.save()
        
        # Create seller profile
        seller_profile = SellerProfile.objects.create(
            user=user,
            store_name=form.cleaned_data['store_name'],
            description=form.cleaned_data['store_description']
        )
        
        login(self.request, user)
        messages.success(
            self.request, 
            _('Seller registration successful! Please complete your store setup.')
        )
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_seller:
            return reverse_lazy('sellers:dashboard')
        elif user.is_admin:
            return reverse_lazy('moderation:dashboard')
        else:
            return reverse_lazy('home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'wishlist_count': Wishlist.objects.filter(user=user).count(),
            'following_count': StoreFollow.objects.filter(user=user).count(),
        })
        
        # Check if user is seller AND has a seller profile
        if user.role == User.Role.SELLER:
            try:
                seller_profile = user.seller_profile
                context.update({
                    'seller_profile': seller_profile,
                    'product_count': Product.objects.filter(seller=seller_profile).count(),
                    'total_sales': seller_profile.total_sales,
                    'follower_count': seller_profile.follower_count,
                })
            except SellerProfile.DoesNotExist:
                # Seller doesn't have a profile yet
                pass
        
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully!'))
        return super().form_valid(form)

class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'users/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 20
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product', 'product__seller')

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, status='published')
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            messages.success(request, _('Product added to wishlist!'))
        else:
            messages.info(request, _('Product is already in your wishlist.'))
        
        return redirect('products:detail', slug=product.slug)

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        wishlist_item = get_object_or_404(
            Wishlist, 
            user=request.user, 
            product_id=product_id
        )
        wishlist_item.delete()
        messages.success(request, _('Product removed from wishlist!'))
        
        # Redirect back to the page they came from
        return redirect(request.META.get('HTTP_REFERER', 'users:wishlist'))
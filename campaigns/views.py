from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from .models import Campaign, Coupon

class CampaignListView(ListView):
    model = Campaign
    template_name = 'campaigns/list.html'
    context_object_name = 'campaigns'
    paginate_by = 12
    
    def get_queryset(self):
        now = timezone.now()
        return Campaign.objects.filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now,
            show_on_homepage=True
        ).order_by('-is_featured', 'sort_order', '-start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Get featured campaigns
        context['featured_campaigns'] = Campaign.objects.filter(
            status='active',
            is_featured=True,
            start_date__lte=now,
            end_date__gte=now
        )[:3]
        
        # Get campaigns ending soon
        context['ending_soon'] = Campaign.objects.filter(
            status='active',
            end_date__gte=now,
            end_date__lte=now + timezone.timedelta(days=3)
        )[:6]
        
        return context

class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'campaigns/detail.html'
    context_object_name = 'campaign'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        now = timezone.now()
        return Campaign.objects.filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now
        ).prefetch_related('eligible_sellers', 'eligible_categories','products')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.object
        
        # Get products in this campaign
        from products.models import Product
        products = Product.objects.filter(
            seller__in=campaign.eligible_sellers.all(),
            status='published',
            is_active=True
        )
        
        if campaign.eligible_categories.exists():
            products = products.filter(category__in=campaign.eligible_categories.all())
        
        context.update({
            'products': products[:20],
            'total_products': products.count(),
        })
        
        return context

class ApplyCouponView(LoginRequiredMixin, View):
    def post(self, request):
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        
        if not coupon_code:
            messages.error(request, _('Please enter a coupon code.'))
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        try:
            coupon = Coupon.objects.get(
                code=coupon_code,
                status='approved',
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            
            # Check usage limits
            if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
                messages.error(request, _('This coupon has reached its usage limit.'))
                return redirect(request.META.get('HTTP_REFERER', 'home'))
            
            # Check if coupon is for specific seller
            if coupon.seller and coupon.seller != request.user.seller_profile:
                messages.error(request, _('This coupon is not valid for your store.'))
                return redirect(request.META.get('HTTP_REFERER', 'home'))
            
            # Store coupon in session
            request.session['applied_coupon'] = {
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value),
                'max_discount': float(coupon.maximum_discount_amount) if coupon.maximum_discount_amount else None,
            }
            
            messages.success(request, _('Coupon applied successfully!'))
            
        except Coupon.DoesNotExist:
            messages.error(request, _('Invalid coupon code.'))
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))

class RemoveCouponView(LoginRequiredMixin, View):
    def post(self, request):
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
            messages.success(request, _('Coupon removed.'))
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))
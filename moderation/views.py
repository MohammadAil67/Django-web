from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Count, Sum
from django.urls import reverse_lazy
from django.utils import timezone
from .models import ModerationAction, ContentFlag, AutoModerationRule, AccountHealthScore
from sellers.models import SellerProfile, KYCRequest
from products.models import Product
from campaigns.models import Campaign, Coupon, Ad

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'moderation/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context.update({
            'total_sellers': SellerProfile.objects.count(),
            'pending_sellers': SellerProfile.objects.filter(
                verification_status='pending'
            ).count(),
            'total_products': Product.objects.count(),
            'pending_products': Product.objects.filter(
                status='draft'
            ).count(),
            'pending_kyc': KYCRequest.objects.filter(
                status='submitted'
            ).count(),
            'pending_content_flags': ContentFlag.objects.filter(
                status='pending'
            ).count(),
            'active_campaigns': Campaign.objects.filter(
                status='active'
            ).count(),
            'recent_actions': ModerationAction.objects.select_related(
                'moderator', 'content_type'
            )[:10],
        })
        
        return context

class SellerManagementView(AdminRequiredMixin, ListView):
    model = SellerProfile
    template_name = 'moderation/seller_management.html'
    context_object_name = 'sellers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = SellerProfile.objects.select_related('user').all()
        
        # Filters
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(verification_status=status)
        
        tier = self.request.GET.get('tier')
        if tier:
            queryset = queryset.filter(tier=tier)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(store_name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'status_choices': SellerProfile.VerificationStatus.choices,
            'tier_choices': SellerProfile.SellerTier.choices,
        })
        return context

class KYCReviewView(AdminRequiredMixin, ListView):
    model = KYCRequest
    template_name = 'moderation/kyc_review.html'
    context_object_name = 'kyc_requests'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = KYCRequest.objects.select_related(
            'seller', 'seller__user'
        ).all()
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        document_type = self.request.GET.get('document_type')
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'status_choices': KYCRequest.Status.choices,
            'document_type_choices': KYCRequest.DocumentType.choices,
        })
        return context

class ProductModerationView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'moderation/product_moderation.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.select_related(
            'seller', 'category'
        ).prefetch_related('images').all()
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        seller = self.request.GET.get('seller')
        if seller:
            queryset = queryset.filter(seller__id=seller)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(seller__store_name__icontains=search)
            )
        
        return queryset.order_by('-created_at')

class CampaignManagementView(AdminRequiredMixin, ListView):
    model = Campaign
    template_name = 'moderation/campaign_management.html'
    context_object_name = 'campaigns'
    paginate_by = 20
    
    def get_queryset(self):
        return Campaign.objects.select_related().all().order_by('-created_at')

class ContentFlagView(AdminRequiredMixin, ListView):
    model = ContentFlag
    template_name = 'moderation/content_flags.html'
    context_object_name = 'content_flags'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ContentFlag.objects.select_related(
            'reporter', 'content_type'
        ).all()
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        flag_type = self.request.GET.get('flag_type')
        if flag_type:
            queryset = queryset.filter(flag_type=flag_type)
        
        return queryset.order_by('-priority_score', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'status_choices': ContentFlag.Status.choices,
            'flag_type_choices': ContentFlag.FlagType.choices,
        })
        return context

class AdminReportsView(AdminRequiredMixin, TemplateView):
    template_name = 'moderation/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Seller statistics
        context['seller_stats'] = {
            'total': SellerProfile.objects.count(),
            'verified': SellerProfile.objects.filter(verification_status='verified').count(),
            'pending': SellerProfile.objects.filter(verification_status='pending').count(),
            'suspended': SellerProfile.objects.filter(verification_status='suspended').count(),
            'by_tier': dict(SellerProfile.objects.values_list('tier').annotate(count=Count('tier'))),
        }
        
        # Product statistics
        context['product_stats'] = {
            'total': Product.objects.count(),
            'published': Product.objects.filter(status='published').count(),
            'draft': Product.objects.filter(status='draft').count(),
            'out_of_stock': Product.objects.filter(stock_quantity=0).count(),
        }
        
        # Campaign statistics
        context['campaign_stats'] = {
            'total': Campaign.objects.count(),
            'active': Campaign.objects.filter(status='active').count(),
            'total_revenue': Campaign.objects.aggregate(total=Sum('revenue'))['total'] or 0,
        }
        
        # Moderation statistics
        context['moderation_stats'] = {
            'total_actions': ModerationAction.objects.count(),
            'this_month': ModerationAction.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).count(),
            'automated_actions': ModerationAction.objects.filter(is_automated=True).count(),
        }
        
        return context

class ApproveSellerView(AdminRequiredMixin, View):
    def post(self, request, seller_id):
        seller = get_object_or_404(SellerProfile, id=seller_id)
        
        seller.verification_status = 'verified'
        seller.is_active = True
        seller.verified_by = request.user
        seller.verification_date = timezone.now()
        seller.save()
        
        # Create moderation action
        ModerationAction.objects.create(
            action_type='approve_seller',
            moderator=request.user,
            content_object=seller,
            reason='Seller approved after review'
        )
        
        messages.success(request, _('Seller approved successfully!'))
        return redirect('moderation:seller_management')

class SuspendSellerView(AdminRequiredMixin, View):
    def post(self, request, seller_id):
        seller = get_object_or_404(SellerProfile, id=seller_id)
        reason = request.POST.get('reason', '')
        
        seller.verification_status = 'suspended'
        seller.is_active = False
        seller.save()
        
        # Create moderation action
        ModerationAction.objects.create(
            action_type='suspend_seller',
            moderator=request.user,
            content_object=seller,
            reason=reason
        )
        
        messages.success(request, _('Seller suspended successfully!'))
        return redirect('moderation:seller_management')

class ApproveKYCView(AdminRequiredMixin, View):
    def post(self, request, kyc_id):
        kyc = get_object_or_404(KYCRequest, id=kyc_id)
        
        kyc.status = 'approved'
        kyc.reviewer = request.user
        kyc.reviewed_at = timezone.now()
        kyc.save()
        
        # Update seller verification status if all KYCs are approved
        seller = kyc.seller
        pending_kyc = KYCRequest.objects.filter(
            seller=seller,
            status__in=['submitted', 'under_review']
        ).exists()
        
        if not pending_kyc:
            seller.verification_status = 'verified'
            seller.is_active = True
            seller.verified_by = request.user
            seller.verification_date = timezone.now()
            seller.save()
        
        messages.success(request, _('KYC document approved successfully!'))
        return redirect('moderation:kyc_review')

class RejectKYCView(AdminRequiredMixin, View):
    def post(self, request, kyc_id):
        kyc = get_object_or_404(KYCRequest, id=kyc_id)
        reason = request.POST.get('reason', '')
        
        kyc.status = 'rejected'
        kyc.reviewer = request.user
        kyc.review_notes = reason
        kyc.reviewed_at = timezone.now()
        kyc.save()
        
        messages.success(request, _('KYC document rejected.'))
        return redirect('moderation:kyc_review')

class ResolveContentFlagView(AdminRequiredMixin, View):
    def post(self, request, flag_id):
        flag = get_object_or_404(ContentFlag, id=flag_id)
        action = request.POST.get('action', 'dismiss')
        notes = request.POST.get('notes', '')
        
        if action == 'resolve':
            flag.status = 'resolved'
        else:
            flag.status = 'dismissed'
        
        flag.reviewed_by = request.user
        flag.review_notes = notes
        flag.reviewed_at = timezone.now()
        flag.save()
        
        messages.success(request, _('Content flag resolved successfully!'))
        return redirect('moderation:content_flags')
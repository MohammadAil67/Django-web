from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import SellerProfile, KYCRequest, StoreFollow

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'store_name', 'user', 'verification_status', 'tier',
        'follower_count', 'rating', 'is_active', 'featured'
    ]
    list_filter = [
        'verification_status', 'tier', 'is_active', 'featured',
        'supports_international_shipping', 'created_at'
    ]
    search_fields = ['store_name', 'user__username', 'user__email', 'business_registration_number']
    readonly_fields = ['created_at', 'updated_at', 'follower_count', 'total_sales', 'total_orders']
    
    fieldsets = (
        (_('Store Information'), {
            'fields': (
                'user', 'store_name', 'store_slug', 'description',
                'logo', 'banner_image', 'is_active', 'featured'
            )
        }),
        (_('Business Information'), {
            'fields': (
                'business_type', 'business_registration_number', 'tax_id',
                'business_phone', 'business_email', 'business_address'
            )
        }),
        (_('Verification & Tier'), {
            'fields': (
                'verification_status', 'kyc_data', 'verification_date', 'verified_by',
                'tier', 'payout_info'
            )
        }),
        (_('Performance Metrics'), {
            'fields': (
                'follower_count', 'total_sales', 'total_orders', 'rating', 'review_count',
                'account_health_score'
            )
        }),
        (_('Policies & Settings'), {
            'fields': (
                'supports_international_shipping', 'return_policy', 'shipping_policy',
                'meta_title', 'meta_description', 'keywords'
            )
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_seller', 'suspend_seller', 'feature_seller', 'unfeature_seller']
    
    def approve_seller(self, request, queryset):
        updated = queryset.update(verification_status='verified', is_active=True)
        self.message_user(request, _(
            f'{updated} seller(s) have been approved and activated.'
        ))
    approve_seller.short_description = _('Approve selected sellers')
    
    def suspend_seller(self, request, queryset):
        updated = queryset.update(verification_status='suspended', is_active=False)
        self.message_user(request, _(
            f'{updated} seller(s) have been suspended.'
        ))
    suspend_seller.short_description = _('Suspend selected sellers')
    
    def feature_seller(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, _(
            f'{updated} seller(s) have been featured.'
        ))
    feature_seller.short_description = _('Feature selected sellers')
    
    def unfeature_seller(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, _(
            f'{updated} seller(s) have been unfeatured.'
        ))
    unfeature_seller.short_description = _('Unfeature selected sellers')

@admin.register(KYCRequest)
class KYCRequestAdmin(admin.ModelAdmin):
    list_display = [
        'seller', 'document_type', 'status', 'reviewer', 'created_at'
    ]
    list_filter = ['status', 'document_type', 'created_at', 'reviewed_at']
    search_fields = ['seller__store_name', 'seller__user__username']
    readonly_fields = ['created_at', 'updated_at', 'activity_log']
    
    fieldsets = (
        (_('KYC Details'), {
            'fields': (
                'seller', 'document_type', 'document_file', 'document_metadata'
            )
        }),
        (_('Review'), {
            'fields': (
                'status', 'reviewer', 'review_notes', 'reviewed_at'
            )
        }),
        (_('Audit Trail'), {
            'fields': ('activity_log',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_kyc', 'reject_kyc', 'request_more_info']
    
    def approve_kyc(self, request, queryset):
        updated = queryset.update(status='approved', reviewer=request.user)
        self.message_user(request, _(
            f'{updated} KYC request(s) have been approved.'
        ))
    approve_kyc.short_description = _('Approve selected KYC requests')
    
    def reject_kyc(self, request, queryset):
        updated = queryset.update(status='rejected', reviewer=request.user)
        self.message_user(request, _(
            f'{updated} KYC request(s) have been rejected.'
        ))
    reject_kyc.short_description = _('Reject selected KYC requests')
    
    def request_more_info(self, request, queryset):
        updated = queryset.update(status='needs_more_info', reviewer=request.user)
        self.message_user(request, _(
            f'{updated} KYC request(s) need more information.'
        ))
    request_more_info.short_description = _('Request more information')

@admin.register(StoreFollow)
class StoreFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'seller', 'created_at']
    list_filter = ['created_at', 'notify_new_products', 'notify_price_drops']
    search_fields = ['user__username', 'seller__store_name']
    readonly_fields = ['created_at']
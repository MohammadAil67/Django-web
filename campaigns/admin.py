from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Campaign, Coupon, Ad

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'campaign_type', 'status', 'start_date', 'end_date',
        'is_featured', 'show_on_homepage', 'progress_percentage'
    ]
    list_filter = [
        'campaign_type', 'status', 'is_featured', 'show_on_homepage',
        'start_date', 'end_date'
    ]
    search_fields = ['title', 'description']
    readonly_fields = [
        'created_at', 'updated_at', 'published_at', 'progress_percentage',
        'impressions', 'clicks', 'conversions', 'revenue'
    ]
    filter_horizontal = ['eligible_sellers', 'eligible_categories']
    
    fieldsets = (
        (_('Campaign Information'), {
            'fields': (
                'title', 'slug', 'description', 'campaign_type', 'status'
            )
        }),
        (_('Timing'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Visual Assets'), {
            'fields': ('banner_image', 'mobile_banner_image')
        }),
        (_('Discount Rules'), {
            'fields': (
                'discount_percentage', 'minimum_order_value', 'max_discount_amount'
            )
        }),
        (_('Eligibility'), {
            'fields': ('eligible_sellers', 'eligible_categories', 'rules')
        }),
        (_('Display Settings'), {
            'fields': (
                'is_featured', 'show_on_homepage', 'show_in_category', 'sort_order'
            )
        }),
        (_('Performance Metrics'), {
            'fields': (
                'impressions', 'clicks', 'conversions', 'revenue', 'progress_percentage'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_campaign', 'pause_campaign', 'feature_campaign']
    
    def activate_campaign(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, _(
            f'{updated} campaign(s) have been activated.'
        ))
    activate_campaign.short_description = _('Activate selected campaigns')
    
    def pause_campaign(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, _(
            f'{updated} campaign(s) have been paused.'
        ))
    pause_campaign.short_description = _('Pause selected campaigns')
    
    def feature_campaign(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, _(
            f'{updated} campaign(s) have been featured.'
        ))
    feature_campaign.short_description = _('Feature selected campaigns')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_type', 'discount_value', 'status',
        'valid_from', 'valid_to', 'times_used', 'seller'
    ]
    list_filter = [
        'discount_type', 'status', 'valid_from', 'valid_to', 'seller__tier'
    ]
    search_fields = ['code', 'description', 'seller__store_name']
    readonly_fields = [
        'created_at', 'updated_at', 'approved_at', 'times_used', 'total_discount_given'
    ]
    
    fieldsets = (
        (_('Coupon Details'), {
            'fields': ('code', 'description', 'discount_type', 'discount_value')
        }),
        (_('Limits & Restrictions'), {
            'fields': (
                'minimum_order_amount', 'maximum_discount_amount',
                'usage_limit', 'usage_per_customer', 'restrictions'
            )
        }),
        (_('Validity'), {
            'fields': ('valid_from', 'valid_to')
        }),
        (_('Ownership'), {
            'fields': ('seller',)
        }),
        (_('Approval'), {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        (_('Usage Statistics'), {
            'fields': ('times_used', 'total_discount_given'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_coupon', 'reject_coupon', 'deactivate_coupon']
    
    def approve_coupon(self, request, queryset):
        updated = queryset.update(status='approved', approved_by=request.user)
        self.message_user(request, _(
            f'{updated} coupon(s) have been approved.'
        ))
    approve_coupon.short_description = _('Approve selected coupons')
    
    def reject_coupon(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, _(
            f'{updated} coupon(s) have been rejected.'
        ))
    reject_coupon.short_description = _('Reject selected coupons')
    
    def deactivate_coupon(self, request, queryset):
        updated = queryset.update(status='expired')
        self.message_user(request, _(
            f'{updated} coupon(s) have been deactivated.'
        ))
    deactivate_coupon.short_description = _('Deactivate selected coupons')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'ad_type', 'placement', 'status', 'start_date', 'end_date',
        'seller', 'ctr', 'conversion_rate'
    ]
    list_filter = [
        'ad_type', 'placement', 'status', 'start_date', 'end_date', 'seller__tier'
    ]
    search_fields = ['title', 'seller__store_name', 'product__title']
    readonly_fields = [
        'created_at', 'updated_at', 'approved_at', 'impressions', 'clicks',
        'conversions', 'spend', 'ctr', 'conversion_rate'
    ]
    
    fieldsets = (
        (_('Ad Information'), {
            'fields': (
                'title', 'ad_type', 'content', 'target_url'
            )
        }),
        (_('Visual Assets'), {
            'fields': ('image', 'mobile_image')
        }),
        (_('Placement & Targeting'), {
            'fields': (
                'placement', 'seller', 'product', 'category'
            )
        }),
        (_('Scheduling'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Budget & Pricing'), {
            'fields': (
                'budget', 'cost_per_click', 'cost_per_impression'
            )
        }),
        (_('Approval'), {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        (_('Performance Metrics'), {
            'fields': (
                'impressions', 'clicks', 'conversions', 'spend', 'ctr', 'conversion_rate'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_ad', 'reject_ad', 'pause_ad']
    
    def approve_ad(self, request, queryset):
        updated = queryset.update(status='active', approved_by=request.user)
        self.message_user(request, _(
            f'{updated} ad(s) have been approved.'
        ))
    approve_ad.short_description = _('Approve selected ads')
    
    def reject_ad(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, _(
            f'{updated} ad(s) have been rejected.'
        ))
    reject_ad.short_description = _('Reject selected ads')
    
    def pause_ad(self, request, queryset):
        updated = queryset.update(status='paused')
        self.message_user(request, _(
            f'{updated} ad(s) have been paused.'
        ))
    pause_ad.short_description = _('Pause selected ads')
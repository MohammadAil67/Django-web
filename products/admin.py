from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, ProductImage, Wishlist, ProductReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'sort_order', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Category Information'), {
            'fields': ('name', 'slug', 'description', 'parent', 'image')
        }),
        (_('Display Settings'), {
            'fields': ('is_active', 'sort_order')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['thumbnail_preview']
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url
            )
        return "No Image"
    thumbnail_preview.short_description = _('Preview')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'seller', 'category', 'price', 'stock_quantity',
        'status', 'is_featured', 'rating', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'condition', 'category', 'seller__tier',
        'is_active', 'created_at'
    ]
    search_fields = ['title', 'description', 'sku', 'seller__store_name']
    list_editable = ['status', 'is_featured', 'price']
    readonly_fields = [
        'created_at', 'updated_at', 'published_at', 'view_count',
        'wishlist_count', 'rating', 'review_count'
    ]
    inlines = [ProductImageInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'seller', 'category', 'title', 'slug', 'sku',
                'description', 'short_description'
            )
        }),
        (_('Pricing & Inventory'), {
            'fields': (
                'price', 'old_price', 'cost_price', 'stock_quantity',
                'min_stock_level', 'track_inventory'
            )
        }),
        (_('Product Details'), {
            'fields': (
                'condition', 'brand', 'model', 'weight', 'dimensions', 'attributes'
            )
        }),
        (_('Status & Visibility'), {
            'fields': (
                'status', 'is_active', 'is_featured', 'published_at'
            )
        }),
        (_('SEO & Marketing'), {
            'fields': (
                'meta_title', 'meta_description', 'keywords'
            )
        }),
        (_('Performance Metrics'), {
            'fields': (
                'view_count', 'wishlist_count', 'rating', 'review_count'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'publish_products', 'unpublish_products', 'feature_products',
        'unfeature_products', 'export_product_data'
    ]
    
    def publish_products(self, request, queryset):
        updated = queryset.update(status='published', is_active=True)
        self.message_user(request, _(
            f'{updated} product(s) have been published.'
        ))
    publish_products.short_description = _('Publish selected products')
    
    def unpublish_products(self, request, queryset):
        updated = queryset.update(status='draft', is_active=False)
        self.message_user(request, _(
            f'{updated} product(s) have been unpublished.'
        ))
    unpublish_products.short_description = _('Unpublish selected products')
    
    def feature_products(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, _(
            f'{updated} product(s) have been featured.'
        ))
    feature_products.short_description = _('Feature selected products')
    
    def unfeature_products(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, _(
            f'{updated} product(s) have been unfeatured.'
        ))
    unfeature_products.short_description = _('Unfeature selected products')
    
    def export_product_data(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Title', 'Seller', 'Category', 'Price', 'Stock', 'Status',
            'Rating', 'Views', 'Wishlist Count', 'Created At'
        ])
        
        for product in queryset:
            writer.writerow([
                product.id, product.title, product.seller.store_name,
                product.category.name, product.price, product.stock_quantity,
                product.status, product.rating, product.view_count,
                product.wishlist_count, product.created_at
            ])
        
        return response
    export_product_data.short_description = _('Export selected products')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'sort_order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__title', 'alt_text']
    readonly_fields = ['created_at', 'thumbnail_preview']
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.image.url
            )
        return "No Image"
    thumbnail_preview.short_description = _('Preview')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_price', 'added_at']
    list_filter = ['added_at', 'notify_price_drop', 'notify_restock']
    search_fields = ['user__username', 'product__title']
    readonly_fields = ['added_at']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_verified_purchase', 'is_reported', 'created_at']
    search_fields = ['product__title', 'user__username', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_as_verified', 'unmark_as_verified']
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified_purchase=True)
        self.message_user(request, _(
            f'{updated} review(s) have been marked as verified purchases.'
        ))
    mark_as_verified.short_description = _('Mark as verified purchase')
    
    def unmark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified_purchase=False)
        self.message_user(request, _(
            f'{updated} review(s) have been unmarked as verified purchases.'
        ))
    unmark_as_verified.short_description = _('Unmark as verified purchase')
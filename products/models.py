from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    """Product categories"""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Display
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    """Product model with comprehensive features"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        OUT_OF_STOCK = 'out_of_stock', _('Out of Stock')
        DISCONTINUED = 'discontinued', _('Discontinued')
        BLOCKED = 'blocked', _('Blocked')
    
    class Condition(models.TextChoices):
        NEW = 'new', _('New')
        USED = 'used', _('Used')
        REFURBISHED = 'refurbished', _('Refurbished')
    
    seller = models.ForeignKey('sellers.SellerProfile', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Basic Information
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    sku = models.CharField(max_length=100, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=1)
    track_inventory = models.BooleanField(default=True)
    
    # Product Details
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.NEW
    )
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)  # LxWxH format
    
    # Product Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Product Attributes (JSON for flexibility)
    attributes = models.JSONField(default=dict, blank=True)  # Color, size, material, etc.
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    
    # Statistics
    view_count = models.PositiveIntegerField(default=0)
    wishlist_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set published date when product is published
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = models.DateTimeField().value_from_object(self)
        
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0 if self.track_inventory else True
    
    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100, 0)
        return 0
    
    @property
    def main_image(self):
        """Get the main product image"""
        return self.images.filter(is_primary=True).first() or self.images.first()

class ProductImage(models.Model):
    """Product images with multiple sizes and optimization"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    
    # Image variants for different use cases
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    medium_size = models.ImageField(upload_to='products/medium/', blank=True, null=True)
    
    # Display settings
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'product_images'
        ordering = ['sort_order', 'created_at']
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
    
    def __str__(self):
        return f"Image for {self.product.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product).update(is_primary=False)
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    """User wishlist"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    
    # Notification preferences for this item
    notify_price_drop = models.BooleanField(default=True)
    notify_restock = models.BooleanField(default=True)
    
    # Metadata
    added_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wishlist'
        unique_together = ['user', 'product']
        verbose_name = _('Wishlist Item')
        verbose_name_plural = _('Wishlist Items')
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
    def save(self, *args, **kwargs):
        if not self.added_price:
            self.added_price = self.product.price
        super().save(*args, **kwargs)
        
        # Update product wishlist count
        self.product.wishlist_count = self.product.wishlisted_by.count()
        self.product.save(update_fields=['wishlist_count'])
    
    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        # Update product wishlist count
        product.wishlist_count = product.wishlisted_by.count()
        product.save(update_fields=['wishlist_count'])

class ProductReview(models.Model):
    """Product reviews and ratings"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255, blank=True)
    comment = models.TextField()
    
    # Review metadata
    is_verified_purchase = models.BooleanField(default=False)
    is_helpful = models.PositiveIntegerField(default=0)
    is_reported = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_reviews'
        unique_together = ['product', 'user']
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')
        indexes = [
            models.Index(fields=['product', 'rating']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"Review for {self.product.title} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update product rating
        self.update_product_rating()
    
    def update_product_rating(self):
        """Update product's average rating"""
        reviews = self.product.reviews.all()
        if reviews.exists():
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.product.rating = round(avg_rating, 2)
            self.product.review_count = reviews.count()
        else:
            self.product.rating = 0.00
            self.product.review_count = 0
        
        self.product.save(update_fields=['rating', 'review_count'])
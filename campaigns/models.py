from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = get_user_model()

class Campaign(models.Model):
    """Marketing campaigns and flash sales"""
    
    class CampaignType(models.TextChoices):
        FLASH_SALE = 'flash_sale', _('Flash Sale')
        SEASONAL = 'seasonal', _('Seasonal Campaign')
        CLEARANCE = 'clearance', _('Clearance Sale')
        NEW_ARRIVAL = 'new_arrival', _('New Arrival Showcase')
        CUSTOM = 'custom', _('Custom Campaign')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        SCHEDULED = 'scheduled', _('Scheduled')
        ACTIVE = 'active', _('Active')
        ENDED = 'ended', _('Ended')
        CANCELLED = 'cancelled', _('Cancelled')
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    # Campaign type and status
    campaign_type = models.CharField(
        max_length=20,
        choices=CampaignType.choices,
        default=CampaignType.CUSTOM
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Visual assets
    banner_image = models.ImageField(upload_to='campaigns/banners/', blank=True, null=True)
    mobile_banner_image = models.ImageField(upload_to='campaigns/mobile_banners/', blank=True, null=True)
    
    # Campaign rules and settings
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    minimum_order_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    max_discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Eligibility
    eligible_sellers = models.ManyToManyField('sellers.SellerProfile', blank=True, related_name='campaigns')
    eligible_categories = models.ManyToManyField('products.Category', blank=True, related_name='campaigns')
    
    # Campaign rules (JSON for flexibility)
    rules = models.JSONField(default=dict, blank=True)
    
    # Display settings
    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=True)
    show_in_category = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    # Performance tracking
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'campaigns'
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['campaign_type', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.status == self.Status.ACTIVE and 
                self.start_date <= now <= self.end_date)
    
    @property
    def progress_percentage(self):
        """Calculate campaign progress"""
        from django.utils import timezone
        now = timezone.now()
        
        if now < self.start_date:
            return 0
        elif now > self.end_date:
            return 100
        else:
            total_duration = (self.end_date - self.start_date).total_seconds()
            elapsed = (now - self.start_date).total_seconds()
            return min(100, int((elapsed / total_duration) * 100))

class Coupon(models.Model):
    """Discount coupons and promo codes"""
    
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', _('Percentage')
        FIXED_AMOUNT = 'fixed_amount', _('Fixed Amount')
        FREE_SHIPPING = 'free_shipping', _('Free Shipping')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PENDING_APPROVAL = 'pending_approval', _('Pending Approval')
        APPROVED = 'approved', _('Approved')
        ACTIVE = 'active', _('Active')
        EXPIRED = 'expired', _('Expired')
        CANCELLED = 'cancelled', _('Cancelled')
    
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    
    # Discount details
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE
    )
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Limits and restrictions
    minimum_order_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    maximum_discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    usage_per_customer = models.PositiveIntegerField(default=1)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    # Ownership
    seller = models.ForeignKey(
        'sellers.SellerProfile', 
        on_delete=models.CASCADE, 
        related_name='coupons',
        null=True, 
        blank=True
    )  # Null means marketplace-wide coupon
    
    # Approval
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_coupons'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    times_used = models.PositiveIntegerField(default=0)
    total_discount_given = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Restrictions (JSON for flexibility)
    restrictions = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coupons'
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status', 'valid_from', 'valid_to']),
            models.Index(fields=['seller', 'status']),
        ]
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.status == self.Status.ACTIVE and 
                self.valid_from <= now <= self.valid_to and
                (self.usage_limit is None or self.times_used < self.usage_limit))
    
    @property
    def discount_percentage(self):
        if self.discount_type == self.DiscountType.PERCENTAGE:
            return self.discount_value
        return 0

class Ad(models.Model):
    """Advertisements and sponsored content"""
    
    class AdType(models.TextChoices):
        BANNER = 'banner', _('Banner Ad')
        PRODUCT_SPONSORED = 'product_sponsored', _('Sponsored Product')
        STORE_SPONSORED = 'store_sponsored', _('Sponsored Store')
        CATEGORY_SPONSORED = 'category_sponsored', _('Sponsored Category')
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PENDING_APPROVAL = 'pending_approval', _('Pending Approval')
        APPROVED = 'approved', _('Approved')
        ACTIVE = 'active', _('Active')
        PAUSED = 'paused', _('Paused')
        EXPIRED = 'expired', _('Expired')
        CANCELLED = 'cancelled', _('Cancelled')
    
    class Placement(models.TextChoices):
        HOMEPAGE_HERO = 'homepage_hero', _('Homepage Hero')
        HOMEPAGE_SIDEBAR = 'homepage_sidebar', _('Homepage Sidebar')
        CATEGORY_TOP = 'category_top', _('Category Top')
        CATEGORY_SIDEBAR = 'category_sidebar', _('Category Sidebar')
        PRODUCT_DETAIL = 'product_detail', _('Product Detail')
        SEARCH_RESULTS = 'search_results', _('Search Results')
    
    title = models.CharField(max_length=255)
    ad_type = models.CharField(
        max_length=30,
        choices=AdType.choices,
        default=AdType.BANNER
    )
    
    # Content
    content = models.TextField()  # HTML content for banner ads
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    mobile_image = models.ImageField(upload_to='ads/mobile/', blank=True, null=True)
    
    # Links
    target_url = models.URLField()
    
    # Placement
    placement = models.CharField(
        max_length=30,
        choices=Placement.choices,
        default=Placement.HOMEPAGE_SIDEBAR
    )
    
    # Targeting
    seller = models.ForeignKey(
        'sellers.SellerProfile',
        on_delete=models.CASCADE,
        related_name='ads',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='ads',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE,
        related_name='ads',
        null=True,
        blank=True
    )
    
    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Pricing and budget
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_per_click = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_per_impression = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Status and approval
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_ads'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Performance metrics
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ads'
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')
        indexes = [
            models.Index(fields=['status', 'start_date', 'end_date']),
            models.Index(fields=['placement', 'status']),
            models.Index(fields=['seller', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.ad_type})"
    
    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return (self.status == self.Status.ACTIVE and 
                self.start_date <= now <= self.end_date)
    
    @property
    def ctr(self):
        """Click-through rate"""
        if self.impressions > 0:
            return round((self.clicks / self.impressions) * 100, 2)
        return 0.00
    
    @property
    def conversion_rate(self):
        """Conversion rate"""
        if self.clicks > 0:
            return round((self.conversions / self.clicks) * 100, 2)
        return 0.00
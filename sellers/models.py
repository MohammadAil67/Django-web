from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import json

User = get_user_model()

class SellerProfile(models.Model):
    """Seller profile with KYC and business information"""
    
    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', _('Pending Review')
        VERIFIED = 'verified', _('Verified')
        REJECTED = 'rejected', _('Rejected')
        SUSPENDED = 'suspended', _('Suspended')
    
    class SellerTier(models.TextChoices):
        BRONZE = 'bronze', _('Bronze')
        SILVER = 'silver', _('Silver')
        GOLD = 'gold', _('Gold')
        PLATINUM = 'platinum', _('Platinum')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    
    # Store Information
    store_name = models.CharField(max_length=255, null=True, blank=True)
    store_slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='store_logos/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='store_banners/', null=True, blank=True)
    
    # Business Information
    business_type = models.CharField(max_length=100, null=True, blank=True)
    business_registration_number = models.CharField(max_length=100, null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Contact Information
    business_phone = models.CharField(max_length=20, null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    
    # KYC Information
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        null=True,
        blank=True
    )
    kyc_data = models.JSONField(default=dict, null=True, blank=True)  # Store KYC documents metadata
    verification_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_sellers'
    )
    
    # Payout Information
    payout_info = models.JSONField(default=dict, null=True, blank=True)  # Store payment gateway info
    
    # Seller Tier and Performance
    tier = models.CharField(
        max_length=20,
        choices=SellerTier.choices,
        default=SellerTier.BRONZE
    )
    tier_updated_at = models.DateTimeField(auto_now_add=True)
    
    # Store Statistics
    follower_count = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_orders = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    
    # Account Health
    account_health_score = models.PositiveIntegerField(default=100)  # 0-100
    health_last_evaluated = models.DateTimeField(auto_now_add=True)
    
    # Store Settings
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    supports_international_shipping = models.BooleanField(default=False)
    return_policy = models.TextField(blank=True)
    shipping_policy = models.TextField(blank=True)
    
    # SEO and Marketing
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'seller_profiles'
        verbose_name = _('Seller Profile')
        verbose_name_plural = _('Seller Profiles')
        indexes = [
            models.Index(fields=['verification_status']),
            models.Index(fields=['tier']),
            models.Index(fields=['is_active', 'featured']),
        ]
    
    def __str__(self):
        return f"{self.store_name} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.store_slug:
            from django.utils.text import slugify
            self.store_slug = slugify(self.store_name)
        super().save(*args, **kwargs)

class KYCRequest(models.Model):
    """KYC verification request with documents"""
    
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', _('Submitted')
        UNDER_REVIEW = 'under_review', _('Under Review')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
        NEEDS_MORE_INFO = 'needs_more_info', _('Needs More Information')
    
    class DocumentType(models.TextChoices):
        IDENTITY = 'identity', _('Identity Document')
        BUSINESS_LICENSE = 'business_license', _('Business License')
        TAX_DOCUMENT = 'tax_document', _('Tax Document')
        ADDRESS_PROOF = 'address_proof', _('Address Proof')
        BANK_STATEMENT = 'bank_statement', _('Bank Statement')
    
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='kyc_requests')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED
    )
    
    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices
    )
    document_file = models.FileField(upload_to='kyc_documents/')
    document_metadata = models.JSONField(default=dict, blank=True)  # File metadata
    
    # Review information
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_kyc'
    )
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Audit trail
    activity_log = models.JSONField(default=list, blank=True)  # List of actions
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'kyc_requests'
        verbose_name = _('KYC Request')
        verbose_name_plural = _('KYC Requests')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['seller', 'status']),
        ]
    
    def __str__(self):
        return f"KYC {self.document_type} for {self.seller.store_name}"
    
    def add_activity_log(self, action, user, notes=""):
        """Add entry to activity log"""
        log_entry = {
            'action': action,
            'user': user.username if user else 'system',
            'notes': notes,
            'timestamp': models.DateTimeField().value_from_object(self)
        }
        self.activity_log.append(log_entry)
        self.save(update_fields=['activity_log'])

class StoreFollow(models.Model):
    """User following stores"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='followers')
    
    # Notification preferences for this follow
    notify_new_products = models.BooleanField(default=True)
    notify_price_drops = models.BooleanField(default=True)
    notify_restock = models.BooleanField(default=True)
    notify_campaigns = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'store_follows'
        unique_together = ['user', 'seller']
        verbose_name = _('Store Follow')
        verbose_name_plural = _('Store Follows')
    
    def __str__(self):
        return f"{self.user.username} follows {self.seller.store_name}"
    
    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        
        # Update follower count
        if created:
            self.seller.follower_count = self.seller.followers.count()
            self.seller.save(update_fields=['follower_count'])
    
    def delete(self, *args, **kwargs):
        seller = self.seller
        super().delete(*args, **kwargs)
        # Update follower count
        seller.follower_count = seller.followers.count()
        seller.save(update_fields=['follower_count'])
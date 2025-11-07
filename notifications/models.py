from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Notification(models.Model):
    """Generic notification system for all user activities"""
    
    class NotificationType(models.TextChoices):
        # KYC and Account
        KYC_SUBMITTED = 'kyc_submitted', _('KYC Submitted')
        KYC_APPROVED = 'kyc_approved', _('KYC Approved')
        KYC_REJECTED = 'kyc_rejected', _('KYC Rejected')
        KYC_NEEDS_INFO = 'kyc_needs_info', _('KYC Needs More Information')
        
        # Product and Store
        PRODUCT_PUBLISHED = 'product_published', _('Product Published')
        PRODUCT_OUT_OF_STOCK = 'product_out_of_stock', _('Product Out of Stock')
        PRODUCT_BACK_IN_STOCK = 'product_back_in_stock', _('Product Back in Stock')
        PRICE_DROP = 'price_drop', _('Price Drop')
        NEW_PRODUCT_FROM_FOLLOWED = 'new_product_from_followed', _('New Product from Followed Store')
        
        # Campaigns and Promotions
        CAMPAIGN_STARTED = 'campaign_started', _('Campaign Started')
        CAMPAIGN_ENDING_SOON = 'campaign_ending_soon', _('Campaign Ending Soon')
        COUPON_AVAILABLE = 'coupon_available', _('New Coupon Available')
        
        # Order and Transaction
        ORDER_PLACED = 'order_placed', _('Order Placed')
        ORDER_SHIPPED = 'order_shipped', _('Order Shipped')
        ORDER_DELIVERED = 'order_delivered', _('Order Delivered')
        ORDER_CANCELLED = 'order_cancelled', _('Order Cancelled')
        PAYMENT_RECEIVED = 'payment_received', _('Payment Received')
        PAYOUT_PROCESSED = 'payout_processed', _('Payout Processed')
        
        # Reviews and Ratings
        NEW_REVIEW = 'new_review', _('New Review')
        REVIEW_REPLY = 'review_reply', _('Review Reply')
        
        # Admin and System
        ACCOUNT_SUSPENDED = 'account_suspended', _('Account Suspended')
        POLICY_UPDATE = 'policy_update', _('Policy Update')
        SYSTEM_MAINTENANCE = 'system_maintenance', _('System Maintenance')
        
        # Social and Engagement
        STORE_FOLLOWED = 'store_followed', _('Store Followed')
        WISHLIST_ITEM_LOW_STOCK = 'wishlist_item_low_stock', _('Wishlist Item Low Stock')
        SELLER_MESSAGE = 'seller_message', _('Seller Message')
    
    class DeliveryStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENT = 'sent', _('Sent')
        FAILED = 'failed', _('Failed')
        BOUNCED = 'bounced', _('Bounced')
    
    # Core notification fields
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )
    
    # Content
    title = models.CharField(max_length=255)
    message = models.TextField()
    short_message = models.CharField(max_length=160, blank=True)  # For SMS/push
    
    # Generic foreign key for related objects
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Action URL
    action_url = models.URLField(blank=True)
    action_text = models.CharField(max_length=100, blank=True)
    
    # Delivery channels
    send_email = models.BooleanField(default=True)
    send_push = models.BooleanField(default=True)
    send_sms = models.BooleanField(default=False)
    send_in_app = models.BooleanField(default=True)
    
    # Delivery tracking
    email_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING
    )
    push_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING
    )
    sms_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING
    )
    
    # Read status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Priority
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', _('Low')),
            ('medium', _('Medium')),
            ('high', _('High')),
            ('urgent', _('Urgent')),
        ],
        default='medium'
    )
    
    # Batch processing
    batch_id = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type', 'created_at']),
            models.Index(fields=['email_status', 'push_status', 'sms_status']),
            models.Index(fields=['batch_id']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = models.DateTimeField().value_from_object(self)
            self.save(update_fields=['is_read', 'read_at'])

class NotificationPreference(models.Model):
    """User notification preferences by type"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Channel preferences by notification type
    preferences = models.JSONField(default=dict, blank=True)  # {notification_type: {email: true, push: true, sms: false}}
    
    # Global overrides
    disable_all_email = models.BooleanField(default=False)
    disable_all_push = models.BooleanField(default=False)
    disable_all_sms = models.BooleanField(default=False)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    # Frequency limits
    max_email_per_day = models.PositiveIntegerField(default=50)
    max_push_per_day = models.PositiveIntegerField(default=100)
    max_sms_per_day = models.PositiveIntegerField(default=10)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = _('Notification Preference')
        verbose_name_plural = _('Notification Preferences')
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
    
    def is_notification_type_enabled(self, notification_type, channel):
        """Check if a specific notification type and channel is enabled"""
        # Check global overrides
        if channel == 'email' and self.disable_all_email:
            return False
        if channel == 'push' and self.disable_all_push:
            return False
        if channel == 'sms' and self.disable_all_sms:
            return False
        
        # Check type-specific preferences
        type_prefs = self.preferences.get(notification_type, {})
        return type_prefs.get(channel, True)
    
    def set_notification_type_enabled(self, notification_type, channel, enabled):
        """Set preference for a specific notification type and channel"""
        if notification_type not in self.preferences:
            self.preferences[notification_type] = {}
        
        self.preferences[notification_type][channel] = enabled
        self.save(update_fields=['preferences'])

class EmailTemplate(models.Model):
    """Email templates for different notification types"""
    
    notification_type = models.CharField(
        max_length=50,
        choices=Notification.NotificationType.choices,
        unique=True
    )
    
    # Template content
    subject_template = models.CharField(max_length=255)
    html_template = models.TextField()
    text_template = models.TextField(blank=True)
    
    # Template variables help
    template_variables = models.JSONField(default=list, blank=True)  # List of available variables
    
    # Template metadata
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'email_templates'
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')
    
    def __str__(self):
        return f"Template for {self.get_notification_type_display()}"
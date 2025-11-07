from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ModerationAction(models.Model):
    """Moderation actions and decisions"""
    
    class ActionType(models.TextChoices):
        # Content moderation
        APPROVE_PRODUCT = 'approve_product', _('Approve Product')
        REJECT_PRODUCT = 'reject_product', _('Reject Product')
        BLOCK_PRODUCT = 'block_product', _('Block Product')
        APPROVE_SELLER = 'approve_seller', _('Approve Seller')
        REJECT_SELLER = 'reject_seller', _('Reject Seller')
        SUSPEND_SELLER = 'suspend_seller', _('Suspend Seller')
        
        # KYC moderation
        APPROVE_KYC = 'approve_kyc', _('Approve KYC')
        REJECT_KYC = 'reject_kyc', _('Reject KYC')
        REQUEST_KYC_INFO = 'request_kyc_info', _('Request More KYC Info')
        
        # Ad moderation
        APPROVE_AD = 'approve_ad', _('Approve Ad')
        REJECT_AD = 'reject_ad', _('Reject Ad')
        PAUSE_AD = 'pause_ad', _('Pause Ad')
        
        # Coupon moderation
        APPROVE_COUPON = 'approve_coupon', _('Approve Coupon')
        REJECT_COUPON = 'reject_coupon', _('Reject Coupon')
        DEACTIVATE_COUPON = 'deactivate_coupon', _('Deactivate Coupon')
        
        # Review moderation
        APPROVE_REVIEW = 'approve_review', _('Approve Review')
        REJECT_REVIEW = 'reject_review', _('Reject Review')
        FLAG_REVIEW = 'flag_review', _('Flag Review')
        
        # User moderation
        WARN_USER = 'warn_user', _('Warn User')
        SUSPEND_USER = 'suspend_user', _('Suspend User')
        BAN_USER = 'ban_user', _('Ban User')
        
        # System actions
        FEATURE_PRODUCT = 'feature_product', _('Feature Product')
        UNFEATURE_PRODUCT = 'unfeature_product', _('Unfeature Product')
        UPDATE_SELLER_TIER = 'update_seller_tier', _('Update Seller Tier')
    
    class Severity(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')
        CRITICAL = 'critical', _('Critical')
    
    # Action details
    action_type = models.CharField(max_length=50, choices=ActionType.choices)
    severity = models.CharField(
        max_length=20,
        choices=Severity.choices,
        default=Severity.MEDIUM
    )
    
    # Who performed the action
    moderator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='moderation_actions'
    )
    
    # Target object (generic relationship)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target_object = GenericForeignKey('content_type', 'object_id')
    
    # Action details
    reason = models.TextField()
    details = models.JSONField(default=dict, blank=True)  # Additional action data
    
    # Previous state (for rollback if needed)
    previous_state = models.JSONField(default=dict, blank=True)
    new_state = models.JSONField(default=dict, blank=True)
    
    # Action metadata
    is_automated = models.BooleanField(default=False)  # Was this an automated action?
    confidence_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )  # For ML-based moderation
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'moderation_actions'
        verbose_name = _('Moderation Action')
        verbose_name_plural = _('Moderation Actions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['moderator', 'created_at']),
            models.Index(fields=['action_type', 'created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['is_automated', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_action_type_display()} by {self.moderator.username}"

class ContentFlag(models.Model):
    """User-generated content flags for review"""
    
    class FlagType(models.TextChoices):
        SPAM = 'spam', _('Spam')
        INAPPROPRIATE = 'inappropriate', _('Inappropriate Content')
        COPYRIGHT = 'copyright', _('Copyright Violation')
        COUNTERFEIT = 'counterfeit', _('Counterfeit Product')
        MISLEADING = 'misleading', _('Misleading Information')
        HARASSMENT = 'harassment', _('Harassment')
        OTHER = 'other', _('Other')
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending Review')
        UNDER_REVIEW = 'under_review', _('Under Review')
        RESOLVED = 'resolved', _('Resolved')
        DISMISSED = 'dismissed', _('Dismissed')
    
    # Flag details
    flag_type = models.CharField(max_length=30, choices=FlagType.choices)
    description = models.TextField(blank=True)  # Additional details from reporter
    
    # Who flagged it
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='content_flags'
    )
    
    # Content that was flagged (generic relationship)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # Review details
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_flags'
    )
    review_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Priority (based on flag type and reporter history)
    priority_score = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'content_flags'
        verbose_name = _('Content Flag')
        verbose_name_plural = _('Content Flags')
        ordering = ['-priority_score', '-created_at']
        indexes = [
            models.Index(fields=['status', 'priority_score']),
            models.Index(fields=['flag_type', 'created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['reporter', 'created_at']),
        ]
    
    def __str__(self):
        return f"Flag for {self.content_object} ({self.get_flag_type_display()})"

class AutoModerationRule(models.Model):
    """Rules for automated content moderation"""
    
    class RuleType(models.TextChoices):
        CONTENT_FILTER = 'content_filter', _('Content Filter')
        IMAGE_ANALYSIS = 'image_analysis', _('Image Analysis')
        BEHAVIOR_DETECTION = 'behavior_detection', _('Behavior Detection')
        DUPLICATE_DETECTION = 'duplicate_detection', _('Duplicate Detection')
        PRICE_ANOMALY = 'price_anomaly', _('Price Anomaly Detection')
        REVIEW_SPAM = 'review_spam', _('Review Spam Detection')
    
    class Action(models.TextChoices):
        FLAG_FOR_REVIEW = 'flag_for_review', _('Flag for Review')
        AUTO_REJECT = 'auto_reject', _('Auto Reject')
        AUTO_APPROVE = 'auto_approve', _('Auto Approve')
        HOLD_FOR_MANUAL = 'hold_for_manual', _('Hold for Manual Review')
        ESCALATE = 'escalate', _('Escalate to Senior Moderator')
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    rule_type = models.CharField(max_length=30, choices=RuleType.choices)
    
    # Rule conditions (JSON for flexibility)
    conditions = models.JSONField(default=dict)
    
    # Action to take
    action = models.CharField(max_length=30, choices=Action.choices)
    severity = models.CharField(
        max_length=20,
        choices=ModerationAction.Severity.choices,
        default=ModerationAction.Severity.MEDIUM
    )
    
    # Rule settings
    is_active = models.BooleanField(default=True)
    confidence_threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.80
    )  # Minimum confidence for automated action
    
    # Scope
    applies_to = models.JSONField(default=list, blank=True)  # List of content types
    
    # Performance tracking
    times_triggered = models.PositiveIntegerField(default=0)
    false_positives = models.PositiveIntegerField(default=0)
    true_positives = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'auto_moderation_rules'
        verbose_name = _('Auto Moderation Rule')
        verbose_name_plural = _('Auto Moderation Rules')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def accuracy(self):
        """Calculate rule accuracy"""
        if self.times_triggered > 0:
            return round((self.true_positives / self.times_triggered) * 100, 2)
        return 0.00

class AccountHealthScore(models.Model):
    """Account health scoring and metrics"""
    
    class ScoreType(models.TextChoices):
        OVERALL = 'overall', _('Overall Health')
        PERFORMANCE = 'performance', _('Performance')
        COMPLIANCE = 'compliance', _('Compliance')
        CUSTOMER_SATISFACTION = 'customer_satisfaction', _('Customer Satisfaction')
        CONTENT_QUALITY = 'content_quality', _('Content Quality')
    
    seller = models.ForeignKey('sellers.SellerProfile', on_delete=models.CASCADE, related_name='health_scores')
    score_type = models.CharField(max_length=30, choices=ScoreType.choices)
    
    # Score (0-100)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Component scores
    component_scores = models.JSONField(default=dict, blank=True)  # Breakdown of score components
    
    # Metrics
    metrics = models.JSONField(default=dict, blank=True)  # Raw metrics used for calculation
    
    # Evaluation details
    evaluated_at = models.DateTimeField(auto_now_add=True)
    evaluated_by = models.CharField(max_length=50, default='system')  # 'system' or username
    
    # Recommendations
    recommendations = models.JSONField(default=list, blank=True)  # List of improvement suggestions
    
    # Flags
    requires_immediate_action = models.BooleanField(default=False)
    is_critical = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'account_health_scores'
        verbose_name = _('Account Health Score')
        verbose_name_plural = _('Account Health Scores')
        unique_together = ['seller', 'score_type', 'evaluated_at']
        ordering = ['-evaluated_at']
        indexes = [
            models.Index(fields=['seller', 'score_type']),
            models.Index(fields=['score', 'evaluated_at']),
            models.Index(fields=['requires_immediate_action', 'is_critical']),
        ]
    
    def __str__(self):
        return f"{self.seller.store_name} - {self.get_score_type_display()}: {self.score}"
    
    @property
    def score_grade(self):
        """Convert score to letter grade"""
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'
    
    @property
    def score_color(self):
        """Get color coding for score"""
        if self.score >= 80:
            return 'green'
        elif self.score >= 60:
            return 'yellow'
        else:
            return 'red'
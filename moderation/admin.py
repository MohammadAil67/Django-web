from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import ModerationAction, ContentFlag, AutoModerationRule, AccountHealthScore

@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = [
        'action_type', 'moderator', 'target_object', 'severity',
        'is_automated', 'confidence_score', 'created_at'
    ]
    list_filter = [
        'action_type', 'severity', 'is_automated', 'created_at'
    ]
    search_fields = ['moderator__username', 'reason']
    readonly_fields = ['created_at', 'previous_state', 'new_state']
    
    fieldsets = (
        (_('Action Details'), {
            'fields': (
                'action_type', 'severity', 'moderator', 'reason', 'details'
            )
        }),
        (_('Target Object'), {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        (_('Automation Info'), {
            'fields': ('is_automated', 'confidence_score')
        }),
        (_('State Changes'), {
            'fields': ('previous_state', 'new_state'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContentFlag)
class ContentFlagAdmin(admin.ModelAdmin):
    list_display = [
        'flag_type', 'reporter', 'content_object', 'status', 'priority_score', 'created_at'
    ]
    list_filter = ['flag_type', 'status', 'created_at']
    search_fields = ['reporter__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Flag Details'), {
            'fields': (
                'flag_type', 'description', 'reporter'
            )
        }),
        (_('Content'), {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        (_('Review'), {
            'fields': (
                'status', 'reviewed_by', 'review_notes', 'reviewed_at'
            )
        }),
        (_('Priority'), {
            'fields': ('priority_score',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_flag', 'dismiss_flag']
    
    def approve_flag(self, request, queryset):
        updated = queryset.update(status='resolved', reviewed_by=request.user)
        self.message_user(request, _(
            f'{updated} flag(s) have been approved.'
        ))
    approve_flag.short_description = _('Approve selected flags')
    
    def dismiss_flag(self, request, queryset):
        updated = queryset.update(status='dismissed', reviewed_by=request.user)
        self.message_user(request, _(
            f'{updated} flag(s) have been dismissed.'
        ))
    dismiss_flag.short_description = _('Dismiss selected flags')

@admin.register(AutoModerationRule)
class AutoModerationRuleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'rule_type', 'action', 'severity', 'is_active',
        'confidence_threshold', 'accuracy', 'times_triggered'
    ]
    list_filter = ['rule_type', 'action', 'severity', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'accuracy']
    
    fieldsets = (
        (_('Rule Information'), {
            'fields': (
                'name', 'description', 'rule_type', 'is_active'
            )
        }),
        (_('Conditions & Action'), {
            'fields': (
                'conditions', 'action', 'severity', 'confidence_threshold'
            )
        }),
        (_('Scope'), {
            'fields': ('applies_to',),
            'classes': ('collapse',)
        }),
        (_('Performance'), {
            'fields': (
                'times_triggered', 'false_positives', 'true_positives', 'accuracy'
            ),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_rule', 'deactivate_rule']
    
    def activate_rule(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _(
            f'{updated} rule(s) have been activated.'
        ))
    activate_rule.short_description = _('Activate selected rules')
    
    def deactivate_rule(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _(
            f'{updated} rule(s) have been deactivated.'
        ))
    deactivate_rule.short_description = _('Deactivate selected rules')

@admin.register(AccountHealthScore)
class AccountHealthScoreAdmin(admin.ModelAdmin):
    list_display = [
        'seller', 'score_type', 'score', 'score_grade', 'score_color',
        'requires_immediate_action', 'is_critical', 'evaluated_at'
    ]
    list_filter = [
        'score_type', 'requires_immediate_action', 'is_critical', 'evaluated_at'
    ]
    search_fields = ['seller__store_name', 'seller__user__username']
    readonly_fields = ['evaluated_at']
    
    fieldsets = (
        (_('Score Information'), {
            'fields': (
                'seller', 'score_type', 'score'
            )
        }),
        (_('Details'), {
            'fields': (
                'component_scores', 'metrics', 'evaluated_by'
            ),
            'classes': ('collapse',)
        }),
        (_('Recommendations'), {
            'fields': ('recommendations',),
            'classes': ('collapse',)
        }),
        (_('Flags'), {
            'fields': ('requires_immediate_action', 'is_critical')
        }),
        (_('Evaluation Time'), {
            'fields': ('evaluated_at',)
        }),
    )
    
    def score_grade(self, obj):
        return obj.score_grade
    score_grade.short_description = _('Grade')
    
    def score_color(self, obj):
        color = obj.score_color
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span>',
            color
        )
    score_color.short_description = _('Color')
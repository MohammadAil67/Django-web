from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Notification, NotificationPreference, EmailTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'recipient', 'notification_type', 'priority',
        'is_read', 'email_status', 'push_status', 'created_at'
    ]
    list_filter = [
        'notification_type', 'priority', 'is_read',
        'email_status', 'push_status', 'sms_status', 'created_at'
    ]
    search_fields = ['title', 'message', 'recipient__username', 'recipient__email']
    readonly_fields = ['created_at', 'sent_at', 'read_at']
    
    fieldsets = (
        (_('Notification Details'), {
            'fields': (
                'recipient', 'notification_type', 'title', 'message', 'short_message'
            )
        }),
        (_('Related Object'), {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        (_('Action'), {
            'fields': ('action_url', 'action_text')
        }),
        (_('Delivery Channels'), {
            'fields': (
                'send_email', 'send_push', 'send_sms', 'send_in_app'
            )
        }),
        (_('Delivery Status'), {
            'fields': (
                'email_status', 'push_status', 'sms_status'
            )
        }),
        (_('Status'), {
            'fields': ('is_read', 'read_at', 'priority', 'batch_id')
        }),
        (_('Scheduling'), {
            'fields': ('scheduled_for', 'sent_at'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_sent', 'resend_failed', 'mark_all_as_read']
    
    def mark_as_sent(self, request, queryset):
        updated = queryset.filter(email_status='pending').update(email_status='sent')
        self.message_user(request, _(
            f'{updated} notification(s) have been marked as sent.'
        ))
    mark_as_sent.short_description = _('Mark selected notifications as sent')
    
    def resend_failed(self, request, queryset):
        failed_notifications = queryset.filter(
            models.Q(email_status='failed') | 
            models.Q(push_status='failed') | 
            models.Q(sms_status='failed')
        )
        # Here you would typically trigger a celery task to resend
        count = failed_notifications.count()
        self.message_user(request, _(
            f'Resend triggered for {count} failed notification(s).'
        ))
    resend_failed.short_description = _('Resend failed notifications')
    
    def mark_all_as_read(self, request, queryset):
        updated = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(request, _(
            f'{updated} notification(s) have been marked as read.'
        ))
    mark_all_as_read.short_description = _('Mark selected notifications as read')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'disable_all_email', 'disable_all_push', 'disable_all_sms']
    list_filter = [
        'disable_all_email', 'disable_all_push', 'disable_all_sms',
        'quiet_hours_enabled', 'created_at'
    ]
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Global Overrides'), {
            'fields': (
                'disable_all_email', 'disable_all_push', 'disable_all_sms'
            )
        }),
        (_('Quiet Hours'), {
            'fields': (
                'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end'
            )
        }),
        (_('Frequency Limits'), {
            'fields': (
                'max_email_per_day', 'max_push_per_day', 'max_sms_per_day'
            )
        }),
        (_('Type-Specific Preferences'), {
            'fields': ('preferences',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['notification_type', 'subject_template', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['notification_type', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Template Information'), {
            'fields': (
                'notification_type', 'description', 'is_active'
            )
        }),
        (_('Content'), {
            'fields': (
                'subject_template', 'html_template', 'text_template'
            )
        }),
        (_('Template Variables'), {
            'fields': ('template_variables',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
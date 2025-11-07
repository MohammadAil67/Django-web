from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import Notification, NotificationPreference
from .forms import NotificationPreferenceForm

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'unread_count': Notification.objects.filter(
                recipient=self.request.user,
                is_read=False
            ).count(),
            'total_count': Notification.objects.filter(
                recipient=self.request.user
            ).count(),
        })
        return context

class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(
            Notification, 
            pk=pk, 
            recipient=request.user
        )
        notification.mark_as_read()
        messages.success(request, _('Notification marked as read.'))
        
        return redirect(request.META.get('HTTP_REFERER', 'notifications:list'))

class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        
        messages.success(
            request, 
            _('%d notifications marked as read.' % updated)
        )
        
        return redirect('notifications:list')

class NotificationSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create notification preference
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        
        context.update({
            'preference': preference,
            'form': NotificationPreferenceForm(instance=preference),
        })
        return context
    
    def post(self, request, *args, **kwargs):
        preference, created = NotificationPreference.objects.get_or_create(
            user=request.user
        )
        
        form = NotificationPreferenceForm(request.POST, instance=preference)
        
        if form.is_valid():
            form.save()
            messages.success(request, _('Notification settings updated successfully!'))
            return redirect('notifications:settings')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
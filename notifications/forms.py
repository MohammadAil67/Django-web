from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from .models import NotificationPreference

class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = [
            'disable_all_email', 'disable_all_push', 'disable_all_sms',
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
            'max_email_per_day', 'max_push_per_day', 'max_sms_per_day'
        ]
        widgets = {
            'quiet_hours_start': forms.TimeInput(attrs={'type': 'time'}),
            'quiet_hours_end': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            HTML('<h3 class="text-lg font-medium text-gray-900">Global Settings</h3>'),
            
            Div(
                HTML('<div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">'),
                HTML('<div class="flex">'),
                HTML('<div class="flex-shrink-0">'),
                HTML('<svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>'),
                HTML('</div>'),
                HTML('<div class="ml-3">'),
                HTML('<p class="text-sm text-yellow-700">'),
                HTML('<strong>Warning:</strong> Disabling all notifications will prevent you from receiving important updates about your account, orders, and store activities.'),
                HTML('</p>'),
                HTML('</div>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='mb-6'
            ),
            
            Div(
                HTML('<div class="relative flex items-start">'),
                Field('disable_all_email', css_class='h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'),
                HTML('<div class="ml-3 text-sm">'),
                HTML('<label for="id_disable_all_email" class="font-medium text-gray-700">Disable All Email Notifications</label>'),
                HTML('<p class="text-gray-500">Stop receiving all email notifications</p>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='space-y-4'
            ),
            
            Div(
                HTML('<div class="relative flex items-start">'),
                Field('disable_all_push', css_class='h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'),
                HTML('<div class="ml-3 text-sm">'),
                HTML('<label for="id_disable_all_push" class="font-medium text-gray-700">Disable All Push Notifications</label>'),
                HTML('<p class="text-gray-500">Stop receiving browser push notifications</p>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='space-y-4'
            ),
            
            Div(
                HTML('<div class="relative flex items-start">'),
                Field('disable_all_sms', css_class='h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'),
                HTML('<div class="ml-3 text-sm">'),
                HTML('<label for="id_disable_all_sms" class="font-medium text-gray-700">Disable All SMS Notifications</label>'),
                HTML('<p class="text-gray-500">Stop receiving text message notifications</p>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='space-y-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Quiet Hours</h3>'),
            
            Div(
                HTML('<div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">'),
                HTML('<div class="flex">'),
                HTML('<div class="flex-shrink-0">'),
                HTML('<svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" /></svg>'),
                HTML('</div>'),
                HTML('<div class="ml-3">'),
                HTML('<p class="text-sm text-blue-700">'),
                HTML('Quiet hours prevent notifications during specified times. This helps you maintain work-life balance.'),
                HTML('</p>'),
                HTML('</div>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='mb-6'
            ),
            
            Div(
                HTML('<div class="relative flex items-start">'),
                Field('quiet_hours_enabled', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                HTML('<div class="ml-3 text-sm">'),
                HTML('<label for="id_quiet_hours_enabled" class="font-medium text-gray-700">Enable Quiet Hours</label>'),
                HTML('<p class="text-gray-500">Prevent notifications during specified hours</p>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='space-y-4'
            ),
            
            Div(
                Div(
                    Field('quiet_hours_start', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('quiet_hours_end', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Frequency Limits</h3>'),
            
            Div(
                HTML('<div class="bg-green-50 border-l-4 border-green-400 p-4 mb-4">'),
                HTML('<div class="flex">'),
                HTML('<div class="flex-shrink-0">'),
                HTML('<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zm-1 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" /></svg>'),
                HTML('</div>'),
                HTML('<div class="ml-3">'),
                HTML('<p class="text-sm text-green-700">'),
                HTML('Set daily limits to prevent notification overload. We recommend keeping reasonable limits to maintain a good user experience.'),
                HTML('</p>'),
                HTML('</div>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='mb-6'
            ),
            
            Div(
                Div(
                    Field('max_email_per_day', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('max_push_per_day', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            
            Div(
                Field('max_sms_per_day', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            Div(
                Submit('submit', _('Save Notification Settings'), css_class='inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'),
                css_class='mt-6'
            )
        )
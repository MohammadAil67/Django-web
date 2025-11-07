from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from crispy_forms.bootstrap import FormActions

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    preferred_language = forms.ChoiceField(
        choices=User._meta.get_field('preferred_language').choices,
        initial='en'
    )
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'phone_number', 'preferred_language', 'password1', 'password2'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('email', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Div(
                    Field('first_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('last_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Field('phone_number', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('preferred_language', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('password1', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('password2', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            FormActions(
                Submit('submit', _('Create Account'), css_class='w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.preferred_language = self.cleaned_data['preferred_language']
        
        if commit:
            user.save()
        return user

class SellerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    
    # Seller-specific fields
    store_name = forms.CharField(max_length=255, required=True)
    store_description = forms.CharField(widget=forms.Textarea, required=False)
    business_type = forms.CharField(max_length=100, required=False)
    business_phone = forms.CharField(max_length=20, required=False)
    business_email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'phone_number',
            'store_name', 'store_description', 'business_type', 
            'business_phone', 'business_email', 'password1', 'password2'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            HTML('<h3 class="text-lg font-medium text-gray-900">Account Information</h3>'),
            Div(
                Field('username', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('email', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Div(
                    Field('first_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('last_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Field('phone_number', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Store Information</h3>'),
            Div(
                Field('store_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('store_description', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('business_type', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Div(
                    Field('business_phone', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('business_email', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Security</h3>'),
            Div(
                Field('password1', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('password2', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            FormActions(
                Submit('submit', _('Create Seller Account'), css_class='w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500')
            )
        )

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            Div(
                Field('username', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('password', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            FormActions(
                Submit('submit', _('Sign In'), css_class='w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'preferred_language', 'email_notifications',
            'push_notifications', 'sms_notifications', 'reduced_data_mode'
        ]
        widgets = {
            'email_notifications': forms.CheckboxInput(),
            'push_notifications': forms.CheckboxInput(),
            'sms_notifications': forms.CheckboxInput(),
            'reduced_data_mode': forms.CheckboxInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('last_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Field('email', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('phone_number', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('preferred_language', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            HTML('<h3 class="text-lg font-medium text-gray-900">Notification Preferences</h3>'),
            Div(
                Div(
                    HTML('<div class="relative flex items-start">'),
                    Field('email_notifications', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                    HTML('<div class="ml-3 text-sm">'),
                    HTML('<label for="id_email_notifications" class="font-medium text-gray-700">Email Notifications</label>'),
                    HTML('<p class="text-gray-500">Get notified via email</p>'),
                    HTML('</div>'),
                    HTML('</div>'),
                    css_class='space-y-4'
                ),
                Div(
                    HTML('<div class="relative flex items-start">'),
                    Field('push_notifications', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                    HTML('<div class="ml-3 text-sm">'),
                    HTML('<label for="id_push_notifications" class="font-medium text-gray-700">Push Notifications</label>'),
                    HTML('<p class="text-gray-500">Get push notifications in your browser</p>'),
                    HTML('</div>'),
                    HTML('</div>'),
                    css_class='space-y-4'
                ),
                Div(
                    HTML('<div class="relative flex items-start">'),
                    Field('sms_notifications', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                    HTML('<div class="ml-3 text-sm">'),
                    HTML('<label for="id_sms_notifications" class="font-medium text-gray-700">SMS Notifications</label>'),
                    HTML('<p class="text-gray-500">Get notified via text message</p>'),
                    HTML('</div>'),
                    HTML('</div>'),
                    css_class='space-y-4'
                ),
                css_class='space-y-6'
            ),
            HTML('<h3 class="text-lg font-medium text-gray-900">Data Usage</h3>'),
            Div(
                HTML('<div class="relative flex items-start">'),
                Field('reduced_data_mode', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                HTML('<div class="ml-3 text-sm">'),
                HTML('<label for="id_reduced_data_mode" class="font-medium text-gray-700">Reduced Data Mode</label>'),
                HTML('<p class="text-gray-500">Use less data when browsing (reduces image quality and animations)</p>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='space-y-4'
            ),
            FormActions(
                Submit('submit', _('Update Profile'), css_class='inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )
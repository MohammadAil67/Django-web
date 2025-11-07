from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from .models import SellerProfile, KYCRequest
from crispy_forms.bootstrap import FormActions

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = [
            'store_name', 'description', 'logo', 'banner_image',
            'business_type', 'business_registration_number', 'tax_id',
            'business_phone', 'business_email', 'business_address',
            'supports_international_shipping', 'return_policy', 'shipping_policy',
            'meta_title', 'meta_description', 'keywords'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'business_address': forms.Textarea(attrs={'rows': 3}),
            'return_policy': forms.Textarea(attrs={'rows': 4}),
            'shipping_policy': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            HTML('<h3 class="text-lg font-medium text-gray-900">Store Information</h3>'),
            Div(
                Field('store_name', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('description', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Div(
                    Field('logo', css_class='mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('banner_image', css_class='mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Business Information</h3>'),
            Div(
                Field('business_type', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Div(
                    Field('business_registration_number', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('tax_id', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
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
            Div(
                Field('business_address', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Store Settings</h3>'),
            Div(
                HTML('<div class="relative flex items-start">'),
                Field('supports_international_shipping', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                HTML('<div class="ml-3 text-sm">'),
                HTML('<label for="id_supports_international_shipping" class="font-medium text-gray-700">Support International Shipping</label>'),
                HTML('<p class="text-gray-500">Allow customers from other countries to purchase your products</p>'),
                HTML('</div>'),
                HTML('</div>'),
                css_class='space-y-4'
            ),
            Div(
                Field('return_policy', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('shipping_policy', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">SEO & Marketing</h3>'),
            Div(
                Field('meta_title', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('meta_description', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('keywords', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            FormActions(
                Submit('submit', _('Update Store Profile'), css_class='inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )

class KYCRequestForm(forms.ModelForm):
    class Meta:
        model = KYCRequest
        fields = ['document_type', 'document_file', 'document_metadata']
        widgets = {
            'document_metadata': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            HTML('<div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6">'),
            HTML('<div class="flex">'),
            HTML('<div class="flex-shrink-0">'),
            HTML('<svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" /></svg>'),
            HTML('</div>'),
            HTML('<div class="ml-3">'),
            HTML('<p class="text-sm text-blue-700">'),
            HTML('<strong>Important:</strong> Please upload clear, high-quality documents. All documents will be reviewed within 24-48 hours.'),
            HTML('</p>'),
            HTML('</div>'),
            HTML('</div>'),
            HTML('</div>'),
            
            Div(
                Field('document_type', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('document_file', css_class='mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'),
                css_class='space-y-4'
            ),
            
            HTML('<div class="bg-gray-50 p-4 rounded-lg">'),
            HTML('<h4 class="text-sm font-medium text-gray-900 mb-2">Document Requirements:</h4>'),
            HTML('<ul class="text-sm text-gray-600 space-y-1">'),
            HTML('<li>• Clear, high-resolution images or PDFs</li>'),
            HTML('<li>• All text must be clearly readable</li>'),
            HTML('<li>• No expired documents</li>'),
            HTML('<li>• Maximum file size: 10MB</li>'),
            HTML('<li>• Accepted formats: JPG, PNG, PDF</li>'),
            HTML('</ul>'),
            HTML('</div>'),
            
            FormActions(
                Submit('submit', _('Submit Document'), css_class='w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )
    
    def clean_document_file(self):
        file = self.cleaned_data.get('document_file')
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(_('File size must be less than 10MB.'))
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
            if file.content_type not in allowed_types:
                raise forms.ValidationError(_('Only JPG, PNG, and PDF files are allowed.'))
        
        return file
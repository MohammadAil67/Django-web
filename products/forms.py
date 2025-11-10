from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from crispy_forms.bootstrap import FormActions
from .models import Product, ProductImage, ProductReview

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'slug', 'description', 'short_description',
            'category', 'price', 'old_price', 'cost_price',
            'sku', 'stock_quantity', 'min_stock_level', 'track_inventory',
            'condition', 'brand', 'model', 'weight', 'dimensions',
            'attributes', 'meta_title', 'meta_description', 'keywords',
            'is_featured', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'slug': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'short_description': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'price': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm', 'step': '0.01'}),
            'old_price': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm', 'step': '0.01'}),
            'cost_price': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm', 'step': '0.01'}),
            'sku': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'condition': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'brand': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'model': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'weight': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm', 'step': '0.001'}),
            'dimensions': forms.TextInput(attrs={'placeholder': '10x5x3', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'attributes': forms.Textarea(attrs={'rows': 3, 'placeholder': '{"color": "red", "size": "M"}', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'meta_title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'meta_description': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'keywords': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
            'track_inventory': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1'
        
        self.helper.layout = Layout(
            HTML('<h3 class="text-lg font-medium text-gray-900">Basic Information</h3>'),
            
            Div(
                Field('title', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('slug', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('description', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('short_description', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('category', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Pricing & Inventory</h3>'),
            
            Div(
                Div(
                    Field('price', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('old_price', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Field('cost_price', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Div(
                    Field('sku', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('stock_quantity', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Div(
                    Field('min_stock_level', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    HTML('<div class="relative flex items-start pt-6">'),
                    Field('track_inventory', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                    HTML('<div class="ml-3 text-sm">'),
                    HTML('<label for="id_track_inventory" class="font-medium text-gray-700">Track Inventory</label>'),
                    HTML('<p class="text-gray-500">Monitor stock levels automatically</p>'),
                    HTML('</div>'),
                    HTML('</div>'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Product Details</h3>'),
            
            Div(
                Div(
                    Field('condition', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('brand', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Div(
                    Field('model', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('weight', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            Div(
                Field('dimensions', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('attributes', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
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
            
            HTML('<h3 class="text-lg font-medium text-gray-900 mt-8">Status & Visibility</h3>'),
            
            Div(
                Div(
                    HTML('<div class="relative flex items-start">'),
                    Field('is_featured', css_class='h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'),
                    HTML('<div class="ml-3 text-sm">'),
                    HTML('<label for="id_is_featured" class="font-medium text-gray-700">Featured Product</label>'),
                    HTML('<p class="text-gray-500">Show this product in featured sections</p>'),
                    HTML('</div>'),
                    HTML('</div>'),
                    css_class='sm:col-span-2'
                ),
                Div(
                    Field('status', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                    css_class='sm:col-span-2'
                ),
                css_class='grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-4'
            ),
            
            FormActions(
                Submit('submit', _('Save Product'), css_class='inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug:
            # Check if slug already exists (excluding current instance)
            queryset = Product.objects.filter(slug=slug)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError(_('This slug is already in use.'))
        return slug
    
    def clean_attributes(self):
        import json
        attributes = self.cleaned_data.get('attributes')
        if attributes:
            try:
                if isinstance(attributes, str):
                    json.loads(attributes)
            except json.JSONDecodeError:
                raise forms.ValidationError(_('Invalid JSON format for attributes.'))
        return attributes

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
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
                Field('rating', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('title', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            Div(
                Field('comment', css_class='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'),
                css_class='space-y-4'
            ),
            FormActions(
                Submit('submit', _('Submit Review'), css_class='inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500')
            )
        )
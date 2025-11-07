from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files import File
from io import BytesIO
from PIL import Image
import random

from users.models import User
from sellers.models import SellerProfile, KYCRequest
from products.models import Product, Category, ProductImage
from campaigns.models import Campaign, Coupon

class Command(BaseCommand):
    help = 'Create sample data for the marketplace'
    
    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--sellers', type=int, default=5, help='Number of sellers to create')
        parser.add_argument('--products', type=int, default=20, help='Number of products to create')
        parser.add_argument('--categories', type=int, default=5, help='Number of categories to create')
        parser.add_argument('--campaigns', type=int, default=3, help='Number of campaigns to create')
        parser.add_argument('--coupons', type=int, default=5, help='Number of coupons to create')
    
    def create_dummy_image(self, width=300, height=300, color=None):
        """Create a dummy image for testing"""
        if color is None:
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
            color = random.choice(colors)
        
        image = Image.new('RGB', (width, height), color)
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return File(buffer, name=f'dummy_{color}_{width}x{height}.jpg')
    
    def create_superuser(self):
        """Create a superuser for admin access"""
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@minimalist-marketplace.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role=User.Role.ADMIN
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
    
    def create_categories(self, count):
        """Create sample categories"""
        category_names = [
            'Electronics', 'Fashion', 'Home & Garden', 'Sports & Outdoors',
            'Books & Media', 'Health & Beauty', 'Toys & Games', 'Automotive'
        ]
        
        categories = []
        for i in range(min(count, len(category_names))):
            category, created = Category.objects.get_or_create(
                name=category_names[i],
                defaults={
                    'slug': slugify(category_names[i]),
                    'description': f'High-quality {category_names[i].lower()} products',
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        return categories
    
    def create_users(self, count):
        """Create sample users"""
        users = []
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'James', 'Lisa', 'Robert', 'Maria']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'{first_name.lower()}{last_name.lower()}{i+1}'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': User.Role.BUYER,
                    'is_verified': True
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                users.append(user)
                self.stdout.write(f'Created user: {username}')
        
        return users
    
    def create_sellers(self, count, users):
        """Create sample sellers"""
        sellers = []
        store_names = [
            'TechHub Store', 'Fashion Forward', 'Home Essentials', 'Sports Pro', 'Book Haven',
            'Beauty Corner', 'Toy World', 'Auto Parts Plus', 'Gadget Galaxy', 'Style Studio'
        ]
        
        for i in range(min(count, len(users))):
            user = users[i]
            user.role = User.Role.SELLER
            user.save()
            
            store_name = store_names[i % len(store_names)]
            seller_profile, created = SellerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'store_name': store_name,
                    'store_slug': slugify(store_name),
                    'description': f'Welcome to {store_name}! We offer high-quality products at competitive prices.',
                    'business_type': 'Retail',
                    'verification_status': SellerProfile.VerificationStatus.VERIFIED,
                    'tier': random.choice(['bronze', 'silver', 'gold']),
                    'is_active': True,
                    'supports_international_shipping': random.choice([True, False])
                }
            )
            
            if created:
                sellers.append(seller_profile)
                self.stdout.write(f'Created seller: {seller_profile.store_name}')
        
        return sellers
    
    def create_products(self, count, sellers, categories):
        """Create sample products"""
        products = []
        product_names = [
            'Premium Wireless Headphones', 'Smart Fitness Tracker', 'Organic Cotton T-Shirt',
            'Professional Yoga Mat', 'Bestseller Novel Collection', 'Natural Face Serum',
            'Educational Building Blocks', 'Car Phone Mount', 'Bluetooth Speaker',
            'Running Shoes', 'LED Desk Lamp', 'Stainless Steel Water Bottle',
            'Portable Charger', 'Kitchen Knife Set', 'Memory Foam Pillow',
            'Wireless Mouse', 'Sunglasses', 'Backpack', 'Coffee Maker', 'Plant Pot Set'
        ]
        
        for i in range(count):
            seller = random.choice(sellers)
            category = random.choice(categories)
            product_name = product_names[i % len(product_names)]
            
            price = round(random.uniform(10.0, 200.0), 2)
            old_price = None
            if random.random() > 0.7:  # 30% chance of having old price
                old_price = round(price * random.uniform(1.2, 2.0), 2)
            
            product = Product.objects.create(
                seller=seller,
                category=category,
                title=product_name,
                slug=slugify(product_name),
                description=f'High-quality {product_name.lower()} with excellent features and durability. Perfect for everyday use.',
                short_description=f'Premium {product_name.lower()} at great value',
                price=price,
                old_price=old_price,
                stock_quantity=random.randint(1, 50),
                condition='new',
                brand='Premium Brand',
                sku=f'SKU{random.randint(1000, 9999)}',
                status='published',
                is_featured=random.random() > 0.8,
                is_active=True
            )
            
            # Create product images
            for j in range(random.randint(1, 3)):
                ProductImage.objects.create(
                    product=product,
                    image=self.create_dummy_image(600, 600),
                    alt_text=f'{product_name} - Image {j+1}',
                    is_primary=(j == 0),
                    sort_order=j
                )
            
            products.append(product)
            self.stdout.write(f'Created product: {product.title}')
        
        return products
    
    def create_campaigns(self, count, sellers):
        """Create sample campaigns"""
        campaigns = []
        campaign_names = [
            'Summer Sale 2024', 'New Year Deals', 'Flash Friday Sale',
            'Back to School Special', 'Holiday Shopping Fest'
        ]
        
        for i in range(min(count, len(campaign_names))):
            selected_sellers = random.sample(sellers, min(3, len(sellers)))
            
            campaign = Campaign.objects.create(
                title=campaign_names[i],
                slug=slugify(campaign_names[i]),
                description=f'Amazing deals and discounts during our {campaign_names[i]} event!',
                campaign_type=random.choice(['flash_sale', 'seasonal', 'clearance']),
                status='active',
                start_date='2024-01-01T00:00:00Z',
                end_date='2024-12-31T23:59:59Z',
                discount_percentage=random.randint(10, 50),
                is_featured=True,
                show_on_homepage=True
            )
            
            campaign.eligible_sellers.set(selected_sellers)
            campaigns.append(campaign)
            self.stdout.write(f'Created campaign: {campaign.title}')
        
        return campaigns
    
    def create_coupons(self, count, sellers):
        """Create sample coupons"""
        coupons = []
        coupon_codes = ['SAVE10', 'WELCOME20', 'FLASH25', 'SUMMER30', 'FIRST15']
        
        for i in range(min(count, len(coupon_codes))):
            seller = random.choice(sellers) if random.random() > 0.5 else None
            
            coupon = Coupon.objects.create(
                code=coupon_codes[i],
                description=f'Get {10 + (i * 5)}% off on your purchase',
                discount_type='percentage',
                discount_value=10 + (i * 5),
                valid_from='2024-01-01T00:00:00Z',
                valid_to='2024-12-31T23:59:59Z',
                seller=seller,
                status='approved',
                usage_limit=100,
                usage_per_customer=1
            )
            
            coupons.append(coupon)
            self.stdout.write(f'Created coupon: {coupon.code}')
        
        return coupons
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create superuser
        self.create_superuser()
        
        # Create categories
        categories = self.create_categories(options['categories'])
        
        # Create users
        users = self.create_users(options['users'])
        
        # Create sellers
        sellers = self.create_sellers(options['sellers'], users)
        
        # Create products
        products = self.create_products(options['products'], sellers, categories)
        
        # Create campaigns
        campaigns = self.create_campaigns(options['campaigns'], sellers)
        
        # Create coupons
        coupons = self.create_coupons(options['coupons'], sellers)
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Users: {len(users)}'))
        self.stdout.write(self.style.SUCCESS(f'Sellers: {len(sellers)}'))
        self.stdout.write(self.style.SUCCESS(f'Products: {len(products)}'))
        self.stdout.write(self.style.SUCCESS(f'Categories: {len(categories)}'))
        self.stdout.write(self.style.SUCCESS(f'Campaigns: {len(campaigns)}'))
        self.stdout.write(self.style.SUCCESS(f'Coupons: {len(coupons)}'))
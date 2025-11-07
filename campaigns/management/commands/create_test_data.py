from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from decimal import Decimal
import random

# Get User model
User = get_user_model()

# Import models (only what exists in your project)
try:
    from sellers.models import SellerProfile
    HAS_SELLER_PROFILE = True
except ImportError:
    HAS_SELLER_PROFILE = False

class Command(BaseCommand):
    help = 'Create dummy test data for the marketplace'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        self.stdout.write('Creating test data...')
        
        # Create users
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))
        
        # Create seller profiles and stores
        if HAS_SELLER_PROFILE:
            sellers = self.create_sellers(users[:5])  # First 5 users are sellers
            self.stdout.write(self.style.SUCCESS(f'✓ Created {len(sellers)} seller profiles with stores'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All test data created successfully!'))
        self.stdout.write('\nTest Accounts:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Buyer: buyer1 / testpass123')
        self.stdout.write('  Seller: seller1 / testpass123')

    def clear_data(self):
        """Clear existing test data"""
        if HAS_SELLER_PROFILE:
            SellerProfile.objects.all().delete()
            self.stdout.write('✓ Cleared seller profiles and stores')
        
        # Only delete non-superuser users
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('✓ Cleared existing users')

    def create_users(self):
        """Create test users"""
        # Create admin if doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@marketplace.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('  - Created admin user'))
        
        users = []
        
        # Create sellers
        seller_data = [
            ('John', 'Smith', 'seller1', 'seller1@marketplace.com'),
            ('Sarah', 'Johnson', 'seller2', 'seller2@marketplace.com'),
            ('Mike', 'Williams', 'seller3', 'seller3@marketplace.com'),
            ('Emily', 'Brown', 'seller4', 'seller4@marketplace.com'),
            ('David', 'Garcia', 'seller5', 'seller5@marketplace.com'),
        ]
        
        for first, last, username, email in seller_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                    'role': User.Role.SELLER,
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'  - Created seller: {username}')
            users.append(user)
        
        # Create buyers
        buyer_data = [
            ('Alice', 'Wilson', 'buyer1', 'buyer1@marketplace.com'),
            ('Bob', 'Martinez', 'buyer2', 'buyer2@marketplace.com'),
            ('Carol', 'Anderson', 'buyer3', 'buyer3@marketplace.com'),
            ('Dan', 'Taylor', 'buyer4', 'buyer4@marketplace.com'),
            ('Eve', 'Thomas', 'buyer5', 'buyer5@marketplace.com'),
        ]
        
        for first, last, username, email in buyer_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                    'role': User.Role.BUYER,
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'  - Created buyer: {username}')
            users.append(user)
        
        return users

    def create_sellers(self, users):
        """Create seller profiles with stores"""
        if not HAS_SELLER_PROFILE:
            return []
        
        sellers = []
        
        # Store data
        store_data = [
            {
                'name': 'TechHub Electronics',
                'description': 'Your one-stop shop for the latest electronics and gadgets. Quality products, competitive prices.',
                'business_type': 'company',
                'phone': '+1-555-0101',
            },
            {
                'name': 'Fashion Forward',
                'description': 'Trendy fashion and accessories for the modern lifestyle. Stay stylish with our curated collections.',
                'business_type': 'individual',
                'phone': '+1-555-0102',
            },
            {
                'name': 'Home & Living Store',
                'description': 'Beautiful home decor and furniture to make your house a home. Quality and style combined.',
                'business_type': 'company',
                'phone': '+1-555-0103',
            },
            {
                'name': 'Sports Zone',
                'description': 'Everything for sports enthusiasts! From equipment to apparel, we have it all.',
                'business_type': 'partnership',
                'phone': '+1-555-0104',
            },
            {
                'name': 'Book World',
                'description': 'Discover your next favorite book. Wide selection of genres, new releases, and classics.',
                'business_type': 'individual',
                'phone': '+1-555-0105',
            },
        ]
        
        for i, user in enumerate(users):
            store_info = store_data[i]
            store_slug = slugify(store_info['name'])
            
            # Create or get seller profile
            seller, created = SellerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'store_name': store_info['name'],
                    'store_slug': store_slug,
                    'description': store_info['description'],
                    'business_type': store_info['business_type'],
                    'phone': store_info['phone'],
                    'verification_status': 'verified',
                    'is_active': True,
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'total_sales': random.randint(100, 1000),
                    'total_orders': random.randint(50, 500),
                    'follower_count': random.randint(10, 200),
                    'account_health_score': random.randint(80, 100),
                    'tier': random.choice(['bronze', 'silver', 'gold']),
                    'supports_international_shipping': random.choice([True, False]),
                }
            )
            
            if created:
                self.stdout.write(f'  - Created store: {store_info["name"]}')
            
            sellers.append(seller)
        
        return sellers
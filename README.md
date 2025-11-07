# Minimalist Marketplace

A clean, minimalist Django-based marketplace with powerful features and beautiful design.

## Features

- **Multi-role Authentication**: Buyers, Sellers, and Admin roles
- **Seller KYC Verification**: Document upload and admin review system
- **Product Management**: Full CRUD operations with image uploads
- **Wishlist & Store Following**: With price drop and restock notifications
- **Campaign Management**: Flash sales and promotional campaigns
- **Admin Dashboard**: Comprehensive moderation and management tools
- **Multi-language Support**: Built-in internationalization
- **Low-bandwidth Optimization**: Reduced data mode for slower connections
- **Responsive Design**: Mobile-first minimalist design
- **SEO Optimized**: Clean URLs and meta tags

## Tech Stack

- **Backend**: Django 4.2, Python 3.8+
- **Frontend**: Tailwind CSS, Alpine.js
- **Database**: SQLite (development), PostgreSQL (production)
- **Cache**: Redis
- **Task Queue**: Celery
- **File Storage**: Local (development), AWS S3 (production)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd minimalist_marketplace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000
   - Admin panel: http://127.0.0.1:8000/admin

## Project Structure

```
minimalist_marketplace/
├── users/                    # User authentication and profiles
├── sellers/                  # Seller management and KYC
├── products/                 # Product catalog and management
├── campaigns/                # Marketing campaigns and coupons
├── notifications/            # Notification system
├── moderation/               # Admin moderation tools
├── templates/                # HTML templates
├── static/                   # CSS, JS, and images
├── requirements.txt          # Python dependencies
└── manage.py                # Django management script
```

## User Roles

### Buyers
- Browse and search products
- Add items to wishlist
- Follow stores
- Receive notifications

### Sellers
- Create and manage products
- Upload KYC documents
- View sales analytics
- Manage store profile

### Admins
- Moderate content
- Review KYC applications
- Manage campaigns
- Monitor platform health

## Configuration

### Email Settings
Configure email in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Redis Configuration
For caching and background tasks:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### File Storage
For production, configure AWS S3:
```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Use black for code formatting:
```bash
pip install black
black .
```

### Migrations
After model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

1. **Set DEBUG=False** in environment variables
2. **Configure production database** (PostgreSQL recommended)
3. **Set up Redis** for caching and Celery
4. **Configure AWS S3** for file storage
5. **Set up reverse proxy** (Nginx recommended)
6. **Use Gunicorn** as WSGI server
7. **Configure SSL certificate**

### Docker Deployment

A Dockerfile is provided for containerized deployment:
```bash
docker build -t minimalist-marketplace .
docker run -p 8000:8000 minimalist-marketplace
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

## Roadmap

- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] AI-powered recommendations
- [ ] Multi-vendor marketplace
- [ ] API development
- [ ] Progressive Web App (PWA)

---

Built with ❤️ for the minimalist community
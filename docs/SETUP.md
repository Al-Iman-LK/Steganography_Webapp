# Setup Instructions

## Prerequisites

- Python 3.9+
- PostgreSQL
- Virtual environment

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd kalinga_project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

4. Configure PostgreSQL:
```sql
CREATE DATABASE steganography_db;
CREATE USER steganography_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE steganography_db TO steganography_user;
```

5. Environment setup:
```bash
cp .env.example .env
# Edit .env with your settings
```

6. Initialize database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Development Setup

1. Install development tools:
```bash
pip install -r requirements/dev.txt
```

2. Run tests:
```bash
python manage.py test
```

## Deployment

1. Update production settings:
```bash
# Edit steganography_service/settings/production.py
```

2. Set up HTTPS:
```bash
# Configure SSL certificate
```

3. Configure static files:
```bash
python manage.py collectstatic
```

4. Set up Gunicorn and Nginx

## Maintenance

- Regular database backups
- Log rotation
- File cleanup
- Security updates

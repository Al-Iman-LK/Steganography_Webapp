# Steganography Web Service

A sophisticated web-based steganography platform using Python and Django, enabling secure information embedding across multiple digital file formats.

## Features

- Multiple file format support (PNG, JPG, MP4, MP3, PDF, DOCX)
- Secure file upload and processing
- User authentication and management
- API endpoints for integration
- Background processing
- Automatic file cleanup

## Tech Stack

- Python 3.9+
- Django 4.1
- SQLite (can be replaced by PostgreSQL for production purpose)
- Celery for background tasks
- Redis for caching
- Bootstrap for frontend

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd Steganography_Webapp
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

4. Configure database in .env:
   (if PostgreSQL is used)
```
DATABASE_URL=postgresql://user:password@localhost:5432/steganography_db
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start development server:
```bash
python manage.py runserver
```

## Documentation

- [API Documentation](docs/API.md)
- [Setup Guide](docs/SETUP.md)
- [Security](docs/SECURITY.md)

## Development

### Testing
```bash
python manage.py test
```

### Code Style
```bash
flake8
black .
```

## Security Features

- File type validation
- Size restrictions
- User authentication
- CSRF protection
- Rate limiting
- Secure file storage

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - See [LICENSE](LICENSE) for details

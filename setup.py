from setuptools import setup, find_packages

setup(
    name="steganography_service",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Django>=4.1',
        'Pillow',  # for image processing
        'python-magic',  # for file type detection
        'psycopg2-binary',  # for PostgreSQL
        'django-cleanup',  # for automatic file cleanup
        'celery',  # for background tasks
        'redis',  # for caching
        'cryptography',  # for encryption
    ],
    author="Your Name",
    description="A web-based steganography platform",
)

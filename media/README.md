# Media Directory Structure

This directory contains user-uploaded files and their processed versions.

## Directory Structure

```
media/
├── uploads/        - Original uploaded files
└── processed/      - Files after steganography processing
```

## Security Considerations

- All uploaded files are automatically renamed
- File type validation is performed
- Maximum file size limit: 10MB
- Processed files are stored separately
- Optional automatic deletion after processing

## Directory Permissions

Set the following permissions:
- Directory: 755 (drwxr-xr-x)
- Files: 644 (-rw-r--r--)

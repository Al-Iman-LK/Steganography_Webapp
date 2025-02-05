# API Documentation

## Authentication

All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

### File Operations

#### Upload File
- **URL**: `/api/files/`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - original_file: File (required)
  - file_type: string (required) [image|video|audio|document]
  - auto_delete: boolean (optional)
- **Response**: 201 Created
```json
{
    "id": 1,
    "original_file": "path/to/file",
    "file_type": "image",
    "status": "pending"
}
```

#### Process File
- **URL**: `/api/files/{id}/process/`
- **Method**: POST
- **Parameters**:
  - message: string (required)
- **Response**: 200 OK
```json
{
    "status": "success"
}
```

### User Profile

#### Get Profile
- **URL**: `/api/profile/`
- **Method**: GET
- **Response**: 200 OK
```json
{
    "username": "user",
    "email": "user@example.com",
    "total_files_processed": 10,
    "storage_used": 1024
}
```

## Error Responses

All errors follow this format:
```json
{
    "error": "Error message",
    "code": "ERROR_CODE"
}
```

## Rate Limiting

- File uploads: 10 requests per minute
- Profile access: 30 requests per minute

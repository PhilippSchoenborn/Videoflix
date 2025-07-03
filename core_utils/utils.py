"""
Shared utility functions for the Videoflix application
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email_format(email):
    """
    Validate email format using regex
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(_('Invalid email format'))
    return email


def sanitize_filename(filename):
    """
    Sanitize filename for safe storage
    """
    # Remove any characters that are not alphanumeric, dash, underscore, or dot
    sanitized = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', filename)
    
    # Ensure filename is not too long
    if len(sanitized) > 100:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:95] + ('.' + ext if ext else '')
    
    return sanitized


def format_file_size(size_bytes):
    """
    Format file size in human readable format
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"


def format_duration(duration):
    """
    Format duration timedelta to human readable string
    """
    if not duration:
        return "0:00"
    
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def generate_slug(title):
    """
    Generate URL-friendly slug from title
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = re.sub(r'[\s\-]+', '-', slug)
    slug = slug.strip('-')
    
    return slug


def truncate_text(text, max_length=100):
    """
    Truncate text to specified length with ellipsis
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def is_video_file(filename):
    """
    Check if file is a video file based on extension
    """
    video_extensions = [
        '.mp4', '.avi', '.mov', '.wmv', '.flv', 
        '.webm', '.mkv', '.m4v', '.3gp'
    ]
    
    return any(filename.lower().endswith(ext) for ext in video_extensions)


def is_image_file(filename):
    """
    Check if file is an image file based on extension
    """
    image_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
        '.tiff', '.webp', '.svg'
    ]
    
    return any(filename.lower().endswith(ext) for ext in image_extensions)


class ResponseMessages:
    """
    Standardized response messages for API
    """
    # Success messages
    SUCCESS_CREATED = "Resource created successfully"
    SUCCESS_UPDATED = "Resource updated successfully"
    SUCCESS_DELETED = "Resource deleted successfully"
    
    # Authentication messages
    AUTH_SUCCESS_LOGIN = "Login successful"
    AUTH_SUCCESS_LOGOUT = "Logout successful"
    AUTH_SUCCESS_REGISTER = "Registration successful. Please check your email for verification."
    AUTH_SUCCESS_EMAIL_VERIFIED = "Email verified successfully"
    AUTH_SUCCESS_PASSWORD_RESET = "Password reset successfully"
    
    # Error messages (generic for security)
    ERROR_INVALID_CREDENTIALS = "Please check your inputs and try again."
    ERROR_EMAIL_NOT_VERIFIED = "Please verify your email before logging in."
    ERROR_INVALID_TOKEN = "Invalid or expired token."
    ERROR_PERMISSION_DENIED = "You don't have permission to perform this action."
    ERROR_NOT_FOUND = "The requested resource was not found."
    ERROR_VALIDATION = "Please check your inputs and try again."
    
    # Video specific messages
    VIDEO_UPLOAD_SUCCESS = "Video uploaded successfully. Processing will begin shortly."
    VIDEO_PROCESSING_COMPLETE = "Video processing completed successfully."
    VIDEO_PROCESSING_FAILED = "Video processing failed. Please try again."


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

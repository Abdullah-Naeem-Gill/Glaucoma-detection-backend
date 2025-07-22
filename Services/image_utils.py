import base64
import re
from typing import Optional, Tuple


def validate_image_data(image_data: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if the provided string is a valid base64 encoded image
    Returns: (is_valid, error_message)
    """
    if not image_data:
        return True, None

    # Check if it's a valid base64 string
    try:
        # Remove data URL prefix if present
        if image_data.startswith('data:image/'):
            # Extract the base64 part after the comma
            image_data = image_data.split(',', 1)[1]

        # Decode base64 to check if it's valid
        decoded_data = base64.b64decode(image_data)

        # Check file size (limit to 5MB)
        if len(decoded_data) > 5 * 1024 * 1024:
            return False, "Image size too large. Maximum size is 5MB."

        # Check if it's a valid image by looking at the first few bytes
        if len(decoded_data) < 4:
            return False, "Invalid image data"

        # Check for common image file signatures
        signatures = {
            b'\xff\xd8\xff': 'JPEG',
            b'\x89PNG\r\n\x1a\n': 'PNG',
            b'GIF87a': 'GIF',
            b'GIF89a': 'GIF',
            b'RIFF': 'WEBP'
        }

        is_valid_image = False
        for signature, format_name in signatures.items():
            if decoded_data.startswith(signature):
                is_valid_image = True
                break

        if not is_valid_image:
            return False, "Invalid image format. Supported formats: JPEG, PNG, GIF, WEBP"

        return True, None

    except Exception as e:
        return False, f"Invalid base64 data: {str(e)}"


def clean_image_data(image_data: str) -> str:
    """
    Clean image data by removing data URL prefix if present
    """
    if image_data and image_data.startswith('data:image/'):
        return image_data.split(',', 1)[1]
    return image_data


def get_image_format(image_data: str) -> Optional[str]:
    """
    Get the format of the image from base64 data
    """
    if not image_data:
        return None

    try:
        # Remove data URL prefix if present
        clean_data = clean_image_data(image_data)
        decoded_data = base64.b64decode(clean_data)

        # Check for common image file signatures
        if decoded_data.startswith(b'\xff\xd8\xff'):
            return 'JPEG'
        elif decoded_data.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'PNG'
        elif decoded_data.startswith(b'GIF87a') or decoded_data.startswith(b'GIF89a'):
            return 'GIF'
        elif decoded_data.startswith(b'RIFF'):
            return 'WEBP'

        return None
    except:
        return None

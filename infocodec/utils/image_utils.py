"""
Image utility functions
"""

import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Tuple


def load_image(filepath: str) -> np.ndarray:
    """
    Load image from file preserving color channels.

    Args:
        filepath: Path to image file

    Returns:
        Image as numpy array: (H, W) for grayscale or (H, W, 3) for RGB, dtype uint8.
    """
    img = Image.open(filepath)

    if img.mode == 'L':
        return np.array(img, dtype=np.uint8)

    # Normalise to RGB (handles RGBA, P, CMYK, etc.)
    img = img.convert('RGB')
    return np.array(img, dtype=np.uint8)


def save_image(array: np.ndarray, filepath: str):
    """
    Save numpy array as image file.

    Args:
        array: Image array — (H, W) for grayscale or (H, W, 3) for RGB.
        filepath: Output path
    """
    if array.dtype != np.uint8:
        array = array.astype(np.uint8)

    if array.ndim == 2:
        img = Image.fromarray(array, mode='L')
    elif array.ndim == 3 and array.shape[2] == 3:
        img = Image.fromarray(array, mode='RGB')
    else:
        # Fallback: squeeze extra dims and save as grayscale
        img = Image.fromarray(array.squeeze(), mode='L')

    img.save(filepath)


def detect_media_type(filepath: str) -> str:
    """
    Detect media type from file extension.
    
    Args:
        filepath: Path to file
        
    Returns:
        Media type: 'image', 'audio', 'text', or 'unknown'
    """
    ext = Path(filepath).suffix.lower()
    
    image_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp'}
    audio_exts = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}
    text_exts = {'.txt', '.md', '.rst', '.json', '.xml', '.html'}
    
    if ext in image_exts:
        return 'image'
    elif ext in audio_exts:
        return 'audio'
    elif ext in text_exts:
        return 'text'
    else:
        return 'unknown'


def create_test_image(size: Tuple[int, int] = (64, 64), pattern: str = 'gradient') -> np.ndarray:
    """
    Create test image with different patterns.
    
    Args:
        size: (height, width)
        pattern: 'gradient', 'blocks', 'noise', or 'checkerboard'
        
    Returns:
        Test image array
    """
    height, width = size
    
    if pattern == 'gradient':
        x = np.linspace(0, 255, width)
        y = np.linspace(0, 255, height)
        X, Y = np.meshgrid(x, y)
        image = ((X + Y) / 2).astype(np.uint8)
    
    elif pattern == 'blocks':
        image = np.zeros(size, dtype=np.uint8)
        block_size = 8
        for i in range(0, height, block_size):
            for j in range(0, width, block_size):
                value = np.random.randint(0, 256)
                image[i:i+block_size, j:j+block_size] = value
    
    elif pattern == 'noise':
        image = np.random.randint(0, 256, size, dtype=np.uint8)
    
    elif pattern == 'checkerboard':
        image = np.zeros(size, dtype=np.uint8)
        image[::2, ::2] = 255
        image[1::2, 1::2] = 255
    
    else:
        raise ValueError(f"Unknown pattern: {pattern}")
    
    return image


def get_image_info(array: np.ndarray) -> dict:
    """
    Get information about image array.
    
    Args:
        array: Image array
        
    Returns:
        Dictionary with image information
    """
    return {
        'shape': array.shape,
        'dtype': str(array.dtype),
        'size_bytes': array.nbytes,
        'min': int(np.min(array)),
        'max': int(np.max(array)),
        'mean': float(np.mean(array)),
        'unique_values': int(len(np.unique(array))),
    }

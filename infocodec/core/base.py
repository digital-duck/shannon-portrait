"""
Base classes for compressors and reconstructors.

Designed to be media-type agnostic for future extension to audio and text.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
import numpy as np


class Compressor(ABC):
    """
    Abstract base class for compression algorithms.
    
    Subclass this for image, audio, or text compression methods.
    """
    
    def __init__(self, **kwargs):
        """Initialize compressor with optional parameters"""
        self.params = kwargs
        self.stats = {}
    
    @abstractmethod
    def compress(self, data: Any) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress input data to bytes.
        
        Args:
            data: Input data (image array, audio samples, text string, etc.)
            
        Returns:
            compressed_bytes: Compressed data as bytes
            metadata: Dictionary with compression metadata (dimensions, method, etc.)
        """
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """
        Get compression statistics.
        
        Returns:
            Dictionary with stats like compression_ratio, entropy, etc.
        """
        pass
    
    @property
    def name(self) -> str:
        """Return the name of this compression method"""
        return self.__class__.__name__


class Reconstructor(ABC):
    """
    Abstract base class for reconstruction algorithms.
    
    Subclass this for image, audio, or text reconstruction methods.
    """
    
    def __init__(self, **kwargs):
        """Initialize reconstructor with optional parameters"""
        self.params = kwargs
        self.stats = {}
    
    @abstractmethod
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> Any:
        """
        Reconstruct data from compressed bytes.
        
        Args:
            compressed_bytes: Compressed data
            metadata: Metadata from compression (dimensions, method, etc.)
            
        Returns:
            Reconstructed data (image array, audio samples, text string, etc.)
        """
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """
        Get reconstruction statistics.
        
        Returns:
            Dictionary with stats like reconstruction_time, quality_loss, etc.
        """
        pass
    
    @property
    def name(self) -> str:
        """Return the name of this reconstruction method"""
        return self.__class__.__name__


class ImageCompressor(Compressor):
    """
    Base class for image compression algorithms.
    
    Handles common image operations.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_shape = None
        self.original_dtype = None
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image before compression"""
        self.original_shape = image.shape
        self.original_dtype = image.dtype
        
        # Ensure grayscale
        if len(image.shape) == 3:
            # Convert to grayscale if color
            image = np.dot(image[...,:3], [0.299, 0.587, 0.114])
        
        return image.astype(np.uint8)
    
    def _create_metadata(self) -> Dict[str, Any]:
        """Create metadata dictionary for reconstruction"""
        return {
            'shape': self.original_shape,
            'dtype': str(self.original_dtype),
            'method': self.name,
        }


class ImageReconstructor(Reconstructor):
    """
    Base class for image reconstruction algorithms.
    
    Handles common image operations.
    """
    
    def _postprocess_image(self, image: np.ndarray, metadata: Dict[str, Any]) -> np.ndarray:
        """Postprocess image after reconstruction"""
        target_shape = metadata.get('shape')
        
        # Reshape if needed
        if target_shape and image.shape != target_shape:
            if len(target_shape) == 2:
                image = image.reshape(target_shape)
            elif len(target_shape) == 3 and image.ndim == 2:
                # Expand grayscale to RGB if original was color
                image = np.stack([image] * 3, axis=-1)
        
        return image


# Future: Audio and Text base classes
class AudioCompressor(Compressor):
    """Base class for audio compression (future implementation)"""
    pass


class AudioReconstructor(Reconstructor):
    """Base class for audio reconstruction (future implementation)"""
    pass


class TextCompressor(Compressor):
    """Base class for text compression (future implementation)"""
    pass


class TextReconstructor(Reconstructor):
    """Base class for text reconstruction (future implementation)"""
    pass

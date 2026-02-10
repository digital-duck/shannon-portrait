"""
Naive Compressor - Baseline method

Simple serialization with no compression.
8 bits per pixel, row-by-row flattening.
"""

import numpy as np
from typing import Dict, Any, Tuple
import struct
from infocodec.core.base import ImageCompressor
from infocodec.core.metrics import calculate_entropy


class NaiveCompressor(ImageCompressor):
    """
    Naive compression: simple flattening with no optimization.
    
    This is the baseline for comparison.
    """
    
    def compress(self, data: np.ndarray) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress image by simple flattening.
        
        Args:
            data: Input image array
            
        Returns:
            compressed_bytes: Flattened image as bytes
            metadata: Image dimensions and stats
        """
        # Preprocess
        image = self._preprocess_image(data)
        
        # Flatten
        flat_data = image.flatten()
        
        # Convert to bytes
        compressed_bytes = flat_data.tobytes()
        
        # Calculate stats
        self.stats = {
            'method': 'Naive',
            'original_pixels': image.size,
            'compressed_bytes': len(compressed_bytes),
            'bits_per_pixel': 8,
            'entropy': calculate_entropy(image),
            'compression_ratio': 1.0,
        }
        
        # Metadata
        metadata = self._create_metadata()
        metadata.update({
            'original_shape': image.shape,
        })
        
        return compressed_bytes, metadata
    
    def get_stats(self) -> Dict[str, Any]:
        """Return compression statistics"""
        return self.stats

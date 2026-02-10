"""
RLE (Run-Length Encoding) Compressor

Encodes consecutive identical values as (value, count) pairs.
Excellent for images with large uniform regions (logos, diagrams).
"""

import numpy as np
from typing import Dict, Any, Tuple
import struct
from infocodec.core.base import ImageCompressor
from infocodec.core.metrics import calculate_entropy


class RLECompressor(ImageCompressor):
    """
    Run-Length Encoding compression.
    
    Best for: Images with large uniform regions (blocks, logos)
    Compression: 4-10x for block patterns, 0.5x for noise (expansion!)
    Type: Lossless
    """
    
    def compress(self, data: np.ndarray) -> Tuple[bytes, Dict[str, Any]]:
        """
        Compress image using Run-Length Encoding.
        
        Args:
            data: Input image array
            
        Returns:
            compressed_bytes: RLE encoded data
            metadata: Image dimensions and stats
        """
        # Preprocess
        image = self._preprocess_image(data)
        
        # Flatten
        flat_data = image.flatten()
        
        # Perform RLE
        rle_encoded = []
        if len(flat_data) == 0:
            compressed_bytes = b''
        else:
            current_val = flat_data[0]
            count = 1
            
            for val in flat_data[1:]:
                if val == current_val and count < 255:
                    count += 1
                else:
                    rle_encoded.extend([current_val, count])
                    current_val = val
                    count = 1
            
            # Don't forget the last run
            rle_encoded.extend([current_val, count])
            
            # Convert to bytes
            compressed_bytes = bytes(rle_encoded)
        
        # Calculate stats
        original_size = len(flat_data)
        compressed_size = len(compressed_bytes)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else float('inf')
        
        self.stats = {
            'method': 'RLE',
            'original_pixels': original_size,
            'compressed_bytes': compressed_size,
            'rle_pairs': len(rle_encoded) // 2,
            'compression_ratio': compression_ratio,
            'space_saved_percent': ((original_size - compressed_size) / original_size * 100) 
                                   if original_size > 0 else 0,
            'entropy': calculate_entropy(image),
        }
        
        # Metadata
        metadata = self._create_metadata()
        metadata.update({
            'original_shape': image.shape,
            'rle_pairs': len(rle_encoded) // 2,
        })
        
        return compressed_bytes, metadata
    
    def get_stats(self) -> Dict[str, Any]:
        """Return compression statistics"""
        return self.stats

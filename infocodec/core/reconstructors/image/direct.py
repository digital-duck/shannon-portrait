"""
Direct Reconstructor

Simple reconstruction for naive and other straightforward compressions.
Just reshapes the data back to 2D.
"""

import numpy as np
from typing import Dict, Any
from infocodec.core.base import ImageReconstructor


class DirectReconstructor(ImageReconstructor):
    """
    Direct reconstruction - simple reshape.
    
    Use for: Naive compression, perfect channel
    Quality: Perfect (lossless)
    """
    
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct image by direct reshape.
        
        Args:
            compressed_bytes: Compressed data
            metadata: Metadata with shape information
            
        Returns:
            Reconstructed image array
        """
        shape = metadata.get('original_shape', metadata.get('shape'))
        
        # Convert bytes back to array
        flat_data = np.frombuffer(compressed_bytes, dtype=np.uint8)
        
        # Reshape
        if isinstance(shape, (list, tuple)) and len(shape) >= 2:
            expected_size = int(np.prod(shape))

            if len(flat_data) < expected_size:
                flat_data = np.pad(flat_data, (0, expected_size - len(flat_data)),
                                  mode='edge')
            elif len(flat_data) > expected_size:
                flat_data = flat_data[:expected_size]

            reconstructed = flat_data.reshape(shape)
        else:
            reconstructed = flat_data
        
        # Postprocess
        reconstructed = self._postprocess_image(reconstructed, metadata)
        
        self.stats = {
            'method': 'Direct',
            'reconstructed_pixels': reconstructed.size,
            'quality': 'Perfect' if metadata.get('method') == 'Naive' else 'Depends on compression',
        }
        
        return reconstructed
    
    def get_stats(self) -> Dict[str, Any]:
        """Return reconstruction statistics"""
        return self.stats

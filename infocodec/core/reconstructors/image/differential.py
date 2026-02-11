"""
Differential Reconstructor

Integrates differential encoding back to absolute pixel values.
"""

import numpy as np
from typing import Dict, Any
from infocodec.core.base import ImageReconstructor


class DifferentialReconstructor(ImageReconstructor):
    """
    Differential encoding reconstruction.
    
    Uses cumulative sum to integrate differences back to absolute values.
    """
    
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct image from differentially encoded data.
        
        Args:
            compressed_bytes: Differentially encoded data
            metadata: Metadata with shape information
            
        Returns:
            Reconstructed image array
        """
        shape = metadata.get('original_shape', metadata.get('shape'))
        
        # Convert bytes to int16 array (differences are signed)
        diff_data = np.frombuffer(compressed_bytes, dtype=np.int16)
        
        # Integrate using cumulative sum
        reconstructed_flat = np.cumsum(diff_data).astype(np.uint8)
        
        # Handle size and reshape
        if isinstance(shape, (list, tuple)) and len(shape) >= 2:
            expected_size = int(np.prod(shape))

            if len(reconstructed_flat) < expected_size:
                reconstructed_flat = np.pad(reconstructed_flat,
                                           (0, expected_size - len(reconstructed_flat)),
                                           mode='edge')
            elif len(reconstructed_flat) > expected_size:
                reconstructed_flat = reconstructed_flat[:expected_size]

            reconstructed = reconstructed_flat.reshape(shape)
        else:
            reconstructed = reconstructed_flat
        
        # Postprocess
        reconstructed = self._postprocess_image(reconstructed, metadata)
        
        self.stats = {
            'method': 'Differential Decode',
            'differences_integrated': len(diff_data),
            'quality': 'Perfect (Lossless)',
        }
        
        return reconstructed
    
    def get_stats(self) -> Dict[str, Any]:
        """Return reconstruction statistics"""
        return self.stats

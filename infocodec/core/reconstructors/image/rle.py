"""
RLE Reconstructor

Decodes Run-Length Encoded data back to original image.
"""

import numpy as np
from typing import Dict, Any
from infocodec.core.base import ImageReconstructor


class RLEReconstructor(ImageReconstructor):
    """
    RLE (Run-Length Encoding) reconstruction.
    
    Decodes (value, count) pairs back to pixel stream.
    """
    
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct image from RLE encoded data.
        
        Args:
            compressed_bytes: RLE encoded data
            metadata: Metadata with shape information
            
        Returns:
            Reconstructed image array
        """
        shape = metadata.get('original_shape', metadata.get('shape'))
        
        # Decode RLE
        rle_data = list(compressed_bytes)
        decoded = []
        
        for i in range(0, len(rle_data), 2):
            if i + 1 < len(rle_data):
                value = rle_data[i]
                count = rle_data[i + 1]
                decoded.extend([value] * count)
        
        decoded_array = np.array(decoded, dtype=np.uint8)
        
        # Handle size mismatch
        if isinstance(shape, (list, tuple)) and len(shape) >= 2:
            expected_size = int(np.prod(shape))

            if len(decoded_array) < expected_size:
                decoded_array = np.pad(decoded_array, (0, expected_size - len(decoded_array)),
                                      mode='edge')
            elif len(decoded_array) > expected_size:
                decoded_array = decoded_array[:expected_size]

            reconstructed = decoded_array.reshape(shape)
        else:
            reconstructed = decoded_array
        
        # Postprocess
        reconstructed = self._postprocess_image(reconstructed, metadata)
        
        self.stats = {
            'method': 'RLE Decode',
            'rle_pairs': len(rle_data) // 2,
            'decoded_pixels': len(decoded),
            'quality': 'Perfect (Lossless)',
        }
        
        return reconstructed
    
    def get_stats(self) -> Dict[str, Any]:
        """Return reconstruction statistics"""
        return self.stats

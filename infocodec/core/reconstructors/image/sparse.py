"""
Sparse Reconstructor

Reconstructs full image from sparse samples using interpolation.
"""

import numpy as np
from typing import Dict, Any
import struct
from infocodec.core.base import ImageReconstructor


class SparseReconstructor(ImageReconstructor):
    """
    Sparse sampling reconstruction.
    
    Uses bilinear interpolation to fill missing pixels from sparse samples.
    """
    
    def reconstruct(self, compressed_bytes: bytes, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct image from sparse samples.
        
        Args:
            compressed_bytes: Sparse sampled pixels with positions
            metadata: Metadata with shape and sampling info
            
        Returns:
            Reconstructed image array (lossy - interpolated)
        """
        shape = metadata.get('original_shape', metadata.get('shape'))
        
        if not isinstance(shape, (list, tuple)) or len(shape) < 2:
            return np.zeros((1, 1), dtype=np.uint8)
        
        height, width = shape[0], shape[1]
        
        # Parse compressed data
        if len(compressed_bytes) < 4:
            return np.zeros((height, width), dtype=np.uint8)
        
        num_samples = struct.unpack('>I', compressed_bytes[:4])[0]
        
        # Extract samples
        known_pixels = {}
        offset = 4
        
        for _ in range(num_samples):
            if offset + 5 > len(compressed_bytes):
                break
            
            row, col, pixel = struct.unpack('>HHB', compressed_bytes[offset:offset+5])
            if row < height and col < width:
                known_pixels[(row, col)] = pixel
            offset += 5
        
        # Reconstruct using bilinear interpolation
        try:
            from scipy.interpolate import griddata
            
            if known_pixels:
                # Known points and values
                points = np.array(list(known_pixels.keys()))
                values = np.array(list(known_pixels.values()))
                
                # Grid to interpolate
                grid_y, grid_x = np.mgrid[0:height, 0:width]
                
                # Interpolate
                reconstructed = griddata(points, values, (grid_y, grid_x),
                                        method='linear', fill_value=128)
                reconstructed = reconstructed.astype(np.uint8)
            else:
                reconstructed = np.full((height, width), 128, dtype=np.uint8)
        
        except ImportError:
            # Fallback: nearest neighbor interpolation
            reconstructed = np.full((height, width), 128, dtype=np.uint8)
            
            for (row, col), pixel in known_pixels.items():
                reconstructed[row, col] = pixel
            
            # Simple nearest neighbor fill
            for i in range(height):
                for j in range(width):
                    if (i, j) not in known_pixels:
                        # Find nearest known pixel
                        min_dist = float('inf')
                        nearest_val = 128
                        
                        for (kr, kc), val in known_pixels.items():
                            dist = abs(i - kr) + abs(j - kc)
                            if dist < min_dist:
                                min_dist = dist
                                nearest_val = val
                        
                        reconstructed[i, j] = nearest_val
        
        # Postprocess
        reconstructed = self._postprocess_image(reconstructed, metadata)
        
        self.stats = {
            'method': 'Sparse Reconstruction',
            'known_pixels': len(known_pixels),
            'total_pixels': height * width,
            'sparsity': len(known_pixels) / (height * width) if height * width > 0 else 0,
            'quality': 'Lossy (Interpolated)',
        }
        
        return reconstructed
    
    def get_stats(self) -> Dict[str, Any]:
        """Return reconstruction statistics"""
        return self.stats

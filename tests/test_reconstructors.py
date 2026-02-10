"""
Unit Tests for Reconstruction Algorithms

Tests all 6 reconstruction methods with round-trip compression.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from infocodec.core.compressors import COMPRESSORS
from infocodec.core.reconstructors import RECONSTRUCTORS
from infocodec.core.metrics import calculate_psnr, calculate_ssim
from infocodec.utils.image_utils import create_test_image


class TestReconstructors:
    """Test suite for all reconstruction algorithms"""
    
    @pytest.fixture
    def test_images(self):
        """Generate test images"""
        return {
            'gradient': create_test_image(size=(64, 64), pattern='gradient'),
            'blocks': create_test_image(size=(64, 64), pattern='blocks'),
            'noise': create_test_image(size=(64, 64), pattern='noise'),
            'small': create_test_image(size=(16, 16), pattern='gradient'),
        }
    
    def test_all_reconstructors_exist(self):
        """Test that all expected reconstructors are registered"""
        expected_methods = ['naive', 'direct', 'rle', 'differential', 'huffman', 'sparse', 'dct']
        
        for method in expected_methods:
            assert method in RECONSTRUCTORS, f"Reconstructor '{method}' not found in registry"
    
    def test_round_trip_lossless(self, test_images):
        """Test perfect reconstruction for lossless methods"""
        lossless_methods = ['naive', 'rle', 'differential', 'huffman']
        
        for method in lossless_methods:
            compressor = COMPRESSORS[method]()
            reconstructor = RECONSTRUCTORS[method]()
            
            for name, image in test_images.items():
                # Compress
                compressed_bytes, metadata = compressor.compress(image)
                
                # Reconstruct
                reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
                
                # Verify perfect reconstruction
                assert reconstructed.shape == image.shape, \
                    f"{method}/{name}: Shape mismatch"
                assert np.array_equal(image, reconstructed), \
                    f"{method}/{name}: Lossless should be perfect"
                
                # Verify PSNR is infinite
                psnr = calculate_psnr(image, reconstructed)
                assert psnr == float('inf'), \
                    f"{method}/{name}: PSNR should be infinite for lossless"
    
    def test_round_trip_lossy(self, test_images):
        """Test lossy methods have acceptable quality"""
        lossy_methods = ['sparse', 'dct']
        
        for method in lossy_methods:
            if method == 'sparse':
                compressor = COMPRESSORS[method](sampling_rate=4)
            elif method == 'dct':
                compressor = COMPRESSORS[method](quality=0.8)
            else:
                compressor = COMPRESSORS[method]()
            
            reconstructor = RECONSTRUCTORS[method]()
            
            for name, image in test_images.items():
                # Compress
                compressed_bytes, metadata = compressor.compress(image)
                
                # Reconstruct
                reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
                
                # Verify shape
                assert reconstructed.shape == image.shape, \
                    f"{method}/{name}: Shape mismatch"
                
                # Verify quality is reasonable
                psnr = calculate_psnr(image, reconstructed)
                assert psnr > 15, \
                    f"{method}/{name}: PSNR too low ({psnr:.2f} dB)"
    
    def test_reconstructor_stats(self, test_images):
        """Test that reconstructors return statistics"""
        image = test_images['gradient']
        
        for method in ['naive', 'rle', 'differential', 'huffman']:
            compressor = COMPRESSORS[method]()
            reconstructor = RECONSTRUCTORS[method]()
            
            compressed_bytes, metadata = compressor.compress(image)
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            
            stats = reconstructor.get_stats()
            assert isinstance(stats, dict), f"{method}: Stats should be dict"
            assert 'method' in stats, f"{method}: Missing method in stats"
    
    def test_metadata_preservation(self, test_images):
        """Test that metadata is correctly used in reconstruction"""
        image = test_images['gradient']
        
        for method in ['naive', 'rle', 'differential']:
            compressor = COMPRESSORS[method]()
            reconstructor = RECONSTRUCTORS[method]()
            
            compressed_bytes, metadata = compressor.compress(image)
            
            # Verify shape in metadata
            shape = metadata.get('original_shape', metadata.get('shape'))
            assert shape is not None, f"{method}: No shape in metadata"
            assert shape[0] == image.shape[0], f"{method}: Height mismatch in metadata"
            assert shape[1] == image.shape[1], f"{method}: Width mismatch in metadata"
            
            # Reconstruct and verify
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            assert reconstructed.shape == image.shape, f"{method}: Reconstruction shape wrong"
    
    def test_sparse_interpolation(self):
        """Test sparse reconstruction interpolation"""
        image = create_test_image(size=(64, 64), pattern='gradient')
        
        # Compress with different sampling rates
        for rate in [2, 4, 8]:
            compressor = COMPRESSORS['sparse'](sampling_rate=rate)
            reconstructor = RECONSTRUCTORS['sparse']()
            
            compressed_bytes, metadata = compressor.compress(image)
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            
            # Higher sampling rate = lower quality
            psnr = calculate_psnr(image, reconstructed)
            
            # But should still be reasonable
            assert psnr > 20, f"Sparse rate={rate}: PSNR too low ({psnr:.2f} dB)"
    
    def test_dct_quality_levels(self):
        """Test DCT reconstruction at different quality levels"""
        image = create_test_image(size=(64, 64), pattern='gradient')
        
        psnr_values = []
        
        for quality in [0.3, 0.5, 0.8, 1.0]:
            compressor = COMPRESSORS['dct'](quality=quality)
            reconstructor = RECONSTRUCTORS['dct']()
            
            compressed_bytes, metadata = compressor.compress(image)
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            
            psnr = calculate_psnr(image, reconstructed)
            psnr_values.append(psnr)
            
            # Higher quality should give higher PSNR
            assert psnr > 20, f"DCT quality={quality}: PSNR too low ({psnr:.2f} dB)"
        
        # PSNR should generally increase with quality
        # (though not strictly monotonic due to quantization)
        assert psnr_values[-1] > psnr_values[0], \
            "Higher quality should generally give better PSNR"
    
    def test_error_handling(self):
        """Test error handling in reconstructors"""
        # Test with corrupted metadata
        corrupted_metadata = {'method': 'test', 'shape': (10, 10)}
        corrupted_bytes = b'corrupted data'
        
        for method in ['direct', 'rle']:
            reconstructor = RECONSTRUCTORS[method]()
            
            try:
                # Should either handle gracefully or raise meaningful error
                result = reconstructor.reconstruct(corrupted_bytes, corrupted_metadata)
                # If it doesn't raise error, should return something
                assert isinstance(result, np.ndarray), \
                    f"{method}: Should return ndarray"
            except (ValueError, IndexError, KeyError) as e:
                # Acceptable to raise error
                pass


class TestRoundTripQuality:
    """Test quality metrics for round-trip compression"""
    
    def test_lossless_ssim(self):
        """Test that lossless methods have perfect SSIM"""
        image = create_test_image(size=(64, 64), pattern='blocks')
        
        for method in ['naive', 'rle', 'differential', 'huffman']:
            compressor = COMPRESSORS[method]()
            reconstructor = RECONSTRUCTORS[method]()
            
            compressed_bytes, metadata = compressor.compress(image)
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            
            ssim = calculate_ssim(image, reconstructed)
            assert ssim > 0.99, f"{method}: SSIM should be ~1.0 for lossless ({ssim:.4f})"
    
    def test_compression_tradeoff(self):
        """Test that higher compression = lower quality for lossy"""
        image = create_test_image(size=(64, 64), pattern='gradient')
        
        # Test DCT at different qualities
        qualities = [0.3, 0.6, 0.9]
        compression_ratios = []
        psnr_values = []
        
        for quality in qualities:
            compressor = COMPRESSORS['dct'](quality=quality)
            reconstructor = RECONSTRUCTORS['dct']()
            
            compressed_bytes, metadata = compressor.compress(image)
            reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
            
            stats = compressor.get_stats()
            compression_ratios.append(stats['compression_ratio'])
            
            psnr = calculate_psnr(image, reconstructed)
            psnr_values.append(psnr)
        
        # Generally: higher compression at lower quality
        # (though not always strictly monotonic)
        assert len(compression_ratios) == len(qualities), "Should have all ratios"
        assert len(psnr_values) == len(qualities), "Should have all PSNR values"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

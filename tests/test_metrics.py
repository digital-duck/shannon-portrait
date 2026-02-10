"""
Unit Tests for Metrics Module

Tests Shannon entropy, PSNR, SSIM, and other metrics.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from infocodec.core.metrics import (
    calculate_entropy,
    calculate_psnr,
    calculate_ssim,
    calculate_mse,
    calculate_compression_ratio,
    calculate_bits_per_pixel,
    comprehensive_quality_analysis,
)


class TestEntropyCalculation:
    """Test Shannon entropy calculations"""
    
    def test_entropy_uniform(self):
        """Test entropy of uniform distribution (all same value)"""
        uniform = np.full((64, 64), 128, dtype=np.uint8)
        entropy = calculate_entropy(uniform)
        
        # Entropy should be 0 for uniform distribution
        assert entropy < 0.01, f"Uniform entropy should be ~0, got {entropy}"
    
    def test_entropy_binary(self):
        """Test entropy of binary distribution"""
        # 50-50 split between 0 and 255
        binary = np.array([0, 255] * 2048, dtype=np.uint8)
        entropy = calculate_entropy(binary)
        
        # Should be close to 1 bit
        assert 0.9 < entropy < 1.1, f"Binary entropy should be ~1, got {entropy}"
    
    def test_entropy_random(self):
        """Test entropy of random distribution"""
        np.random.seed(42)
        random = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        entropy = calculate_entropy(random)
        
        # Should be close to 8 bits (maximum for 8-bit data)
        assert 7.0 < entropy <= 8.0, f"Random entropy should be ~8, got {entropy}"
    
    def test_entropy_bounds(self):
        """Test that entropy is always within valid bounds"""
        test_cases = [
            np.full((10, 10), 0, dtype=np.uint8),  # All zeros
            np.arange(256, dtype=np.uint8).reshape(16, 16),  # All values
            np.random.randint(0, 256, size=(32, 32), dtype=np.uint8),  # Random
        ]
        
        for data in test_cases:
            entropy = calculate_entropy(data)
            assert 0 <= entropy <= 8, f"Entropy {entropy} outside bounds [0, 8]"


class TestQualityMetrics:
    """Test quality metrics (PSNR, SSIM, MSE)"""
    
    def test_psnr_identical(self):
        """Test PSNR of identical images"""
        image = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        psnr = calculate_psnr(image, image)
        
        assert psnr == float('inf'), "Identical images should have infinite PSNR"
    
    def test_psnr_different(self):
        """Test PSNR of different images"""
        image1 = np.zeros((64, 64), dtype=np.uint8)
        image2 = np.full((64, 64), 255, dtype=np.uint8)
        
        psnr = calculate_psnr(image1, image2)
        
        # Should be finite and relatively low
        assert psnr != float('inf'), "Different images should have finite PSNR"
        assert psnr < 50, "Completely different images should have low PSNR"
    
    def test_psnr_properties(self):
        """Test PSNR mathematical properties"""
        original = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        
        # Small noise
        small_noise = original + np.random.randint(-5, 5, size=original.shape)
        small_noise = np.clip(small_noise, 0, 255).astype(np.uint8)
        psnr_small = calculate_psnr(original, small_noise)
        
        # Large noise
        large_noise = original + np.random.randint(-50, 50, size=original.shape)
        large_noise = np.clip(large_noise, 0, 255).astype(np.uint8)
        psnr_large = calculate_psnr(original, large_noise)
        
        # Smaller noise should give higher PSNR
        assert psnr_small > psnr_large, "Smaller noise should give higher PSNR"
    
    def test_ssim_identical(self):
        """Test SSIM of identical images"""
        image = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        ssim = calculate_ssim(image, image)
        
        assert 0.99 < ssim <= 1.0, f"Identical images should have SSIM ~1.0, got {ssim}"
    
    def test_ssim_bounds(self):
        """Test that SSIM is within valid bounds"""
        image1 = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        image2 = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        
        ssim = calculate_ssim(image1, image2)
        
        assert 0 <= ssim <= 1.0, f"SSIM {ssim} outside bounds [0, 1]"
    
    def test_mse_identical(self):
        """Test MSE of identical images"""
        image = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        mse = calculate_mse(image, image)
        
        assert mse == 0.0, "Identical images should have MSE = 0"
    
    def test_mse_maximum(self):
        """Test MSE of maximally different images"""
        image1 = np.zeros((64, 64), dtype=np.uint8)
        image2 = np.full((64, 64), 255, dtype=np.uint8)
        
        mse = calculate_mse(image1, image2)
        
        # MSE should be 255^2 = 65025
        assert abs(mse - 255**2) < 0.1, f"Max MSE should be ~65025, got {mse}"


class TestCompressionMetrics:
    """Test compression-related metrics"""
    
    def test_compression_ratio(self):
        """Test compression ratio calculation"""
        original_size = 4096
        compressed_size = 1024
        
        ratio = calculate_compression_ratio(original_size, compressed_size)
        
        assert ratio == 4.0, f"Ratio should be 4.0, got {ratio}"
    
    def test_compression_ratio_no_compression(self):
        """Test compression ratio when no compression"""
        size = 4096
        ratio = calculate_compression_ratio(size, size)
        
        assert ratio == 1.0, "No compression should give 1.0x ratio"
    
    def test_compression_ratio_expansion(self):
        """Test compression ratio for expansion"""
        original_size = 1024
        compressed_size = 2048
        
        ratio = calculate_compression_ratio(original_size, compressed_size)
        
        assert ratio == 0.5, f"Expansion should give <1.0x ratio, got {ratio}"
    
    def test_bits_per_pixel(self):
        """Test bits per pixel calculation"""
        total_bits = 32768
        num_pixels = 4096
        
        bpp = calculate_bits_per_pixel(total_bits, num_pixels)
        
        assert bpp == 8.0, f"Should be 8 BPP, got {bpp}"
    
    def test_bits_per_pixel_compressed(self):
        """Test BPP for compressed data"""
        total_bits = 16384
        num_pixels = 4096
        
        bpp = calculate_bits_per_pixel(total_bits, num_pixels)
        
        assert bpp == 4.0, f"Should be 4 BPP, got {bpp}"


class TestComprehensiveAnalysis:
    """Test comprehensive quality analysis function"""
    
    def test_comprehensive_analysis_lossless(self):
        """Test comprehensive analysis for lossless compression"""
        original = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        reconstructed = original.copy()
        
        original_size = original.size * 1
        compressed_size = original.size * 1 // 2  # Assume 2x compression
        
        analysis = comprehensive_quality_analysis(
            original, reconstructed, original_size, compressed_size
        )
        
        # Check that all expected keys are present
        expected_keys = [
            'original_entropy', 'reconstructed_entropy',
            'psnr_db', 'ssim', 'mse',
            'compression_ratio', 'bits_per_pixel',
            'efficiency_percent', 'theoretical_min_bits'
        ]
        
        for key in expected_keys:
            assert key in analysis, f"Missing key: {key}"
        
        # For lossless, PSNR should be infinite
        assert analysis['psnr_db'] == float('inf'), "Lossless should have infinite PSNR"
        assert analysis['mse'] == 0.0, "Lossless should have MSE = 0"
    
    def test_comprehensive_analysis_lossy(self):
        """Test comprehensive analysis for lossy compression"""
        np.random.seed(42)
        original = np.random.randint(0, 256, size=(64, 64), dtype=np.uint8)
        
        # Add some noise to simulate lossy compression
        reconstructed = original + np.random.randint(-10, 10, size=original.shape)
        reconstructed = np.clip(reconstructed, 0, 255).astype(np.uint8)
        
        original_size = original.size * 1
        compressed_size = original.size * 1 // 4  # Assume 4x compression
        
        analysis = comprehensive_quality_analysis(
            original, reconstructed, original_size, compressed_size
        )
        
        # For lossy, should have finite PSNR
        assert analysis['psnr_db'] != float('inf'), "Lossy should have finite PSNR"
        assert analysis['psnr_db'] > 0, "PSNR should be positive"
        assert analysis['mse'] > 0, "Lossy should have MSE > 0"
        assert analysis['compression_ratio'] > 1.0, "Should show compression"
    
    def test_comprehensive_analysis_edge_cases(self):
        """Test edge cases in comprehensive analysis"""
        # Very small image
        original = np.array([[128, 129], [130, 131]], dtype=np.uint8)
        reconstructed = original.copy()
        
        analysis = comprehensive_quality_analysis(
            original, reconstructed, original_size=4, compressed_size=2
        )
        
        # Should complete without errors
        assert isinstance(analysis, dict), "Should return dict"
        assert 'compression_ratio' in analysis, "Should have compression ratio"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

"""
Information Theory and Quality Metrics

Implements Shannon entropy, PSNR, SSIM, and other metrics for analyzing
compression and reconstruction quality.
"""

import numpy as np
from typing import Dict, Any, Optional
from collections import Counter
import warnings


def calculate_entropy(data: np.ndarray) -> float:
    """
    Calculate Shannon entropy: H(X) = -Σ p(x) * log2(p(x))
    
    This is the theoretical minimum bits per symbol.
    
    Args:
        data: Input data (flattened array of symbols)
        
    Returns:
        Entropy in bits per symbol
    """
    # Flatten data
    flat_data = data.flatten()
    
    # Get probability distribution
    values, counts = np.unique(flat_data, return_counts=True)
    probabilities = counts / counts.sum()
    
    # Calculate entropy (filter out zero probabilities)
    probabilities = probabilities[probabilities > 0]
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    return float(entropy)


def calculate_psnr(original: np.ndarray, reconstructed: np.ndarray, 
                   max_value: float = 255.0) -> float:
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR)
    
    PSNR = 10 * log10(MAX^2 / MSE)
    
    Higher is better. Typical values:
    - > 40 dB: Excellent quality
    - 30-40 dB: Good quality
    - 20-30 dB: Acceptable
    - < 20 dB: Poor quality
    
    Args:
        original: Original data
        reconstructed: Reconstructed data
        max_value: Maximum possible value (255 for 8-bit images)
        
    Returns:
        PSNR in decibels (dB)
    """
    mse = np.mean((original.astype(float) - reconstructed.astype(float)) ** 2)
    
    if mse == 0:
        return float('inf')  # Perfect reconstruction
    
    psnr = 10 * np.log10(max_value ** 2 / mse)
    return float(psnr)


def calculate_ssim(original: np.ndarray, reconstructed: np.ndarray,
                   window_size: int = 11, k1: float = 0.01, k2: float = 0.03) -> float:
    """
    Calculate Structural Similarity Index (SSIM)
    
    Measures perceptual similarity (0 to 1, higher is better)
    
    Args:
        original: Original image
        reconstructed: Reconstructed image
        window_size: Size of sliding window
        k1, k2: Stability constants
        
    Returns:
        SSIM value between 0 and 1
    """
    try:
        from scipy.ndimage import uniform_filter
        
        # Ensure same shape
        if original.shape != reconstructed.shape:
            return 0.0
        
        # Convert to float
        img1 = original.astype(np.float64)
        img2 = reconstructed.astype(np.float64)
        
        # Constants
        C1 = (k1 * 255) ** 2
        C2 = (k2 * 255) ** 2
        
        # Compute means
        mu1 = uniform_filter(img1, size=window_size)
        mu2 = uniform_filter(img2, size=window_size)
        
        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2
        
        # Compute variances and covariance
        sigma1_sq = uniform_filter(img1 ** 2, size=window_size) - mu1_sq
        sigma2_sq = uniform_filter(img2 ** 2, size=window_size) - mu2_sq
        sigma12 = uniform_filter(img1 * img2, size=window_size) - mu1_mu2
        
        # Compute SSIM
        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
                   ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
        
        return float(np.mean(ssim_map))
    
    except ImportError:
        warnings.warn("scipy not available, SSIM calculation skipped")
        return 0.0


def calculate_mse(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """
    Calculate Mean Squared Error (MSE)
    
    Args:
        original: Original data
        reconstructed: Reconstructed data
        
    Returns:
        MSE value (lower is better)
    """
    mse = np.mean((original.astype(float) - reconstructed.astype(float)) ** 2)
    return float(mse)


def calculate_compression_ratio(original_size: int, compressed_size: int) -> float:
    """
    Calculate compression ratio
    
    Args:
        original_size: Size of original data in bytes
        compressed_size: Size of compressed data in bytes
        
    Returns:
        Compression ratio (e.g., 2.0 means 2x compression)
    """
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size


def calculate_space_saved(original_size: int, compressed_size: int) -> float:
    """
    Calculate percentage of space saved
    
    Args:
        original_size: Size of original data in bytes
        compressed_size: Size of compressed data in bytes
        
    Returns:
        Percentage saved (e.g., 75.0 means 75% reduction)
    """
    if original_size == 0:
        return 0.0
    return ((original_size - compressed_size) / original_size) * 100


def calculate_bits_per_pixel(total_bits: int, num_pixels: int) -> float:
    """
    Calculate bits per pixel (bpp)
    
    Args:
        total_bits: Total bits in compressed data
        num_pixels: Number of pixels in image
        
    Returns:
        Bits per pixel
    """
    if num_pixels == 0:
        return 0.0
    return total_bits / num_pixels


def analyze_data_distribution(data: np.ndarray) -> Dict[str, Any]:
    """
    Analyze the statistical distribution of data
    
    Args:
        data: Input data array
        
    Returns:
        Dictionary with distribution statistics
    """
    flat_data = data.flatten()
    
    return {
        'min': float(np.min(flat_data)),
        'max': float(np.max(flat_data)),
        'mean': float(np.mean(flat_data)),
        'median': float(np.median(flat_data)),
        'std': float(np.std(flat_data)),
        'unique_values': int(len(np.unique(flat_data))),
        'entropy': calculate_entropy(data),
    }


def comprehensive_quality_analysis(original: np.ndarray, 
                                   reconstructed: np.ndarray,
                                   original_size: int,
                                   compressed_size: int) -> Dict[str, Any]:
    """
    Perform comprehensive quality and compression analysis
    
    Args:
        original: Original data
        reconstructed: Reconstructed data
        original_size: Size of original in bytes
        compressed_size: Size of compressed in bytes
        
    Returns:
        Dictionary with all metrics
    """
    # Information theory metrics
    original_entropy = calculate_entropy(original)
    reconstructed_entropy = calculate_entropy(reconstructed)
    
    # Quality metrics
    psnr = calculate_psnr(original, reconstructed)
    ssim = calculate_ssim(original, reconstructed)
    mse = calculate_mse(original, reconstructed)
    
    # Compression metrics
    compression_ratio = calculate_compression_ratio(original_size, compressed_size)
    space_saved = calculate_space_saved(original_size, compressed_size)
    num_pixels = original.size
    bits_per_pixel = calculate_bits_per_pixel(compressed_size * 8, num_pixels)
    
    # Theoretical limits
    theoretical_min_bits = num_pixels * original_entropy
    efficiency = (theoretical_min_bits / (compressed_size * 8)) * 100 if compressed_size > 0 else 0
    
    return {
        # Information Theory
        'original_entropy': original_entropy,
        'reconstructed_entropy': reconstructed_entropy,
        'entropy_reduction': ((original_entropy - reconstructed_entropy) / original_entropy * 100) 
                            if original_entropy > 0 else 0,
        
        # Quality Metrics
        'psnr_db': psnr,
        'ssim': ssim,
        'mse': mse,
        
        # Compression Metrics
        'original_size_bytes': original_size,
        'compressed_size_bytes': compressed_size,
        'compression_ratio': compression_ratio,
        'space_saved_percent': space_saved,
        'bits_per_pixel': bits_per_pixel,
        
        # Efficiency
        'theoretical_min_bits': theoretical_min_bits,
        'efficiency_percent': efficiency,
        
        # Size info
        'num_pixels': num_pixels,
        'original_bpp': 8.0,  # Assuming 8-bit data
    }


def format_metrics_report(metrics: Dict[str, Any]) -> str:
    """
    Format metrics dictionary as readable report
    
    Args:
        metrics: Dictionary of metrics
        
    Returns:
        Formatted string report
    """
    report = []
    report.append("=" * 60)
    report.append("COMPRESSION & QUALITY ANALYSIS")
    report.append("=" * 60)
    
    report.append("\n📊 INFORMATION THEORY METRICS")
    report.append("-" * 60)
    report.append(f"Original Entropy:       {metrics['original_entropy']:.3f} bits/symbol")
    report.append(f"Reconstructed Entropy:  {metrics['reconstructed_entropy']:.3f} bits/symbol")
    report.append(f"Entropy Reduction:      {metrics['entropy_reduction']:.1f}%")
    
    report.append("\n🎯 QUALITY METRICS")
    report.append("-" * 60)
    report.append(f"PSNR:                   {metrics['psnr_db']:.2f} dB")
    report.append(f"SSIM:                   {metrics['ssim']:.4f}")
    report.append(f"MSE:                    {metrics['mse']:.2f}")
    
    report.append("\n💾 COMPRESSION METRICS")
    report.append("-" * 60)
    report.append(f"Original Size:          {metrics['original_size_bytes']:,} bytes")
    report.append(f"Compressed Size:        {metrics['compressed_size_bytes']:,} bytes")
    report.append(f"Compression Ratio:      {metrics['compression_ratio']:.2f}x")
    report.append(f"Space Saved:            {metrics['space_saved_percent']:.1f}%")
    report.append(f"Bits per Pixel:         {metrics['bits_per_pixel']:.2f}")
    
    report.append("\n⚡ EFFICIENCY")
    report.append("-" * 60)
    report.append(f"Theoretical Minimum:    {metrics['theoretical_min_bits']:,.0f} bits")
    report.append(f"Efficiency:             {metrics['efficiency_percent']:.1f}%")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)

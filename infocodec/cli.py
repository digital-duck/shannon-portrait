#!/usr/bin/env python3
"""
InfoCodec CLI - Information Coding and Encoding Tool

Command-line interface for compression and reconstruction experiments.
"""

import click
import sys
from pathlib import Path
import json
import numpy as np
from PIL import Image
import time

from infocodec.core.compressors import COMPRESSORS
from infocodec.core.metrics import comprehensive_quality_analysis, format_metrics_report
from infocodec.utils.image_utils import load_image, save_image, detect_media_type


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    InfoCodec - Information Coding & Encoding
    
    Research and educational tool for exploring Shannon's Information Theory
    through practical compression and reconstruction.
    
    \b
    Examples:
        infocodec encode --input shannon.png --method huffman
        infocodec decode --input compressed.dat --output restored.png  
        infocodec benchmark --input shannon.png --methods all
    """
    pass


@cli.command()
@click.option('--input', '-i', 'input_path', required=True, type=click.Path(exists=True),
              help='Input file path')
@click.option('--method', '-m', type=click.Choice(['naive', 'rle', 'differential', 'huffman', 'sparse', 'auto']),
              default='auto', help='Compression method (auto-detects best method)')
@click.option('--output', '-o', 'output_path', type=click.Path(),
              help='Output file path (default: input_compressed.dat)')
@click.option('--quality', '-q', type=click.FloatRange(0.0, 1.0), default=1.0,
              help='Quality level (0.0-1.0, where 1.0 is lossless)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def encode(input_path, method, output_path, quality, verbose):
    """
    Encode (compress) input data.
    
    Automatically detects media type (image/audio/text) and applies
    appropriate compression method.
    """
    click.echo(f"🔄 Encoding: {input_path}")
    
    # Detect media type
    media_type = detect_media_type(input_path)
    click.echo(f"📎 Media type: {media_type}")
    
    if media_type == 'image':
        _encode_image(input_path, method, output_path, quality, verbose)
    elif media_type == 'audio':
        click.echo("🎵 Audio compression coming soon!")
        sys.exit(1)
    elif media_type == 'text':
        click.echo("📝 Text compression coming soon!")
        sys.exit(1)
    else:
        click.echo(f"❌ Unsupported media type: {media_type}", err=True)
        sys.exit(1)


def _encode_image(input_path, method, output_path, quality, verbose):
    """Encode image file"""
    # Load image
    image = load_image(input_path)
    if verbose:
        click.echo(f"✓ Loaded image: {image.shape}")
    
    # Auto-detect best method if requested
    if method == 'auto':
        method = _auto_select_method(image, verbose)
        click.echo(f"🤖 Auto-selected method: {method}")
    
    # Get compressor
    compressor_class = COMPRESSORS.get(method)
    if not compressor_class:
        click.echo(f"❌ Unknown method: {method}", err=True)
        sys.exit(1)
    
    # Compress
    click.echo(f"⚡ Compressing with {method}...")
    start_time = time.time()
    
    compressor = compressor_class(quality=quality)
    compressed_bytes, metadata = compressor.compress(image)
    
    elapsed = time.time() - start_time
    
    # Determine output path
    if not output_path:
        output_path = Path(input_path).with_suffix('.dat')
    
    # Save compressed data
    output_path = Path(output_path)
    with open(output_path, 'wb') as f:
        # Write metadata as JSON header
        metadata_json = json.dumps(metadata)
        metadata_bytes = metadata_json.encode('utf-8')
        
        # Write: [metadata_length(4 bytes)][metadata][compressed_data]
        f.write(len(metadata_bytes).to_bytes(4, byteorder='big'))
        f.write(metadata_bytes)
        f.write(compressed_bytes)
    
    # Save metadata separately
    metadata_path = output_path.with_suffix('.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Statistics
    stats = compressor.get_stats()
    original_size = image.size * image.itemsize
    compressed_size = len(compressed_bytes)
    
    click.echo(f"\n✅ Compression complete!")
    click.echo(f"   Time: {elapsed:.3f}s")
    click.echo(f"   Original: {original_size:,} bytes")
    click.echo(f"   Compressed: {compressed_size:,} bytes")
    click.echo(f"   Ratio: {original_size/compressed_size:.2f}x")
    click.echo(f"   Output: {output_path}")
    click.echo(f"   Metadata: {metadata_path}")
    
    if verbose:
        click.echo(f"\n📊 Detailed Stats:")
        for key, value in stats.items():
            click.echo(f"   {key}: {value}")


def _auto_select_method(image, verbose=False):
    """Auto-select best compression method based on image characteristics"""
    from infocodec.core.metrics import calculate_entropy, analyze_data_distribution
    
    # Analyze image
    entropy = calculate_entropy(image)
    dist = analyze_data_distribution(image)
    
    if verbose:
        click.echo(f"  Entropy: {entropy:.2f} bits/pixel")
        click.echo(f"  Unique values: {dist['unique_values']}")
        click.echo(f"  Std dev: {dist['std']:.2f}")
    
    # Decision logic
    if dist['unique_values'] < 32:
        # Very few unique values - RLE will work well
        return 'rle'
    elif entropy < 3.0:
        # Low entropy - differential or RLE
        return 'differential'
    elif dist['std'] < 30:
        # Low variance - differential
        return 'differential'
    else:
        # General case - Huffman
        return 'huffman'


@cli.command()
@click.option('--input', '-i', 'input_path', required=True, type=click.Path(exists=True),
              help='Input compressed file')
@click.option('--output', '-o', 'output_path', type=click.Path(),
              help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def decode(input_path, output_path, verbose):
    """
    Decode (decompress) compressed data.
    
    Reads metadata from compressed file and applies appropriate
    reconstruction method.
    """
    from infocodec.core.reconstructors import RECONSTRUCTORS
    from infocodec.utils.image_utils import save_image
    
    click.echo(f"🔄 Decoding: {input_path}")
    
    # Read compressed file
    with open(input_path, 'rb') as f:
        # Read metadata length
        metadata_length = int.from_bytes(f.read(4), byteorder='big')
        
        # Read metadata
        metadata_bytes = f.read(metadata_length)
        metadata = json.loads(metadata_bytes.decode('utf-8'))
        
        # Read compressed data
        compressed_bytes = f.read()
    
    if verbose:
        click.echo(f"📋 Metadata: {json.dumps(metadata, indent=2)}")
    
    method = metadata.get('method', 'Unknown')
    click.echo(f"⚡ Decompressing with {method}...")
    
    # Get reconstructor
    reconstructor_class = RECONSTRUCTORS.get(method.lower())
    
    if not reconstructor_class:
        click.echo(f"❌ Unknown method: {method}", err=True)
        click.echo(f"   Available methods: {', '.join(RECONSTRUCTORS.keys())}")
        sys.exit(1)
    
    try:
        start_time = time.time()
        
        reconstructor = reconstructor_class()
        reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)
        
        elapsed = time.time() - start_time
        
        # Determine output path
        if not output_path:
            output_path = Path(input_path).with_suffix('.reconstructed.png')
        
        # Save reconstructed image
        save_image(reconstructed, output_path)
        
        # Get stats
        stats = reconstructor.get_stats()
        
        click.echo(f"\n✅ Decompression complete!")
        click.echo(f"   Time: {elapsed:.3f}s")
        click.echo(f"   Method: {method}")
        click.echo(f"   Output: {output_path}")
        click.echo(f"   Shape: {reconstructed.shape}")
        
        if verbose:
            click.echo(f"\n📊 Detailed Stats:")
            for key, value in stats.items():
                click.echo(f"   {key}: {value}")
    
    except Exception as e:
        click.echo(f"❌ Error during decoding: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--input', '-i', 'input_path', required=True, type=click.Path(exists=True),
              help='Input file path')
@click.option('--methods', '-m', default='all',
              help='Comma-separated methods to benchmark (e.g., "rle,huffman" or "all")')
@click.option('--output', '-o', 'output_dir', type=click.Path(),
              help='Output directory for results')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'markdown']),
              default='table', help='Output format')
def benchmark(input_path, methods, output_dir, format):
    """
    Benchmark multiple compression methods.
    
    Compares compression ratio, speed, and quality across methods.
    """
    click.echo(f"🔬 Benchmarking: {input_path}\n")
    
    # Parse methods
    if methods == 'all':
        methods_list = list(COMPRESSORS.keys())
    else:
        methods_list = [m.strip() for m in methods.split(',')]
    
    # Load image
    image = load_image(input_path)
    original_size = image.size * image.itemsize
    
    # Run benchmarks
    results = []
    
    for method in methods_list:
        click.echo(f"Testing {method}...", nl=False)
        
        compressor_class = COMPRESSORS.get(method)
        if not compressor_class:
            click.echo(" ❌ Unknown")
            continue
        
        try:
            start_time = time.time()
            compressor = compressor_class()
            compressed_bytes, metadata = compressor.compress(image)
            elapsed = time.time() - start_time
            
            stats = compressor.get_stats()
            compressed_size = len(compressed_bytes)
            ratio = original_size / compressed_size if compressed_size > 0 else 0
            
            results.append({
                'method': method,
                'original_bytes': original_size,
                'compressed_bytes': compressed_size,
                'ratio': ratio,
                'time_sec': elapsed,
                'entropy': stats.get('entropy', 0),
            })
            
            click.echo(f" ✓ {ratio:.2f}x in {elapsed:.3f}s")
            
        except Exception as e:
            click.echo(f" ❌ Error: {e}")
    
    # Display results
    click.echo(f"\n{'='*80}")
    click.echo("BENCHMARK RESULTS")
    click.echo(f"{'='*80}\n")
    
    if format == 'table':
        _print_table(results)
    elif format == 'json':
        click.echo(json.dumps(results, indent=2))
    elif format == 'markdown':
        _print_markdown(results)
    
    # Save to file if output directory specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"benchmark_{Path(input_path).stem}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        click.echo(f"\n💾 Results saved to: {output_file}")


def _print_table(results):
    """Print results as formatted table"""
    # Header
    header = f"{'Method':<15} {'Original':<12} {'Compressed':<12} {'Ratio':<8} {'Time':<8} {'Entropy':<8}"
    click.echo(header)
    click.echo("-" * len(header))
    
    # Rows
    for r in results:
        row = (f"{r['method']:<15} "
               f"{r['original_bytes']:>10,}  "
               f"{r['compressed_bytes']:>10,}  "
               f"{r['ratio']:>6.2f}x  "
               f"{r['time_sec']:>6.3f}s  "
               f"{r['entropy']:>6.2f}")
        click.echo(row)


def _print_markdown(results):
    """Print results as Markdown table"""
    click.echo("| Method | Original | Compressed | Ratio | Time | Entropy |")
    click.echo("|--------|----------|------------|-------|------|---------|")
    
    for r in results:
        click.echo(f"| {r['method']} | {r['original_bytes']:,} | "
                  f"{r['compressed_bytes']:,} | {r['ratio']:.2f}x | "
                  f"{r['time_sec']:.3f}s | {r['entropy']:.2f} |")


@cli.command()
def ui():
    """
    Launch Streamlit UI.
    
    Opens the interactive web interface for visual exploration.
    """
    import subprocess
    
    click.echo("🚀 Launching Streamlit UI...")
    click.echo("   Opening in browser: http://localhost:8501")
    click.echo("   Press Ctrl+C to stop")
    
    # Find streamlit app path
    app_path = Path(__file__).parent / "ui" / "app.py"
    
    if not app_path.exists():
        click.echo(f"❌ Streamlit app not found at: {app_path}", err=True)
        sys.exit(1)
    
    try:
        subprocess.run(['streamlit', 'run', str(app_path)])
    except KeyboardInterrupt:
        click.echo("\n👋 Stopping UI...")
    except FileNotFoundError:
        click.echo("❌ Streamlit not installed. Install with: pip install streamlit", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()

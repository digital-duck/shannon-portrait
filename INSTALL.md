# Installation & Quick Start Guide

## 📦 Installation

### Method 1: Install from PyPI (when published)

```bash
pip install shannon-portrait
```

### Method 2: Install from source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/shannon-portrait.git
cd shannon-portrait

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Method 3: Using the provided project

Since this is a complete project structure, you can:

```bash
cd shannon-portrait

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## ⚙️ Configuration

### 1. Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```bash
OPENROUTER_API_KEY=your-actual-key-here
```

### 2. Get OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Sign up or log in
3. Navigate to [API Keys](https://openrouter.ai/keys)
4. Create a new key
5. Copy and paste into `.env` file

## 🚀 Quick Start

### CLI Usage

```bash
# Check installation
infocodec --version

# Get help
infocodec --help

# Encode an image
infocodec encode --input examples/shannon.png --method auto

# Benchmark methods
infocodec benchmark --input examples/shannon.png --methods all

# Launch UI
infocodec ui
```

### Streamlit UI

```bash
# Start the web interface
streamlit run infocodec/ui/app.py

# Or use the CLI shortcut
infocodec ui
```

The UI will open in your browser at http://localhost:8501

## 📚 First Steps Tutorial

### Step 1: Prepare an Image

```bash
# Option A: Use a test image
python -c "from infocodec.utils.image_utils import create_test_image, save_image; save_image(create_test_image(pattern='blocks'), 'test.png')"

# Option B: Use your own image
# Just have any PNG/JPG ready
```

### Step 2: Run Compression

```bash
# Compress with auto-detection
infocodec encode --input test.png --method auto --verbose

# Try specific methods
infocodec encode --input test.png --method huffman
infocodec encode --input test.png --method rle
infocodec encode --input test.png --method differential
```

### Step 3: Compare Methods

```bash
# Benchmark all methods
infocodec benchmark --input test.png --methods all --format table

# Save results
infocodec benchmark --input test.png --methods all --output results/ --format json
```

### Step 4: Explore UI

```bash
# Launch Streamlit
infocodec ui
```

Then:
1. **Settings**: Configure algorithms and LLM
2. **Encode**: Upload and compress your image
3. **Decode**: View reconstruction
4. **Diff**: Analyze quality metrics
5. **Summarize**: Generate AI report (requires OpenRouter key)

## 🐍 Python API Usage

### Basic Compression

```python
from infocodec.core.compressors.image import NaiveCompressor, HuffmanCompressor
from infocodec.utils.image_utils import load_image, save_image

# Load image
image = load_image("shannon.png")

# Compress
compressor = HuffmanCompressor()
compressed_bytes, metadata = compressor.compress(image)

# Get stats
stats = compressor.get_stats()
print(f"Entropy: {stats['entropy']:.2f} bits/pixel")
print(f"Compression ratio: {stats['compression_ratio']:.2f}x")
```

### Metrics Calculation

```python
from infocodec.core.metrics import (
    calculate_entropy,
    calculate_psnr,
    comprehensive_quality_analysis
)

# Calculate entropy
entropy = calculate_entropy(image)
print(f"Entropy: {entropy:.2f} bits/pixel")

# Compare original vs reconstructed
analysis = comprehensive_quality_analysis(
    original=original_image,
    reconstructed=reconstructed_image,
    original_size=original_image.nbytes,
    compressed_size=len(compressed_bytes)
)

print(f"PSNR: {analysis['psnr_db']:.2f} dB")
print(f"SSIM: {analysis['ssim']:.4f}")
print(f"Compression: {analysis['compression_ratio']:.2f}x")
```

### Benchmark All Methods

```python
from infocodec.core.compressors import COMPRESSORS
from infocodec.utils.image_utils import load_image

image = load_image("test.png")

results = []
for name, compressor_class in COMPRESSORS.items():
    compressor = compressor_class()
    compressed, metadata = compressor.compress(image)
    stats = compressor.get_stats()
    
    results.append({
        'method': name,
        'entropy': stats['entropy'],
        'size': len(compressed),
        'ratio': stats.get('compression_ratio', 1.0)
    })

# Print results
for r in results:
    print(f"{r['method']:15s}: {r['ratio']:.2f}x compression")
```

## 🔧 Troubleshooting

### Issue: `infocodec: command not found`

**Solution**: Make sure the package is installed:

```bash
pip install -e .
```

And that your PATH includes the Python scripts directory.

### Issue: `ModuleNotFoundError: No module named 'infocodec'`

**Solution**: Install the package:

```bash
cd shannon-portrait
pip install -e .
```

### Issue: Streamlit won't start

**Solution**: Install Streamlit:

```bash
pip install streamlit
```

Then run:

```bash
streamlit run infocodec/ui/app.py
```

### Issue: OpenRouter API errors

**Solutions**:

1. Check your API key is correct in `.env`
2. Verify your account has credits
3. Check network connection
4. Try a different model

### Issue: Import errors

**Solution**: Install all dependencies:

```bash
pip install -r requirements.txt
```

## 📖 Next Steps

1. **Read the documentation**: Check `docs/` folder
2. **Run examples**: See `notebooks/` for Jupyter tutorials
3. **Explore UI**: Try different compression methods
4. **Read theory**: See `docs/THEORY.md` for information theory background
5. **Contribute**: See `CONTRIBUTING.md` for guidelines

## 💡 Tips

1. **Start with auto method**: Let the system choose the best algorithm
2. **Use caching**: Enable in Settings for faster repeated operations
3. **Compare methods**: Use benchmark to understand trade-offs
4. **Try different images**: Patterns affect compression differently
5. **Read the metrics**: Understand what PSNR, SSIM, entropy mean

## 🆘 Getting Help

- **Documentation**: Check `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/shannon-portrait/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shannon-portrait/discussions)

---

Happy exploring Shannon's Information Theory! 🎉

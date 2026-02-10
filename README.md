# Shannon Portrait - InfoCodec

**Information Coding & Encoding**: A research and educational tool for exploring Claude Shannon's Information Theory through practical image compression experiments.

## 🎯 Project Overview

This project demonstrates Shannon's fundamental concepts through the thought experiment of transmitting 2D images over a 1D wire:

- **2D → 1D**: Various encoding/compression methods
- **Transmission**: Simulated 1D channel
- **1D → 2D**: Reconstruction with quality analysis
- **Analysis**: Information theory metrics and AI-generated reports

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shannon-portrait.git
cd shannon-portrait

# Install the package
pip install -e .

# Or install from PyPI (when published)
pip install shannon-portrait
```

### CLI Usage

```bash
# Encode an image
infocodec encode --input shannon.png --method huffman

# Decode compressed data
infocodec decode --input compressed.dat --output restored.png

# Benchmark all methods
infocodec benchmark --input shannon.png --methods all

# Launch interactive UI
infocodec ui
```

### Streamlit UI

```bash
# Launch web interface
streamlit run infocodec/ui/app.py

# Or via CLI
infocodec ui
```

## 📚 Features

### Compression Methods

| Method | Type | Best For | Compression | Quality |
|--------|------|----------|-------------|---------|
| Naive | Baseline | Comparison | 1.0x | Perfect |
| RLE | Lossless | Block patterns | 4-10x | Perfect |
| Differential | Lossless | Smooth gradients | 2-5x | Perfect |
| Huffman | Lossless | General purpose | 1.5-3x | Perfect |
| Sparse | Lossy | Quick preview | 10-50x | Variable |
| DCT | Lossy | Photos (JPEG-style) | 5-20x | Variable |

### Information Theory Metrics

- **Shannon Entropy**: H(X) = -Σ p(x) log₂(p(x))
- **PSNR**: Peak Signal-to-Noise Ratio
- **SSIM**: Structural Similarity Index
- **Compression Ratio**: Original size / Compressed size
- **Bits per Pixel**: Total bits / Number of pixels

### Multi-Page UI

1. **⚙️ Settings**: Configure algorithms, LLM integration, caching
2. **📤 Encode**: Upload and compress images
3. **📥 Decode**: Reconstruct from compressed data
4. **📊 Diff**: Visual and quantitative quality analysis
5. **📝 Summarize**: AI-generated experimental reports

## 🏗️ Project Structure

```
shannon-portrait/
├── infocodec/                  # Main package
│   ├── __init__.py
│   ├── cli.py                  # Click CLI
│   ├── core/
│   │   ├── base.py             # Abstract base classes
│   │   ├── metrics.py          # Information theory metrics
│   │   ├── compressors/        # Compression algorithms
│   │   │   └── image/
│   │   │       ├── naive.py
│   │   │       ├── rle.py
│   │   │       ├── differential.py
│   │   │       ├── huffman.py
│   │   │       ├── sparse.py
│   │   │       └── dct.py
│   │   └── reconstructors/     # Reconstruction algorithms
│   │       └── image/
│   │           ├── direct.py
│   │           ├── progressive.py
│   │           └── error_recovery.py
│   ├── ui/                     # Streamlit interface
│   │   ├── app.py              # Main app
│   │   ├── pages/              # Multi-page app
│   │   │   ├── 1_⚙️_Settings.py
│   │   │   ├── 2_📤_Encode.py
│   │   │   ├── 3_📥_Decode.py
│   │   │   ├── 4_📊_Diff.py
│   │   │   └── 5_📝_Summarize.py
│   │   └── components/         # Reusable UI components
│   └── utils/                  # Utilities
│       ├── image_utils.py
│       ├── config.py
│       └── openrouter.py       # LLM integration
├── data/
│   └── images/
│       └── shannon_portrait.png
├── tests/                      # Unit tests
├── docs/                       # Documentation
├── notebooks/                  # Jupyter tutorials
├── setup.py                    # Package setup
├── requirements.txt
└── README.md

```

## 🔬 Research Use Cases

### 1. Information Representation Study

Explore how different encodings represent the same information:

```python
from infocodec.core.compressors import COMPRESSORS
from infocodec.utils.image_utils import load_image

image = load_image("shannon.png")

for method_name, compressor_class in COMPRESSORS.items():
    compressor = compressor_class()
    compressed, metadata = compressor.compress(image)
    stats = compressor.get_stats()
    print(f"{method_name}: {stats['entropy']:.2f} bits/pixel")
```

### 2. Compression Algorithm Comparison

Benchmark multiple methods:

```bash
infocodec benchmark --input test_images/ --methods all --output results/
```

### 3. Rate-Distortion Analysis

Study the trade-off between compression and quality:

```python
qualities = [1.0, 0.9, 0.8, 0.7, 0.5, 0.3, 0.1]
for q in qualities:
    # Compress at different quality levels
    # Measure PSNR vs. compression ratio
```

### 4. Educational Demonstrations

Use the Streamlit UI for interactive teaching:

1. Show students entropy of different patterns
2. Demonstrate compression effectiveness
3. Visualize reconstruction quality
4. Compare theoretical vs. practical results

## 🤖 LLM Integration (OpenRouter)

### Setup

1. Get API key from [OpenRouter.ai](https://openrouter.ai/keys)
2. Configure in Settings page or environment variable:

```bash
export OPENROUTER_API_KEY="your-key-here"
```

### Supported Models

- `anthropic/claude-3.5-sonnet` (Recommended)
- `anthropic/claude-3-opus`
- `openai/gpt-4-turbo`
- `google/gemini-pro`
- And more...

### Report Generation

The **Summarize** page uses LLM to generate:

- Markdown reports with all metrics
- Theoretical analysis
- Recommendations
- Experimental conclusions

## 📖 Theoretical Background

### Shannon's Information Theory

**Entropy** - Measures information content:
```
H(X) = -Σ p(x) log₂(p(x))
```

**Channel Capacity** - Maximum reliable transmission rate:
```
C = B log₂(1 + SNR)
```

**Rate-Distortion** - Trade-off between rate and quality:
```
R(D) = min I(X;Y) subject to E[d(X,Y)] ≤ D
```

### Why This Matters

Shannon proved:
1. **You cannot compress below entropy** (losslessly)
2. **Reliable communication is possible** below channel capacity
3. **There's always a rate-distortion trade-off** for lossy compression

This project makes these abstract concepts tangible!

## 🔮 Future Enhancements

### Phase 2: Audio Support

- Implement audio compressors (MP3-style, Opus-style)
- Waveform visualization
- Perceptual audio metrics

### Phase 3: Text Support

- LZ77, LZ78 algorithms
- Huffman for text
- Dictionary-based methods
- Language model-based compression

### Phase 4: Advanced Features

- Real-time streaming simulation
- Error injection and correction
- Multi-user collaboration
- Comparative studies database

## 🧪 Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=infocodec

# Specific test file
pytest tests/test_compressors.py
```

## 📊 Example Results

### Gradient Image (64x64)

| Method | Entropy | Compression | PSNR | Time |
|--------|---------|-------------|------|------|
| Naive | 6.72 | 1.00x | ∞ | 0.001s |
| RLE | 6.72 | 0.50x | ∞ | 0.002s |
| Differential | 0.28 | 8.93x | ∞ | 0.003s |
| Huffman | 6.72 | 1.19x | ∞ | 0.015s |

### Block Pattern (64x64)

| Method | Entropy | Compression | PSNR | Time |
|--------|---------|-------------|------|------|
| Naive | 5.72 | 1.00x | ∞ | 0.001s |
| RLE | 5.72 | 4.00x | ∞ | 0.002s |
| Differential | 1.29 | 2.19x | ∞ | 0.003s |
| Huffman | 5.72 | 1.40x | ∞ | 0.014s |

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas for contribution:
- New compression algorithms
- Audio/text support
- UI improvements
- Documentation
- Test coverage
- Performance optimization

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Claude Shannon**: For founding information theory
- **Tutorial inspirations**: Cover & Thomas, MacKay
- **Community**: All contributors and users

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/shannon-portrait/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shannon-portrait/discussions)

---

*"The fundamental problem of communication is that of reproducing at one point exactly or approximately a message selected at another."* — Claude Shannon, 1948

Built with ❤️ for exploring information theory.

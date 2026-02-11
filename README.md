# Shannon Portrait — InfoCodec

**Information Coding & Encoding**: A research and educational tool for exploring Claude Shannon's Information Theory through practical image compression experiments.

## 🎯 Project Overview

This project demonstrates Shannon's fundamental concepts through the thought experiment of transmitting a 2D image over a 1D wire:

- **2D → 1D**: Encode/compress an image with one of six algorithms
- **Transmission**: Simulated 1D byte channel (the `.dat` file)
- **1D → 2D**: Reconstruct the image and measure quality loss
- **Analysis**: Information theory metrics, visual diff, and AI-generated reports

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shannon-portrait.git
cd shannon-portrait

# Create and activate environment
conda create -n st python=3.11
conda activate st

# Install in editable mode
pip install -e .
```

### CLI Usage

```bash
# Encode an image (auto-selects best method)
infocodec encode --input data/input/image/shannon-4.png

# Encode with a specific method
infocodec encode --input data/input/image/shannon-4.png --method huffman

# Decode back to an image
infocodec decode --input data/output/image/shannon-4_image_huffman.dat

# Benchmark all methods on an image
infocodec benchmark --input data/input/image/shannon-4.png --methods all

# Benchmark specific methods, output as Markdown
infocodec benchmark --input data/input/image/shannon-4.png --methods rle,huffman,dct --format markdown

# Launch the interactive web UI
infocodec-ui
```

### Streamlit UI

```bash
# Launch directly with Streamlit
streamlit run infocodec/ui/InfoCoDec.py

# Or via the installed entry point
infocodec-ui
```

The UI opens at **http://localhost:8501**.

## 📚 Features

### Compression Methods

| Method | Type | Best For | Ratio | Quality |
|--------|------|----------|-------|---------|
| Naive | Baseline | Comparison only | 1.0× | Perfect |
| RLE | Lossless | Solid regions, logos | 4–10× | Perfect |
| Differential | Lossless | Smooth gradients | 2–5× | Perfect |
| Huffman | Lossless | General purpose | 1.5–3× | Perfect |
| Sparse | Lossy | Quick preview | 10–50× | Variable |
| DCT | Lossy | Natural photos (JPEG-style) | 5–20× | Adjustable |
| **auto** | — | Let the app decide | varies | varies |

**Auto-detection logic:**
- Unique pixel values < 32 → RLE
- Entropy < 3.0 bits/pixel → Differential
- Std deviation < 30 → Differential
- Otherwise → Huffman

### Information Theory Metrics

| Metric | Formula | Meaning |
|--------|---------|---------|
| Shannon Entropy | H(X) = -Σ p(x) log₂(p(x)) | Theoretical minimum bits/symbol |
| PSNR | 10 log₁₀(255² / MSE) | Reconstruction fidelity (dB) |
| SSIM | structural + luminance + contrast | Perceptual similarity (0–1) |
| Coding Efficiency | H(X)·N / compressed_bits × 100% | How close to Shannon limit |
| BPP | compressed_bits / num_pixels | Bits per pixel after compression |
| Compression Ratio | original_bytes / compressed_bytes | Size reduction factor |

### Multi-Page Streamlit UI

| Page | Description |
|------|-------------|
| ⚙️ Settings | Compression defaults, OpenRouter API key, LLM model selection |
| 🗜️ Encode | Upload or generate an image, compress it, download `.dat` |
| 🖼️ Decode | Reconstruct image from compressed data, view quality metrics |
| 📊 Diff | Visual diff, error heatmap, entropy analysis, rate-distortion |
| 📝 Summarize | AI-generated report via OpenRouter (Claude, GPT-4, Gemini, etc.) |
| 🎓 Explain | Educational reference for all algorithms and metrics |

## 🏗️ Project Structure

```
shannon-portrait/
├── infocodec/                      # Main package
│   ├── __init__.py
│   ├── cli.py                      # Click CLI (encode, decode, benchmark, ui)
│   ├── core/
│   │   ├── base.py                 # Abstract base classes + registry helpers
│   │   ├── metrics.py              # Shannon entropy, PSNR, SSIM, compression ratio
│   │   ├── compressors/
│   │   │   └── image/
│   │   │       ├── naive.py        # Baseline — raw byte stream
│   │   │       ├── rle.py          # Run-Length Encoding
│   │   │       ├── differential.py # Delta / differential encoding
│   │   │       ├── huffman.py      # Huffman variable-length coding
│   │   │       ├── sparse.py       # Sparse sampling
│   │   │       └── dct.py          # Discrete Cosine Transform (JPEG-style)
│   │   └── reconstructors/
│   │       └── image/
│   │           ├── direct.py       # Naive reconstructor (reshape)
│   │           ├── rle.py          # RLE decoder
│   │           ├── differential.py # Cumulative-sum integrator
│   │           ├── huffman.py      # Huffman decoder
│   │           ├── sparse.py       # Interpolation-based reconstructor
│   │           └── dct.py          # Inverse DCT reconstructor
│   ├── ui/
│   │   ├── InfoCoDec.py            # Streamlit app entry point
│   │   ├── components/             # Reusable UI components (future)
│   │   └── pages/
│   │       ├── 1_⚙️_Settings.py
│   │       ├── 2_🗜️_Encode.py
│   │       ├── 3_🖼️_Decode.py
│   │       ├── 4_📊_Diff.py
│   │       ├── 5_📝_Summarize.py
│   │       └── 6_🎓_Explain.py
│   └── utils/
│       ├── image_utils.py          # load_image, save_image, create_test_image
│       ├── paths.py                # Project-root resolution, output path builder
│       └── openrouter.py           # API key resolution + OpenAI-compat client
├── data/
│   ├── input/
│   │   ├── image/                  # Source images (Shannon portrait variants)
│   │   ├── audio/                  # Placeholder (Phase 2)
│   │   └── text/                   # Placeholder (Phase 3)
│   └── output/
│       ├── image/                  # .dat compressed files + .json sidecars
│       ├── audio/
│       └── text/
├── tests/
│   ├── test_compressors.py
│   ├── test_metrics.py
│   └── test_reconstructors.py
├── docs/
│   ├── CLAUDE.md
│   ├── DIAGRAMS.md
│   ├── VERIFICATION_GUIDE.md
│   └── FINAL_DELIVERY.md
├── .env.example                    # API key template
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## 🗂️ File Naming Convention

Compressed outputs follow a structured naming scheme so the method and modality are
readable at a glance without opening the file:

```
{stem}_{modality}_{method}[_{qualifier}].{ext}
```

| Component | Example | Notes |
|-----------|---------|-------|
| `stem` | `shannon-4` | Source filename without extension |
| `modality` | `image` | `image` / `audio` / `text` |
| `method` | `huffman` | The compression algorithm used |
| `qualifier` | `q08` / `sr4` | DCT quality (`q08` = 0.8) or Sparse rate (`sr4` = every 4th pixel) |
| `ext` | `dat` / `json` / `txt` | `.dat` = compressed binary; `.json` = metadata sidecar |

**Examples:**

```
shannon-4_image_huffman.dat        # Huffman-compressed image
shannon-4_image_dct_q08.dat        # DCT at quality 0.8
shannon-4_image_sparse_sr4.dat     # Sparse sampling, every 4th pixel
report_shannon-4_image_huffman.txt # Text report
summary_shannon-4_image_huffman.md # AI summary (Markdown)
metrics_shannon-4_image_huffman.json
```

## 📦 Compressed File Format

Each `.dat` file is self-describing — no external configuration needed to decode it:

```
[4 bytes — metadata length (big-endian uint32)]
[N bytes — JSON metadata (method, original_shape, algorithm params)]
[remaining bytes — compressed payload]
```

A `.json` sidecar with the same stem is also written alongside each `.dat`
for easy inspection without decoding.

## ⚙️ CLI Reference

### `infocodec encode`

```
Usage: infocodec encode [OPTIONS]

Options:
  -i, --input PATH     Input image file [required]
  -m, --method TEXT    naive|rle|differential|huffman|sparse|dct|auto  [default: auto]
  -o, --output PATH    Output .dat file [default: data/output/image/...]
  -q, --quality FLOAT  Quality level 0.0–1.0 for DCT  [default: 1.0]
  -v, --verbose        Show detailed compression stats
```

### `infocodec decode`

```
Usage: infocodec decode [OPTIONS]

Options:
  -i, --input PATH   Compressed .dat file [required]
  -o, --output PATH  Output image file  [default: data/output/image/..._reconstructed.png]
  -v, --verbose      Show reconstruction stats
```

### `infocodec benchmark`

```
Usage: infocodec benchmark [OPTIONS]

Options:
  -i, --input PATH    Input image file [required]
  -m, --methods TEXT  Comma-separated methods or "all"  [default: all]
  -o, --output PATH   Output directory for results
  -f, --format TEXT   table|json|markdown  [default: table]
```

### `infocodec-ui`

Launches the Streamlit web interface at `http://localhost:8501`.

## 🤖 LLM Integration (OpenRouter)

The **📝 Summarize** page generates AI-powered experiment reports.

### Setup

```bash
# Option 1 — .env file (recommended)
cp .env.example .env
# Edit .env and set:  OPENROUTER_API_KEY=sk-or-...

# Option 2 — shell export
export OPENROUTER_API_KEY=sk-or-...
```

Resolution order: `.env` file → `OPENROUTER_API_KEY` env var → manual entry in Settings.

### Supported Models

- `anthropic/claude-3.5-sonnet` (default)
- `anthropic/claude-3-opus`
- `anthropic/claude-3-haiku`
- `openai/gpt-4-turbo`
- `openai/gpt-4`
- `google/gemini-pro`
- `meta-llama/llama-3-70b-instruct`
- Any model available on [openrouter.ai](https://openrouter.ai/models)

### Report Styles

| Style | Audience |
|-------|---------|
| Technical | Research papers, engineering reports |
| Educational | Students, classroom demos |
| Executive Summary | Quick decision-makers |

The prompt is fully editable before generation. Reports can be downloaded as `.md` or `.txt`.

## 📖 Theoretical Background

### Shannon's Three Theorems

**Entropy** — the information content of a source:
```
H(X) = -Σ p(x) log₂(p(x))     bits/symbol
```
This is the *theoretical lower bound* for lossless compression. No algorithm can compress below it.

**Channel Capacity** — maximum reliable transmission rate:
```
C = B log₂(1 + S/N)            bits/second
```

**Rate–Distortion** — the fundamental lossy trade-off:
```
R(D) = min I(X;Y)  subject to  E[d(X,Y)] ≤ D
```
More compression (lower rate) always means more distortion. This app makes this trade-off
visible through the DCT quality slider and the Diff page.

## 🔬 Python API

```python
from infocodec.core.compressors import COMPRESSORS
from infocodec.core.reconstructors import RECONSTRUCTORS
from infocodec.core.metrics import calculate_entropy, comprehensive_quality_analysis
from infocodec.utils.image_utils import load_image, save_image

# Load image (returns uint8 ndarray, grayscale or RGB)
image = load_image("data/input/image/shannon-4.png")

# Compress
compressor = COMPRESSORS['huffman']()
compressed_bytes, metadata = compressor.compress(image)
print(compressor.get_stats())

# Reconstruct
reconstructor = RECONSTRUCTORS['huffman']()
reconstructed = reconstructor.reconstruct(compressed_bytes, metadata)

# Analyse
analysis = comprehensive_quality_analysis(
    original=image,
    reconstructed=reconstructed,
    original_size=image.size,
    compressed_size=len(compressed_bytes),
)
print(f"PSNR: {analysis['psnr_db']:.2f} dB")
print(f"SSIM: {analysis['ssim']:.4f}")
print(f"Efficiency: {analysis['efficiency_percent']:.1f}%")
```

### Benchmark all methods in code

```python
for name, cls in COMPRESSORS.items():
    c = cls()
    cb, meta = c.compress(image)
    stats = c.get_stats()
    print(f"{name:15} ratio={stats.get('compression_ratio', 0):.2f}x  entropy={stats.get('entropy', 0):.2f}")
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=infocodec --cov-report=html

# Run a specific suite
pytest tests/test_compressors.py -v
pytest tests/test_metrics.py -v
pytest tests/test_reconstructors.py -v
```

## 📊 Example Results

### Shannon Portrait (shannon-4.png — colour, 240×179)

| Method | Ratio | Entropy (bpp) | PSNR | Type |
|--------|-------|---------------|------|------|
| Naive | 1.00× | 7.54 | ∞ | Lossless |
| RLE | ~0.5× | 7.54 | ∞ | Lossless |
| Differential | ~2.0× | ~1.2 | ∞ | Lossless |
| Huffman | ~1.2× | 7.54 | ∞ | Lossless |
| Sparse (sr=4) | ~16× | — | ~28 dB | Lossy |
| DCT (q=0.8) | ~8× | — | ~35 dB | Lossy |

### Synthetic Gradient (64×64, grayscale)

| Method | Ratio | Entropy | PSNR |
|--------|-------|---------|------|
| Naive | 1.00× | 6.72 | ∞ |
| RLE | 0.50× | 6.72 | ∞ |
| Differential | 8.93× | 0.28 | ∞ |
| Huffman | 1.19× | 6.72 | ∞ |

### Synthetic Blocks (64×64, grayscale)

| Method | Ratio | Entropy | PSNR |
|--------|-------|---------|------|
| Naive | 1.00× | 5.72 | ∞ |
| RLE | 4.00× | 5.72 | ∞ |
| Differential | 2.19× | 1.29 | ∞ |
| Huffman | 1.40× | 5.72 | ∞ |

## 🔮 Future Enhancements

### Phase 2 — Audio Support

- PCM, ADPCM, simplified LPC compressors
- Waveform + spectrogram visualisation
- Perceptual audio metrics (SNR, spectral distortion)

### Phase 3 — Text Support

- LZ77 / LZ78 / LZW algorithms
- Huffman and arithmetic coding for text
- Language-model-based compression (tokenisation entropy)

### Phase 4 — Advanced Features

- Real-time streaming simulation with latency/packet-loss injection
- Error correction codes (Hamming, Reed-Solomon)
- Comparative studies database
- Arithmetic coding (approaches entropy within 0.001 bits)

## 🤝 Contributing

Contributions welcome! Areas of interest:

- New compression algorithms (arithmetic coding, LZ77, LZMA)
- Audio / text modality support (architecture already in place)
- UI improvements and new visualisations
- Performance optimisation (numba, Cython for inner loops)
- Additional test coverage

## 📄 License

MIT License — see [LICENSE](LICENSE).

## 🙏 Acknowledgments

- **Claude Shannon** — for founding information theory
- **Cover & Thomas** — *Elements of Information Theory* (textbook reference)
- **David MacKay** — *Information Theory, Inference, and Learning Algorithms* (freely available online)

## 🐘 Broader Context: Elegant Elephant

This project is one instrument in a larger research programme called **Elegant Elephant**,
which proposes that compression, dimensionality reduction, quantum measurement, symmetry
breaking, and philosophical notions of illusion are all the *same underlying process* —
projection from a higher-dimensional reality to a lower-dimensional observable.

Within that framework, `shannon-portrait` studies the **information theory axis**:

| Elegant Elephant concept | This project's concrete form |
|---|---|
| Projection operator `π: H → L` | Each compression algorithm (DCT, Huffman, RLE, …) |
| Information loss `I(H) > I(π(H))` | Entropy, PSNR, SSIM, compression ratio metrics |
| Irreversibility of projection | Lossy vs lossless reconstruction experiments |
| Different projections reveal different aspects | Benchmark comparison across all methods |

The manifold learning axis (PHATE, t-SNE, PCA as projection operators) is studied in a
sibling instrument: **Semanscope**.

See [`README-Elegant-Elephant.md`](../zinets/README-Elegant-Elephant.md) for the full unified framework.

---

*"The fundamental problem of communication is that of reproducing at one point exactly or approximately a message selected at another."* — Claude Shannon, 1948

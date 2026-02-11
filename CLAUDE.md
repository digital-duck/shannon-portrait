# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Research Context

This project is the **information theory instrument** within the **Elegant Elephant** research programme — a unified framework proposing that compression, dimensionality reduction, quantum measurement, and symmetry breaking are all instances of the same projection operation `π: H → L` (higher-dimensional reality → lower-dimensional observable). The manifold learning instrument is **Semanscope**. The overarching framework document is at `../zinets/README-Elegant-Elephant.md`.

## Project Overview

**shannon-portrait / infocodec** is a research and educational Python package for exploring Claude Shannon's Information Theory through image compression experiments. The core concept is "2D → 1D → 2D": images are compressed (encoded), transmitted, and reconstructed with quality analysis.

The package is installable as `shannon-portrait` and exposes a `infocodec` CLI entry point.

## Commands

### Installation

```bash
# Recommended: use a conda environment
conda create -n st python=3.11
conda activate st

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or just core dependencies
pip install -e .
```

### Running Tests

```bash
# Run all tests (with coverage, per pyproject.toml defaults)
pytest

# Run a single test file
pytest tests/test_compressors.py

# Run a single test
pytest tests/test_compressors.py::TestClassName::test_method_name

# Run without coverage (faster)
pytest --no-cov
```

### Linting / Formatting

```bash
black infocodec tests          # Format code (line length: 100)
isort infocodec tests          # Sort imports
flake8 infocodec               # Lint
mypy infocodec                 # Type check
```

### Running the App

```bash
# Launch the Streamlit UI directly
streamlit run infocodec/ui/InfoCoDec.py

# Or via CLI
infocodec-ui

# CLI usage
infocodec encode --input image.png --method huffman
infocodec decode --input compressed.dat --output restored.png
infocodec benchmark --input image.png --methods all --format table
```

### LLM Integration

Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY` to enable the AI-powered Summarize page. The `openai` client is configured to point at OpenRouter's API base URL.

## Architecture

### Core Design Pattern

The package uses **abstract base classes + registry pattern**:

- `infocodec/core/base.py`: `Compressor` and `Reconstructor` ABCs, with `ImageCompressor` and `ImageReconstructor` subclasses for image-specific preprocessing/postprocessing. Stub classes exist for future `AudioCompressor` and `TextCompressor`.
- `infocodec/core/compressors/image/` and `infocodec/core/reconstructors/image/`: Concrete algorithm implementations (naive, rle, differential, huffman, sparse, dct).
- **`COMPRESSORS` and `RECONSTRUCTORS` registries** (dicts in the respective `__init__.py`) map method name strings to classes. The CLI and UI look up algorithms by name through these registries.

### Compress/Reconstruct Contract

Every compressor returns `(compressed_bytes, metadata_dict)`. The metadata is **self-describing**: it embeds the method name, original shape, dtype, and any algorithm-specific parameters needed for reconstruction. The `.dat` file format written by the CLI stores `[4-byte metadata length][metadata JSON][compressed bytes]`.

### Metrics

`infocodec/core/metrics.py` provides standalone functions:
- `calculate_entropy(data)` — Shannon entropy H(X)
- `calculate_psnr(original, reconstructed)` — PSNR in dB
- `calculate_ssim(original, reconstructed)` — SSIM
- `calculate_compression_ratio(original, compressed)` — size ratio
- `comprehensive_quality_analysis(...)` — runs all metrics together

### UI Structure

`infocodec/ui/InfoCoDec.py` is the Streamlit entry point. The multi-page UI lives in `infocodec/ui/pages/` (Streamlit's native multi-page format using numbered filenames). The 5th page (Summarize) uses OpenRouter/OpenAI SDK for LLM-generated reports; infrastructure is in `infocodec/utils/` (note: `openrouter.py` is referenced in docs but was not present in the repo at time of analysis — the `openai` package is used directly with a custom `base_url`).

### Extending with a New Compression Method

1. Create `infocodec/core/compressors/image/<method>.py` inheriting from `ImageCompressor`.
2. Implement `compress(image) -> (bytes, metadata)` and `get_stats() -> dict`.
3. Register in `infocodec/core/compressors/__init__.py`'s `COMPRESSORS` dict.
4. Create the matching reconstructor in `infocodec/core/reconstructors/image/<method>.py`.
5. Register in `infocodec/core/reconstructors/__init__.py`'s `RECONSTRUCTORS` dict.
6. Add tests in `tests/test_compressors.py` and `tests/test_reconstructors.py`.

### Data Directory Layout

Input files go under `data/input/{modality}/`; all outputs land in `data/output/{modality}/`:

```
data/
├── input/
│   ├── image/      # source images (.png, .jpg, …)
│   ├── audio/      # future
│   └── text/       # future
└── output/
    ├── image/      # compressed .dat, reconstructed .png, reports, benchmarks
    ├── audio/      # future
    └── text/       # future
```

### Output Filename Convention

All generated files follow: `[{prefix}_]{stem}_{modality}_{method}[_{qualifier}][_{suffix}].{ext}`

| Example filename | What it means |
|---|---|
| `shannon_portrait_image_huffman.dat` | Huffman-compressed image |
| `shannon_portrait_image_dct_q08.dat` | DCT at quality 0.8 |
| `shannon_portrait_image_sparse_sr4.dat` | Sparse with sampling_rate=4 |
| `shannon_portrait_image_huffman_reconstructed.png` | Reconstructed output |
| `benchmark_shannon_portrait_image_all.json` | Benchmark results |
| `report_shannon_portrait_image_huffman.txt` | Text quality report |
| `metrics_shannon_portrait_image_huffman.json` | JSON metrics |

Helpers live in `infocodec/utils/paths.py`: `get_input_dir(media_type)`, `get_output_dir(media_type)`, `make_output_filename(stem, modality, method, ext, ...)`, `quality_qualifier(q)`, `sampling_rate_qualifier(n)`.

### Key Files

| File | Purpose |
|------|---------|
| `infocodec/core/base.py` | Abstract base classes for all compressors/reconstructors |
| `infocodec/core/metrics.py` | Shannon entropy, PSNR, SSIM, compression ratio |
| `infocodec/core/compressors/image/__init__.py` | `COMPRESSORS` registry |
| `infocodec/core/reconstructors/image/__init__.py` | `RECONSTRUCTORS` registry |
| `infocodec/cli.py` | Click CLI (`encode`, `decode`, `benchmark`, `ui` commands) |
| `infocodec/ui/InfoCoDec.py` | Streamlit app entry point |
| `infocodec/utils/image_utils.py` | `load_image`, `save_image`, `create_test_image`, `detect_media_type` |
| `infocodec/utils/paths.py` | Data directory helpers and output filename builder |

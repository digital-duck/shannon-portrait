"""
Path helpers and output filename conventions for InfoCodec.

Naming convention for output files:
    {stem}_{modality}_{method}[_{qualifier}].{ext}

Examples:
    shannon_portrait_image_huffman.dat
    shannon_portrait_image_dct_q08.dat          # DCT at quality 0.8
    shannon_portrait_image_sparse_sr4.dat        # Sparse with sampling_rate=4
    shannon_portrait_image_huffman_reconstructed.png
    benchmark_shannon_portrait_image_all.json
    report_shannon_portrait_image_huffman.txt
"""

from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Return the repository root directory.

    Walks up from this file (infocodec/utils/paths.py) to find the root,
    identified by the presence of pyproject.toml.
    """
    candidate = Path(__file__).resolve().parent
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    # Fallback: two levels up from this file (infocodec/utils -> infocodec -> root)
    return Path(__file__).resolve().parent.parent.parent


def get_data_dir() -> Path:
    """Return the root-level data/ directory."""
    return get_project_root() / "data"


def get_input_dir(media_type: str = "image") -> Path:
    """
    Return data/input/{media_type}/, creating it if needed.

    Args:
        media_type: One of 'image', 'audio', 'text'.
    """
    path = get_data_dir() / "input" / media_type
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_output_dir(media_type: str = "image") -> Path:
    """
    Return data/output/{media_type}/, creating it if needed.

    Args:
        media_type: One of 'image', 'audio', 'text'.
    """
    path = get_data_dir() / "output" / media_type
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_output_filename(
    stem: str,
    modality: str,
    method: str,
    ext: str,
    qualifier: Optional[str] = None,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> str:
    """
    Build a descriptive output filename.

    Pattern: [{prefix}_]{stem}_{modality}_{method}[_{qualifier}][_{suffix}].{ext}

    Args:
        stem:      Base name, typically the input filename stem
                   (e.g. 'shannon_portrait').
        modality:  Data type: 'image', 'audio', or 'text'.
        method:    Compression method name (e.g. 'huffman', 'dct', 'rle').
        ext:       File extension without leading dot (e.g. 'dat', 'png', 'json').
        qualifier: Optional algorithm parameter tag (e.g. 'q08' for quality=0.8,
                   'sr4' for sampling_rate=4).
        prefix:    Optional filename prefix (e.g. 'benchmark', 'report').
        suffix:    Optional trailing tag (e.g. 'reconstructed').

    Returns:
        Filename string, e.g. 'shannon_portrait_image_dct_q08_reconstructed.dat'
    """
    ext = ext.lstrip(".")
    parts = []
    if prefix:
        parts.append(prefix)
    parts.append(stem)
    parts.append(modality)
    parts.append(method)
    if qualifier:
        parts.append(qualifier)
    if suffix:
        parts.append(suffix)
    return "_".join(parts) + f".{ext}"


def quality_qualifier(quality: float) -> str:
    """
    Convert a float quality value to a compact qualifier tag.

    Examples:
        0.8  -> 'q08'
        1.0  -> 'q10'
        0.25 -> 'q025'
    """
    # Remove leading zero and decimal point: 0.8 -> '08', 0.25 -> '025'
    tag = f"{quality:.2f}".replace(".", "").lstrip("0") or "0"
    return f"q{tag}"


def sampling_rate_qualifier(sampling_rate: int) -> str:
    """
    Convert a sampling rate integer to a qualifier tag.

    Example: 4 -> 'sr4'
    """
    return f"sr{sampling_rate}"

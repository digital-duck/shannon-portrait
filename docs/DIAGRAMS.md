# Shannon Portrait - Architecture Diagrams

This document contains Mermaid diagrams visualizing the Shannon Portrait project architecture.

---

## 📊 Diagram 1: System Architecture Overview

```mermaid
graph TB
    subgraph "User Interfaces"
        CLI[CLI - infocodec]
        UI[Streamlit Multi-Page UI]
    end

    subgraph "Core Engine"
        direction TB
        COMP[Compressors]
        RECON[Reconstructors]
        METRICS[Metrics Engine]
        
        subgraph "Compressors Registry"
            C1[Naive]
            C2[RLE]
            C3[Differential]
            C4[Huffman]
            C5[Sparse]
            C6[DCT]
        end
        
        subgraph "Reconstructors Registry"
            R1[Direct]
            R2[RLE Decoder]
            R3[Differential Decoder]
            R4[Huffman Decoder]
            R5[Sparse Interpolator]
            R6[DCT Inverse]
        end
        
        COMP --> C1 & C2 & C3 & C4 & C5 & C6
        RECON --> R1 & R2 & R3 & R4 & R5 & R6
    end
    
    subgraph "Data Layer"
        IMG[Image Utils]
        CONFIG[Configuration]
        CACHE[Cache Manager]
    end
    
    subgraph "External Services"
        OPENROUTER[OpenRouter API]
        LLM[LLM Models]
        OPENROUTER --> LLM
    end
    
    CLI --> COMP
    CLI --> RECON
    CLI --> METRICS
    
    UI --> COMP
    UI --> RECON
    UI --> METRICS
    UI --> OPENROUTER
    
    COMP --> IMG
    RECON --> IMG
    
    UI --> CONFIG
    UI --> CACHE
    
    METRICS --> COMP
    METRICS --> RECON
    
    style CLI fill:#667eea
    style UI fill:#764ba2
    style COMP fill:#f093fb
    style RECON fill:#4facfe
    style METRICS fill:#43e97b
    style OPENROUTER fill:#fa709a
```

**Description**: High-level system architecture showing the main components:
- **User Interfaces**: CLI and Streamlit UI as entry points
- **Core Engine**: Compression/reconstruction algorithms and metrics
- **Data Layer**: Utilities for data handling
- **External Services**: LLM integration via OpenRouter

---

## 📊 Diagram 2: Compression & Reconstruction Workflow

```mermaid
flowchart LR
    subgraph "Input"
        A[2D Image<br/>64×64 pixels<br/>4,096 bytes]
    end
    
    subgraph "Encoding Phase"
        B[Preprocessing<br/>• Grayscale<br/>• Normalize<br/>• Extract metadata]
        C{Select<br/>Method}
        
        C -->|Uniform regions| D1[RLE<br/>4-10x compression]
        C -->|Smooth gradients| D2[Differential<br/>2-5x compression]
        C -->|General purpose| D3[Huffman<br/>1.5-3x compression]
        C -->|Quick preview| D4[Sparse<br/>10-50x compression]
        C -->|Natural photos| D5[DCT<br/>5-20x compression]
        C -->|Baseline| D6[Naive<br/>1.0x no compression]
        
        D1 & D2 & D3 & D4 & D5 & D6 --> E[1D Byte Stream<br/>+ Metadata]
    end
    
    subgraph "Transmission/Storage"
        F[Compressed Data<br/>256-4096 bytes<br/>Serialized format]
    end
    
    subgraph "Decoding Phase"
        G[Read Metadata<br/>Extract method<br/>& parameters]
        H{Route to<br/>Reconstructor}
        
        H -->|RLE| I1[RLE Decoder<br/>Expand runs]
        H -->|Differential| I2[Cumulative Sum<br/>Integrate diffs]
        H -->|Huffman| I3[Huffman Decoder<br/>Bit-by-bit decode]
        H -->|Sparse| I4[Interpolation<br/>Fill missing pixels]
        H -->|DCT| I5[Inverse DCT<br/>Frequency→Spatial]
        H -->|Naive| I6[Direct Reshape<br/>No processing]
        
        I1 & I2 & I3 & I4 & I5 & I6 --> J[Reshape to 2D<br/>Postprocess]
    end
    
    subgraph "Output"
        K[2D Image<br/>64×64 pixels<br/>Reconstructed]
    end
    
    subgraph "Quality Analysis"
        L[Metrics<br/>• PSNR<br/>• SSIM<br/>• MSE<br/>• Entropy<br/>• Compression Ratio]
    end
    
    A --> B --> C
    E --> F --> G --> H
    J --> K
    A -.Compare.-> L
    K -.Compare.-> L
    
    style A fill:#ffadad
    style E fill:#ffd6a5
    style F fill:#fdffb6
    style K fill:#caffbf
    style L fill:#9bf6ff
    style C fill:#bdb2ff
    style H fill:#ffc6ff
```

**Description**: Complete data flow from input to output:
1. **Input**: Original 2D image
2. **Encoding**: Multiple compression methods available
3. **Transmission**: 1D byte stream (simulated wire)
4. **Decoding**: Method-specific reconstruction
5. **Output**: Reconstructed 2D image
6. **Analysis**: Quality metrics comparing input/output

---

## 📊 Diagram 3: Information Theory Metrics Flow

```mermaid
graph TD
    subgraph "Original Image Analysis"
        A[Original Image<br/>H × W pixels]
        B[Calculate Entropy<br/>H = -Σ p·log₂p]
        C[Theoretical Minimum<br/>Min bits = H × pixels]
        A --> B --> C
    end
    
    subgraph "Compression Analysis"
        D[Compressed Data<br/>N bytes]
        E[Calculate<br/>• Bits per pixel<br/>• Compression ratio<br/>• Space saved]
        F[Efficiency<br/>η = Theoretical/Actual]
        D --> E --> F
    end
    
    subgraph "Quality Analysis"
        G[Original vs<br/>Reconstructed]
        H[PSNR<br/>10·log₁₀MAX²/MSE]
        I[SSIM<br/>Structural Similarity]
        J[MSE<br/>Mean Squared Error]
        G --> H & I & J
    end
    
    subgraph "Shannon's Limits"
        K{Is Lossless?}
        K -->|Yes| L[PSNR = ∞<br/>Perfect reconstruction<br/>Cannot compress below H]
        K -->|No| M[PSNR finite<br/>Rate-distortion tradeoff<br/>Quality vs Size]
    end
    
    subgraph "Results Dashboard"
        N[Comprehensive Report<br/>• Entropy reduction<br/>• Compression efficiency<br/>• Quality metrics<br/>• Theoretical vs actual]
    end
    
    C --> F
    F --> N
    H & I & J --> K
    K --> N
    L --> N
    M --> N
    
    style B fill:#ff6b6b
    style C fill:#ee5a6f
    style F fill:#4ecdc4
    style H fill:#95e1d3
    style I fill:#f38181
    style K fill:#aa96da
    style N fill:#fcbad3
```

**Description**: Information theory metrics calculation and Shannon's theoretical bounds:
- **Entropy**: Sets theoretical compression limit
- **Efficiency**: How close algorithm is to theoretical optimum
- **Quality Metrics**: Quantify reconstruction quality
- **Shannon's Limits**: Distinguish lossless vs lossy compression

---

## 📊 Diagram 4: Streamlit UI State Management

```mermaid
stateDiagram-v2
    [*] --> Settings: Launch App
    
    Settings --> Settings: Configure algorithms<br/>Set API keys<br/>Adjust parameters
    
    Settings --> Encode: Navigate
    
    Encode --> Encode: Upload image<br/>Select method<br/>Compress
    
    state Encode {
        [*] --> Idle
        Idle --> Compressing: Click Compress
        Compressing --> ShowResults: Success
        ShowResults --> Idle: Reset
        Compressing --> Error: Failure
        Error --> Idle: Retry
    }
    
    Encode --> Decode: Auto-pass data<br/>via session_state
    
    state Decode {
        [*] --> CheckData
        CheckData --> Ready: Data available
        CheckData --> WaitingForData: No data
        WaitingForData --> CheckData: Return to Encode
        Ready --> Reconstructing: Click Reconstruct
        Reconstructing --> ShowQuality: Success
        ShowQuality --> Ready: Reset
    }
    
    Decode --> Diff: Auto-pass data
    
    state Diff {
        [*] --> Analyzing
        Analyzing --> VisualTab: View visuals
        Analyzing --> StatsTab: View statistics
        Analyzing --> TheoryTab: View theory
        Analyzing --> ReportTab: Generate report
        VisualTab --> DownloadReport
        StatsTab --> DownloadReport
        TheoryTab --> DownloadReport
        ReportTab --> DownloadReport
    }
    
    Diff --> Summarize: Optional
    
    state Summarize {
        [*] --> CheckLLM
        CheckLLM --> LLMReady: API configured
        CheckLLM --> ConfigureAPI: Not configured
        ConfigureAPI --> CheckLLM: Settings updated
        LLMReady --> Generating: Request report
        Generating --> ShowReport: Success
        ShowReport --> [*]
    }
    
    Summarize --> Settings: Configure LLM
    
    note right of Encode
        session_state.encoded_data = {
            'original': image,
            'compressed_bytes': bytes,
            'metadata': dict,
            'stats': dict,
            'method': str
        }
    end note
    
    note right of Decode
        session_state.reconstructed_data = {
            'image': reconstructed,
            'method': str,
            'stats': dict,
            'elapsed_time': float
        }
    end note
```

**Description**: Streamlit UI state transitions and data flow:
- **Settings**: Global configuration (persists in session_state)
- **Encode**: Compression with state management
- **Decode**: Reconstruction using encoded data from session
- **Diff**: Analysis using both encoded and decoded data
- **Summarize**: LLM report generation (optional)

---

## 📊 Diagram 5: Extensibility Architecture

```mermaid
classDiagram
    class Compressor {
        <<abstract>>
        +compress(data) Tuple~bytes, dict~
        +get_stats() dict
        #params dict
        #stats dict
    }
    
    class Reconstructor {
        <<abstract>>
        +reconstruct(bytes, metadata) Any
        +get_stats() dict
        #params dict
        #stats dict
    }
    
    class ImageCompressor {
        #_preprocess_image(image)
        #_create_metadata() dict
        #original_shape tuple
        #original_dtype type
    }
    
    class ImageReconstructor {
        #_postprocess_image(image, metadata)
    }
    
    class AudioCompressor {
        <<future>>
        #_preprocess_audio(audio)
        #_create_metadata() dict
    }
    
    class AudioReconstructor {
        <<future>>
        #_postprocess_audio(audio, metadata)
    }
    
    class TextCompressor {
        <<future>>
        #_preprocess_text(text)
        #_create_metadata() dict
    }
    
    class TextReconstructor {
        <<future>>
        #_postprocess_text(text, metadata)
    }
    
    class NaiveCompressor {
        +compress(data)
    }
    
    class RLECompressor {
        +compress(data)
    }
    
    class HuffmanCompressor {
        +compress(data)
        -_build_huffman_tree()
        -_generate_codes()
    }
    
    class DirectReconstructor {
        +reconstruct(bytes, metadata)
    }
    
    class RLEReconstructor {
        +reconstruct(bytes, metadata)
    }
    
    class HuffmanReconstructor {
        +reconstruct(bytes, metadata)
    }
    
    Compressor <|-- ImageCompressor
    Compressor <|-- AudioCompressor
    Compressor <|-- TextCompressor
    
    Reconstructor <|-- ImageReconstructor
    Reconstructor <|-- AudioReconstructor
    Reconstructor <|-- TextReconstructor
    
    ImageCompressor <|-- NaiveCompressor
    ImageCompressor <|-- RLECompressor
    ImageCompressor <|-- HuffmanCompressor
    
    ImageReconstructor <|-- DirectReconstructor
    ImageReconstructor <|-- RLEReconstructor
    ImageReconstructor <|-- HuffmanReconstructor
    
    note for Compressor "Abstract base for all media types"
    note for ImageCompressor "Current: 6 implementations"
    note for AudioCompressor "Phase 2: Future implementation"
    note for TextCompressor "Phase 3: Future implementation"
```

**Description**: Class hierarchy showing extensibility design:
- **Abstract Base Classes**: Media-agnostic interfaces
- **Image Classes**: Current implementations (6 compressors)
- **Audio/Text Classes**: Future extensions (architecture ready)
- **Inheritance**: Clear separation of concerns

---

## 📊 Diagram 6: CLI Command Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI as infocodec CLI
    participant Detector as Media Detector
    participant Compressor
    participant File as File System
    participant Reconstructor
    participant Metrics
    
    Note over User,Metrics: Encode Command
    User->>CLI: infocodec encode --input image.png --method auto
    CLI->>Detector: detect_media_type(image.png)
    Detector-->>CLI: "image"
    CLI->>CLI: _auto_select_method()
    Note right of CLI: Analyzes entropy,<br/>unique values,<br/>std dev
    CLI-->>CLI: Selected: huffman
    CLI->>Compressor: HuffmanCompressor.compress(image)
    Compressor-->>CLI: (compressed_bytes, metadata)
    CLI->>File: Write .dat file with metadata header
    CLI->>File: Write .json metadata file
    File-->>User: compressed.dat + metadata.json
    
    Note over User,Metrics: Decode Command
    User->>CLI: infocodec decode --input compressed.dat
    CLI->>File: Read metadata from .dat header
    File-->>CLI: metadata dict
    CLI->>CLI: Extract method from metadata
    CLI->>Reconstructor: HuffmanReconstructor.reconstruct()
    Reconstructor-->>CLI: reconstructed_image
    CLI->>File: Save as .png
    File-->>User: reconstructed.png
    
    Note over User,Metrics: Benchmark Command
    User->>CLI: infocodec benchmark --input image.png --methods all
    
    loop For each method
        CLI->>Compressor: compress(image)
        Compressor-->>CLI: (bytes, metadata)
        CLI->>Metrics: calculate_stats()
        Metrics-->>CLI: compression_ratio, entropy, etc.
    end
    
    CLI->>CLI: Format as table/JSON/markdown
    CLI-->>User: Comparison report
    
    Note over User,Metrics: UI Command
    User->>CLI: infocodec-ui
    CLI->>CLI: Launch streamlit
    activate CLI
    Note right of CLI: Opens browser<br/>to localhost:8501
    CLI-->>User: Streamlit interface running
    deactivate CLI
```

**Description**: Sequence diagram showing CLI command execution:
1. **Encode**: Auto-detection → Compression → File save
2. **Decode**: Metadata read → Reconstruction → Image save
3. **Benchmark**: Multiple compressions → Comparison
4. **UI**: Launch Streamlit server

---

## 📊 Diagram 7: Test Coverage Map

```mermaid
mindmap
    root((Test Suite<br/>40+ Tests))
        Compressors
            Registry
                All methods registered
                Correct mapping
            Naive
                Basic compression
                1.0x ratio
                Perfect quality
            RLE
                Blocks compression high
                Noise expansion
                Metadata complete
            Differential
                Entropy reduction
                Gradient performance
                Signed integers
            Huffman
                Efficiency >90%
                Code table valid
                Round-trip perfect
            Sparse
                Sampling rates
                Interpolation quality
                Compression high
            DCT
                Quality levels
                Block processing
                Frequency domain
        Reconstructors
            Round-trip
                Lossless perfect
                Lossy acceptable
                Shape preserved
            Registry
                All methods mapped
                Correct routing
            Quality
                PSNR checks
                SSIM validation
                MSE calculation
            Edge Cases
                Empty images
                Single pixel
                Corrupted data
        Metrics
            Entropy
                Bounds 0-8
                Uniform 0
                Random 8
            PSNR
                Identical infinite
                Different finite
                Noise correlation
            SSIM
                Bounds 0-1
                Identity 1.0
                Structure sensitive
            Compression
                Ratio calculation
                BPP calculation
                Efficiency formula
            Comprehensive
                All keys present
                Lossless detection
                Lossy analysis
```

**Description**: Mind map of test coverage:
- **Compressors**: All 6 methods tested thoroughly
- **Reconstructors**: Round-trip and quality validation
- **Metrics**: Shannon entropy, PSNR, SSIM, efficiency
- **Edge Cases**: Empty, single-pixel, corrupted data

---

## 🎨 How to Use These Diagrams

### In Documentation
Copy the mermaid code blocks into:
- GitHub README.md (renders automatically)
- Documentation sites (GitBook, ReadTheDocs, etc.)
- Jupyter notebooks (with mermaid extension)

### In Presentations
1. Render diagrams using:
   - Mermaid Live Editor: https://mermaid.live
   - VS Code Mermaid extension
   - GitHub markdown preview

2. Export as PNG/SVG for:
   - PowerPoint presentations
   - Academic papers
   - Project proposals

### For Development
- **Architecture Planning**: Reference during design discussions
- **Onboarding**: Help new contributors understand structure
- **Debugging**: Trace data flow through system
- **Documentation**: Keep diagrams updated with code changes

---

## 📝 Diagram Maintenance

### When to Update

**Diagram 1 (System Architecture)**: When adding new major components
**Diagram 2 (Workflow)**: When adding new compression methods
**Diagram 3 (Metrics)**: When adding new metrics
**Diagram 4 (UI State)**: When adding new pages
**Diagram 5 (Extensibility)**: When adding new base classes
**Diagram 6 (CLI Flow)**: When changing CLI commands
**Diagram 7 (Test Coverage)**: After adding new tests

### Quick Edit Guide

```bash
# Edit this file
vim DIAGRAMS.md

# Preview in VS Code (install Mermaid extension)
code DIAGRAMS.md

# Render online
# Copy code block → https://mermaid.live

# Commit changes
git add DIAGRAMS.md
git commit -m "Update architecture diagrams"
```

---

## 🎓 Educational Use

These diagrams are perfect for:

1. **Teaching Information Theory**
   - Show Diagram 3 for Shannon's metrics
   - Use Diagram 2 for compression workflow

2. **Software Architecture Courses**
   - Diagram 1 for system design
   - Diagram 5 for extensibility patterns

3. **Research Presentations**
   - Diagram 2 for methodology
   - Diagram 3 for theoretical framework

4. **Project Documentation**
   - All diagrams for comprehensive docs
   - Diagram 6 for user guide

---

*These diagrams visualize the complete Shannon Portrait architecture, from high-level system design to detailed workflows and test coverage.*

**Shannon Portrait - Information Coding & Encoding**
**Built with Claude (Anthropic) • February 2025**


readme = '''<div align="center">

# 🎵 Generative Music Visualizer

**Real-time audio-reactive visuals that dance to your music.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-ff69b4?logo=pygame)](https://pygame.org)
[![Librosa](https://img.shields.io/badge/Librosa-0.10%2B-orange)](https://librosa.org)

<img src="https://via.placeholder.com/800x450/0a0a1a/00d4ff?text=Generative+Music+Visualizer+Demo" width="700" alt="Demo Preview">

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-controls">Controls</a> •
  <a href="#-modes">Modes</a> •
  <a href="#-customization">Customize</a>
</p>

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 5 Generative Modes
- **Frequency Bars** — Classic spectrum with reflections
- **Circular Spectrum** — Rotating radial ring
- **Particle Burst** — Physics-driven particle systems
- **Waveform Ring** — 3D perspective with trails
- **Neural Mesh** — Dynamic node network graph

</td>
<td width="50%">

### 🎛️ Audio Engine
- Real-time FFT analysis (64 frequency bands)
- Automatic beat detection & tempo sync
- Log-spaced frequency binning
- Exponential smoothing for fluid motion
- Support for MP3, WAV, FLAC, OGG

</td>
</tr>
<tr>
<td width="50%">

### 🎮 Interactive Controls
- Switch modes instantly (1–5)
- Pause / resume playback
- Toggle fullscreen
- Adjust sensitivity on the fly
- Progress bar with seek preview

</td>
<td width="50%">

### 🌈 Visual Polish
- 5 auto-rotating color palettes
- Beat-triggered particle explosions
- Motion trails & ghosting effects
- Alpha-blended connections
- Responsive window resizing

</td>
</tr>
</table>

---

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **ffmpeg** (for MP3 support)

<details>
<summary>📋 Install ffmpeg (click to expand)</summary>

| OS | Command |
|----|---------|
| **macOS** | `brew install ffmpeg` |
| **Ubuntu/Debian** | `sudo apt-get install ffmpeg` |
| **Windows** | [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |
| **Conda** | `conda install -c conda-forge ffmpeg` |

</details>

### Install Python Dependencies

```bash
pip install pygame numpy librosa
```

Or clone and install from requirements:

```bash
git clone https://github.com/yourusername/generative-music-visualizer.git
cd generative-music-visualizer
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run with a song

```bash
python music_visualizer.py path/to/your_song.mp3
```

### Interactive mode (prompts for file)

```bash
python music_visualizer.py
```

### Drag & drop (Windows)

Drag any audio file onto `music_visualizer.py`.

---

## 🎮 Controls

| Key | Action | Description |
|:---:|:-------|:------------|
| `1` | **Frequency Bars** | Classic vertical spectrum bars |
| `2` | **Circular Spectrum** | Rotating ring visualization |
| `3` | **Particle Burst** | Particle system driven by audio |
| `4` | **Waveform Ring** | 3D ring with motion trails |
| `5` | **Neural Mesh** | Connected node network |
| `SPACE` | ⏯️ Pause / Resume | Toggle playback |
| `F` | 🖥️ Fullscreen | Toggle fullscreen mode |
| `+` | 🔼 Sensitivity Up | More reactive visuals |
| `-` | 🔽 Sensitivity Down | Smoother visuals |
| `ESC` | ❌ Quit | Exit application |

---

## 🎨 Modes

<details open>
<summary><b>1️⃣ Frequency Bars</b></summary>

<img src="https://via.placeholder.com/700x200/0a0a1a/ff0055?text=Frequency+Bars+Preview" width="100%">

Classic spectrum analyzer with 64 log-spaced frequency bands.
- Reflections below the baseline
- White peak indicators
- Beat-triggered screen flash & particles
- Best for: **Bass-heavy electronic music**

</details>

<details>
<summary><b>2️⃣ Circular Spectrum</b></summary>

<img src="https://via.placeholder.com/700x200/0a0a1a/aa00ff?text=Circular+Spectrum+Preview" width="100%">

Rotating ring where frequency magnitude pushes points outward.
- Continuous rotation synced to amplitude
- Inner/outer ring with radial lines
- Center glow orb pulsing to bass
- Best for: **Rhythmic / melodic tracks**

</details>

<details>
<summary><b>3️⃣ Particle Burst</b></summary>

<img src="https://via.placeholder.com/700x200/0a0a1a/00d4ff?text=Particle+Burst+Preview" width="100%">

Purely particle-driven with gravity and trails.
- Particles emit from frequency band positions
- Central orb grows with bass energy
- Radial bursts on detected beats
- Best for: **High-energy / fast tempo songs**

</details>

<details>
<summary><b>4️⃣ Waveform Ring</b></summary>

<img src="https://via.placeholder.com/700x200/0a0a1a/00ff88?text=Waveform+Ring+Preview" width="100%">

3D-perspective rotating ring with ghost trails.
- 20-frame motion trail history
- Perspective flattening (y-axis scaled)
- Brightest ring with white outline
- Best for: **Ambient / progressive tracks**

</details>

<details>
<summary><b>5️⃣ Neural Mesh</b></summary>

<img src="https://via.placeholder.com/700x200/0a0a1a/ffaa00?text=Neural+Mesh+Preview" width="100%">

Dynamic network graph of 50 connected nodes.
- Nodes jitter to corresponding frequencies
- Proximity-based alpha-blended connections
- Node size scales with intensity
- Best for: **Complex / layered compositions**

</details>

---

## ⚙️ Customization

Edit constants at the top of `music_visualizer.py`:

```python
# Display
WIDTH, HEIGHT = 1280, 720    # Default window resolution
FPS = 60                     # Target frame rate

# Audio
N_BARS = 64                  # Number of frequency bands (more = smoother)
SMOOTHING = 0.15             # Spectrum smoothing (0.0 = raw, 1.0 = frozen)
DEFAULT_SENSITIVITY = 1.5    # Default reactivity multiplier

# Colors — add your own palettes!
PALETTES = [
    [(255, 0, 128), (128, 0, 255), (0, 128, 255), (0, 255, 128)],    # Neon
    [(255, 100, 0), (255, 200, 0), (255, 50, 100), (200, 0, 255)],    # Sunset
    # ... add more RGB tuples
]
```

---

## 🖥️ System Requirements

| | Minimum | Recommended |
|:---|:---|:---|
| **Python** | 3.8 | 3.11+ |
| **CPU** | Dual-core | Quad-core |
| **RAM** | 2 GB | 4 GB |
| **GPU** | Integrated | Dedicated (for 1080p fullscreen) |
| **OS** | Windows 10 / macOS 10.14 / Linux | Latest |

---

## 🧪 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Audio File    │────▶│  Librosa Load    │────▶│ Beat Detection  │
│  (MP3/WAV/FLAC) │     │  (22,050 Hz)     │     │  & Onset Track  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                         │
┌─────────────────┐     ┌──────────────────┐            ▼
│   Pygame Mixer  │◀────│  FFT + Window    │◀─────── Playback
│   (Playback)    │     │  (Real-time)     │            │
└─────────────────┘     └──────────────────┘            │
       │                         │                      │
       │                         ▼                      │
       │                ┌──────────────────┐            │
       │                │ 64 Log Bins      │            │
       │                │ Smooth + Compress│            │
       │                └──────────────────┘            │
       │                         │                      │
       ▼                         ▼                      ▼
┌──────────────────────────────────────────────────────────────┐
│                      Visualizer Modes                         │
│  Frequency Bars │ Circular │ Particles │ Wave Ring │ Mesh   │
└──────────────────────────────────────────────────────────────┘
```

1. **Load** — Librosa decodes audio and pre-computes beat times
2. **Play** — Pygame mixer streams audio
3. **Sync** — Playback position aligns the FFT analysis window
4. **Analyze** — Hanning-windowed STFT → log-spaced magnitude bins
5. **Smooth** — Exponential moving average prevents visual jitter
6. **Render** — Spectrum drives geometry, colors, particles, and beat effects

---

## 🐛 Troubleshooting

<details>
<summary><b>FileNotFoundError</b></summary>

Ensure the path is correct. Wrap paths with spaces in quotes:
```bash
python music_visualizer.py "/path/to/my song.mp3"
```
</details>

<details>
<summary><b>NoBackendError (Librosa cannot load MP3)</b></summary>

Install ffmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows — download from https://ffmpeg.org/download.html
```
</details>

<details>
<summary><b>Low FPS / Laggy visuals</b></summary>

- Reduce `N_BARS` from 64 to 32
- Avoid particle-heavy modes (3 & 5) on low-end hardware
- Close other applications
- Run in windowed mode instead of fullscreen
</details>

<details>
<summary><b>Audio-visual desync</b></summary>

- Reduce `chunk_size` in `AudioProcessor.__init__`
- Ensure no heavy background processes are running
- Try a different audio file format (WAV has lowest latency)
</details>

---

## 📁 Project Structure

```
generative-music-visualizer/
├── music_visualizer.py      # Main application (single file!)
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── assets/
    └── demo.gif             # Demo animation (optional)
```

---

## 🔮 Roadmap

- [ ] 🎥 **Video Export** — Save visualizations as MP4
- [ ] 🎤 **Live Input** — Microphone / line-in support
- [ ] 🎛️ **MIDI Control** — Map modes to MIDI controllers
- [ ] 🎨 **Palette Editor** — GUI for custom color schemes
- [ ] 📂 **Playlist Mode** — Auto-transition between songs
- [ ] 🥽 **VR Support** — 360° / stereoscopic rendering

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs via [Issues](https://github.com/yourusername/generative-music-visualizer/issues)
- 💡 Suggest new visualization modes
- 🔧 Submit pull requests
- ⭐ Star the repo if you like it!

### Development Setup

```bash
git clone https://github.com/yourusername/generative-music-visualizer.git
cd generative-music-visualizer
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python music_visualizer.py demo.mp3
```

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgements

- **[Librosa](https://librosa.org/)** — Audio analysis & music information retrieval
- **[Pygame](https://www.pygame.org/)** — Cross-platform graphics & audio
- **[NumPy](https://numpy.org/)** — Fast numerical computing

---

<div align="center">

**Made with 💜 and Python.**

If this project helped you, please consider giving it a ⭐!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/generative-music-visualizer?style=social)](https://github.com/yourusername/generative-music-visualizer/stargazers)

</div>
'''

# Also create requirements.txt
requirements = '''pygame>=2.5.0
numpy>=1.24.0
librosa>=0.10.0
'''

with open("/mnt/agents/output/README.md", "w") as f:
    f.write(readme)

with open("/mnt/agents/output/requirements.txt", "w") as f:
    f.write(requirements)

print("✅ README.md saved")
print("✅ requirements.txt saved")
print(f"📏 README: {len(readme)} chars")

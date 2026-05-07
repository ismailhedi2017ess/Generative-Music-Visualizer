# Generative-Music-Visualizer
🎵 Generative Music Visualizer
A real-time, audio-reactive music visualizer built in Python. It analyzes audio frequencies, detects beats, and generates stunning generative visuals that dance to your music.
 Demo 

 License 
✨ Features
Table
Feature	Description
5 Visualization Modes	Frequency Bars, Circular Spectrum, Particle Burst, Waveform Ring, Neural Mesh
Real-Time Audio Analysis	Uses Librosa for FFT, spectrogram, and onset detection
Beat Detection	Automatically syncs visuals to song tempo and beats
Particle Systems	Reactive particles that burst on beats and frequency peaks
Dynamic Color Palettes	5 auto-rotating palettes: Neon, Sunset, CMYK, Monochrome, Primary
Smooth Interpolation	Exponential smoothing for fluid, non-jittery motion
Fullscreen & Resizable	Toggle fullscreen or resize the window freely
Sensitivity Control	Adjust reactivity on the fly
📦 Requirements
Python 3.8 or higher
Pygame — Graphics & audio playback
Librosa — Audio analysis & beat detection
NumPy — Numerical computations
Install Dependencies
bash
Copy
pip install pygame numpy librosa
Note: Librosa requires ffmpeg or libsndfile for MP3 support. If you get audio loading errors:
macOS: brew install ffmpeg
Ubuntu/Debian: sudo apt-get install ffmpeg
Windows: Download from ffmpeg.org and add to PATH
🚀 Quick Start
Run with an audio file
bash
Copy
python music_visualizer.py path/to/your_song.mp3
Run without arguments (interactive prompt)
bash
Copy
python music_visualizer.py
Then paste or type the path to your audio file when prompted.
Supported Formats
.mp3
.wav
.flac
.ogg
Any format supported by Librosa / SoundFile
🎮 Controls
Table
Key	Action
1	Frequency Bars — Classic vertical bars with reflections
2	Circular Spectrum — Rotating ring with radial lines
3	Particle Burst — Particles emit from frequency bands
4	Waveform Ring — 3D-perspective rotating ring with trails
5	Neural Mesh — Dynamic network of connected nodes
SPACE	Pause / Resume playback
F	Toggle fullscreen mode
+	Increase sensitivity (more reactive)
-	Decrease sensitivity (less reactive)
ESC	Quit the visualizer
🎨 Visualization Modes
1. Frequency Bars
Classic spectrum analyzer. 64 vertical bars represent log-spaced frequency bands from bass to treble. Features:
Reflections below the baseline
White peak indicators
Beat-triggered screen flash
Particle explosion on strong beats
2. Circular Spectrum
A rotating ring visualization where frequency magnitude pushes points outward. Features:
Continuous rotation synced to audio amplitude
Inner/outer ring with connecting radial lines
Center glow orb that pulses with bass
Polygon fill with outline
3. Particle Burst
A purely particle-driven mode. Features:
Particles emit from each frequency band's position around a circle
Central orb grows with bass energy
Beat-triggered radial particle bursts
Long particle trails with gravity simulation
4. Waveform Ring
A rotating ring with 3D perspective and motion trails. Features:
20-frame history creates ghost trails
Perspective flattening (y-axis scaled to 0.6)
Brightest current ring with white outline
Beat-triggered expanding ring
5. Neural Mesh
A network graph of 50 nodes that react to the music. Features:
Nodes attracted to their base positions with music-driven jitter
Proximity-based connections with alpha blending
Connection color derived from corresponding frequency band
Node size scales with frequency intensity
🧪 How It Works
Audio Pipeline
Load — Librosa loads audio at 22,050 Hz mono
Analyze — Beat tracking and onset strength computed upfront
Stream — Pygame mixer plays audio while visualizer runs
Sync — Visualizer queries playback position to align FFT window
FFT — Real-time Short-Time Fourier Transform with Hanning window
Bin — Log-spaced frequency aggregation into 64 bands
Smooth — Exponential moving average prevents jitter
Rendering Pipeline
Fade — Semi-transparent overlay creates motion trails
React — Spectrum data drives geometry, colors, and particles
Beat — Pre-computed beat times trigger particle bursts
Composite — UI overlay (mode name, controls, progress bar)
⚙️ Configuration
Edit these constants at the top of music_visualizer.py:
Python
Copy
WIDTH, HEIGHT = 1280, 720    # Default window size
FPS = 60                     # Target frame rate
N_BARS = 64                  # Number of frequency bands
SMOOTHING = 0.15             # Spectrum smoothing factor (0-1)
DEFAULT_SENSITIVITY = 1.5    # Default reactivity multiplier
Color Palettes
Add or modify palettes in the PALETTES list:
Python
Copy
PALETTES = [
    [(255, 0, 128), (128, 0, 255), (0, 128, 255), (0, 255, 128)],    # Neon
    # Add your own RGB tuples here...
]
🖥️ System Requirements
Table
Component	Minimum	Recommended
CPU	Dual-core	Quad-core
RAM	2 GB	4 GB
GPU	Integrated	Dedicated (for fullscreen 1080p)
OS	Windows 10 / macOS 10.14 / Linux	Latest
🐛 Troubleshooting
Table
Issue	Solution
FileNotFoundError	Check that the audio file path is correct and quoted if it contains spaces
NoBackendError (Librosa)	Install ffmpeg (see Requirements section)
Low frame rate	Reduce N_BARS or disable particle-heavy modes (3, 5)
Audio out of sync	Close other heavy applications; reduce chunk_size in AudioProcessor
Black screen	Ensure your audio file isn't corrupted; try a different format
📁 Project Structure
plain
Copy
music_visualizer/
├── music_visualizer.py    # Main application
├── README.md              # This file
└── your_music/
    └── song.mp3
🔮 Future Ideas
[ ] Export visualizations to video (MP4)
[ ] Microphone / live audio input mode
[ ] Custom palette editor
[ ] VR / 360° mode
[ ] MIDI controller integration
[ ] Playlist support with auto-transition
📜 License
MIT License — feel free to use, modify, and distribute.
🙏 Credits
Librosa — Audio analysis
Pygame — Graphics & audio playback
NumPy — Fast numerical computing

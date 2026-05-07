#!/usr/bin/env python3
"""
Generative Music Visualizer
============================
A real-time audio-reactive visualizer with multiple generative modes:
  - Frequency Bars
  - Circular Spectrum
  - Particle Burst
  - Waveform Ring
  - Neural Mesh

Requirements:
    pip install pygame numpy librosa

Usage:
    python music_visualizer.py <audio_file.mp3>
    or just run it and it will prompt for a file.

Controls:
    1-5      : Switch visualization modes
    SPACE    : Pause/Resume
    F        : Toggle fullscreen
    +/-      : Adjust sensitivity
    ESC      : Quit
"""

import sys
import math
import random
import os

try:
    import numpy as np
except ImportError:
    print("Installing numpy...")
    os.system(f"{sys.executable} -m pip install numpy")
    import numpy as np

try:
    import pygame
    from pygame import gfxdraw
except ImportError:
    print("Installing pygame...")
    os.system(f"{sys.executable} -m pip install pygame")
    import pygame
    from pygame import gfxdraw

try:
    import librosa
except ImportError:
    print("Installing librosa...")
    os.system(f"{sys.executable} -m pip install librosa")
    import librosa

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
FPS = 60
N_BARS = 64
SMOOTHING = 0.15
DEFAULT_SENSITIVITY = 1.5

# Color palettes (RGB tuples)
PALETTES = [
    [(255, 0, 128), (128, 0, 255), (0, 128, 255), (0, 255, 128)],    # Neon
    [(255, 100, 0), (255, 200, 0), (255, 50, 100), (200, 0, 255)],    # Sunset
    [(0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0)],       # CMYK
    [(255, 255, 255), (200, 200, 200), (150, 150, 150), (100, 100, 255)], # Monochrome
    [(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50)],    # Primary
]

# ---------------------------------------------------------------------------
# Audio Processor
# ---------------------------------------------------------------------------
class AudioProcessor:
    def __init__(self, filepath, chunk_size=1024):
        self.filepath = filepath
        self.chunk_size = chunk_size
        self.sample_rate = 22050

        print(f"Loading audio: {filepath}")
        self.y, self.sr = librosa.load(filepath, sr=self.sample_rate, mono=True)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)

        # Beat tracking
        print("Analyzing beats...")
        self.tempo, self.beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.beat_times = librosa.frames_to_time(self.beat_frames, sr=self.sr)
        self.beat_idx = 0

        # Onset strength for beat detection
        self.onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)

        # Normalization
        self.y = self.y / (np.max(np.abs(self.y)) + 1e-8)

        self.position = 0
        self.is_playing = False

        # Pygame mixer setup
        pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=chunk_size)
        pygame.mixer.music.load(filepath)

    def start(self):
        pygame.mixer.music.play()
        self.is_playing = True
        self.start_tick = pygame.time.get_ticks()

    def get_current_time(self):
        if not self.is_playing:
            return 0
        return pygame.mixer.music.get_pos() / 1000.0

    def get_spectrum(self):
        """Returns frequency magnitudes and beat detection info."""
        t = self.get_current_time()
        if t <= 0:
            return np.zeros(N_BARS), 0.0, False

        # Convert time to sample index
        sample_idx = int(t * self.sr)
        start = max(0, sample_idx - self.chunk_size // 2)
        end = min(len(self.y), start + self.chunk_size)

        if end - start < self.chunk_size:
            chunk = np.zeros(self.chunk_size)
            chunk[:end-start] = self.y[start:end]
        else:
            chunk = self.y[start:end]

        # Windowed FFT
        window = np.hanning(len(chunk))
        fft = np.fft.rfft(chunk * window)
        magnitudes = np.abs(fft)

        # Log-spaced frequency bins
        freqs = np.fft.rfftfreq(len(chunk), 1/self.sr)
        log_bins = np.logspace(np.log10(20), np.log10(freqs[-1]+1), N_BARS+1)

        binned = np.zeros(N_BARS)
        for i in range(N_BARS):
            mask = (freqs >= log_bins[i]) & (freqs < log_bins[i+1])
            if np.any(mask):
                binned[i] = np.mean(magnitudes[mask])

        # Normalize
        binned = binned / (np.max(binned) + 1e-8)
        binned = np.power(binned, 0.6)  # Compress dynamic range

        # Overall amplitude
        amplitude = np.mean(np.abs(chunk))

        # Beat detection
        is_beat = False
        if self.beat_idx < len(self.beat_times):
            if t >= self.beat_times[self.beat_idx]:
                is_beat = True
                self.beat_idx += 1

        return binned, amplitude, is_beat

    def is_finished(self):
        return not pygame.mixer.music.get_busy() and self.is_playing

# ---------------------------------------------------------------------------
# Particle System
# ---------------------------------------------------------------------------
class Particle:
    def __init__(self, x, y, color, velocity, life, size):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.life = life
        self.max_life = life
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 1
        self.size *= 0.98
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        size = max(1, int(self.size))
        color = tuple(min(255, c) for c in self.color)
        if size > 2:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)
        else:
            pygame.gfxdraw.pixel(surface, int(self.x), int(self.y), color)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, speed=5):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            vel = random.uniform(1, speed)
            vx = math.cos(angle) * vel
            vy = math.sin(angle) * vel
            life = random.randint(20, 60)
            size = random.uniform(2, 8)
            self.particles.append(Particle(x, y, color, (vx, vy), life, size))

    def update_and_draw(self, surface):
        self.particles = [p for p in self.particles if p.update()]
        for p in self.particles:
            p.draw(surface)

# ---------------------------------------------------------------------------
# Visualization Modes
# ---------------------------------------------------------------------------
class VisualizerMode:
    def __init__(self, screen_width, screen_height):
        self.w = screen_width
        self.h = screen_height
        self.smoothed = np.zeros(N_BARS)
        self.particles = ParticleSystem()
        self.palette_idx = 0
        self.palette_timer = 0

    def get_color(self, idx, intensity=1.0):
        palette = PALETTES[self.palette_idx]
        color = palette[idx % len(palette)]
        return tuple(min(255, int(c * intensity)) for c in color)

    def update_palette(self):
        self.palette_timer += 1
        if self.palette_timer > 300:  # Change every 5 seconds
            self.palette_timer = 0
            self.palette_idx = (self.palette_idx + 1) % len(PALETTES)

    def smooth_spectrum(self, spectrum):
        self.smoothed = self.smoothed * (1 - SMOOTHING) + spectrum * SMOOTHING
        return self.smoothed

    def draw(self, surface, spectrum, amplitude, is_beat, sensitivity):
        raise NotImplementedError


class FrequencyBarsMode(VisualizerMode):
    """Classic vertical frequency bars with reflections."""

    def draw(self, surface, spectrum, amplitude, is_beat, sensitivity):
        self.update_palette()
        spec = self.smooth_spectrum(spectrum) * sensitivity

        bar_width = self.w // N_BARS
        cx = self.w // 2

        # Background fade
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        surface.blit(overlay, (0, 0))

        for i in range(N_BARS):
            height = spec[i] * self.h * 0.7
            x = i * bar_width
            y = self.h - height

            color = self.get_color(i, 0.5 + spec[i] * 0.5)

            # Main bar
            pygame.draw.rect(surface, color, (x, y, bar_width - 1, height))

            # Reflection
            refl_color = tuple(c // 3 for c in color)
            pygame.draw.rect(surface, refl_color, (x, self.h, bar_width - 1, height * 0.3))

            # Peak indicator
            peak_y = y - 3
            if peak_y > 0:
                pygame.draw.rect(surface, (255, 255, 255), (x, peak_y, bar_width - 1, 2))

        # Beat flash
        if is_beat:
            flash = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 30))
            surface.blit(flash, (0, 0))
            self.particles.emit(self.w//2, self.h//2, (255, 255, 255), 20, 8)

        self.particles.update_and_draw(surface)


class CircularSpectrumMode(VisualizerMode):
    """Circular spectrum with rotating rings."""

    def __init__(self, w, h):
        super().__init__(w, h)
        self.rotation = 0

    def draw(self, surface, spectrum, amplitude, is_beat, sensitivity):
        self.update_palette()
        spec = self.smooth_spectrum(spectrum) * sensitivity
        self.rotation += 0.005 + amplitude * 0.02

        # Fade background
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((5, 5, 15, 60))
        surface.blit(overlay, (0, 0))

        cx, cy = self.w // 2, self.h // 2
        base_radius = min(cx, cy) * 0.25

        points_outer = []
        points_inner = []

        for i in range(N_BARS):
            angle = self.rotation + (2 * math.pi * i / N_BARS)
            r = base_radius + spec[i] * min(cx, cy) * 0.45

            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r
            points_outer.append((x, y))

            x_in = cx + math.cos(angle) * base_radius * 0.8
            y_in = cy + math.sin(angle) * base_radius * 0.8
            points_inner.append((x_in, y_in))

            # Radial lines
            color = self.get_color(i, 0.6 + spec[i] * 0.4)
            pygame.draw.line(surface, color, (x_in, y_in), (x, y), 2)

        # Draw connecting polygon
        if len(points_outer) > 2:
            color = self.get_color(0, 0.3)
            pygame.draw.polygon(surface, color, points_outer)
            pygame.draw.polygon(surface, self.get_color(2), points_outer, 2)

        # Center glow
        glow_radius = int(base_radius * 0.5 + amplitude * 50)
        for r in range(glow_radius, 0, -5):
            alpha = int(50 * (1 - r / glow_radius))
            color = self.get_color(1)
            pygame.draw.circle(surface, color, (cx, cy), r, 1)

        if is_beat:
            self.particles.emit(cx, cy, self.get_color(0), 30, 10)

        self.particles.update_and_draw(surface)


class ParticleBurstMode(VisualizerMode):
    """Particle system that reacts to each frequency band."""

    def __init__(self, w, h):
        super().__init__(w, h)
        self.band_particles = [[] for _ in range(N_BARS)]

    def draw(self, surface, spectrum, amplitude, is_beat, sensitivity):
        self.update_palette()
        spec = self.smooth_spectrum(spectrum) * sensitivity

        # Dark fade
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 25))
        surface.blit(overlay, (0, 0))

        cx, cy = self.w // 2, self.h // 2

        # Emit particles from frequency bands
        for i in range(N_BARS):
            if spec[i] > 0.3:
                angle = (2 * math.pi * i / N_BARS) - math.pi / 2
                dist = 100 + spec[i] * 200
                px = cx + math.cos(angle) * dist
                py = cy + math.sin(angle) * dist

                color = self.get_color(i, spec[i])
                count = int(spec[i] * 5)
                self.particles.emit(px, py, color, count, spec[i] * 8)

        # Central bass reaction
        bass = np.mean(spec[:8])
        if bass > 0.5:
            self.particles.emit(cx, cy, self.get_color(0), int(bass * 5), bass * 6)

        if is_beat:
            for _ in range(5):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(50, 200)
                px = cx + math.cos(angle) * dist
                py = cy + math.sin(angle) * dist
                self.particles.emit(px, py, (255, 255, 255), 15, 12)

        self.particles.update_and_draw(surface)

        # Draw center orb
        orb_size = int(20 + bass * 60)
        for r in range(orb_size, 0, -3):
            alpha = int(100 * (1 - r / orb_size))
            color = self.get_color(0)
            pygame.draw.circle(surface, color, (cx, cy), r, 1)


class WaveformRingMode(VisualizerMode):
    """Waveform drawn as a rotating 3D-like ring."""

    def __init__(self, w, h):
        super().__init__(w, h)
        self.rotation = 0
        self.history = []

    def draw(self, surface, spectrum, amplitude, is_beat, sensitivity):
        self.update_palette()
        spec = self.smooth_spectrum(spectrum) * sensitivity
        self.rotation += 0.01

        # Long fade for trail effect
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 15))
        surface.blit(overlay, (0, 0))

        cx, cy = self.w // 2, self.h // 2

        # Store history for trails
        self.history.append(spec.copy())
        if len(self.history) > 20:
            self.history.pop(0)

        # Draw multiple rings (history)
        for h_idx, hist_spec in enumerate(self.history):
            alpha_mult = (h_idx + 1) / len(self.history)
            radius = 80 + (len(self.history) - h_idx) * 12

            points = []
            for i in range(N_BARS):
                angle = self.rotation + (2 * math.pi * i / N_BARS)
                r = radius + hist_spec[i] * 150 * alpha_mult
                x = cx + math.cos(angle) * r
                y = cy + math.sin(angle) * r * 0.6  # Perspective flattening
                points.append((x, y))

            color = self.get_color(h_idx % 4, alpha_mult * 0.7)
            if len(points) > 2:
                pygame.draw.lines(surface, color, True, points, 2)

        # Current ring (brightest)
        points = []
        for i in range(N_BARS):
            angle = self.rotation + (2 * math.pi * i / N_BARS)
            r = 80 + spec[i] * 150
            x = cx + math.cos(angle) * r
            y = cy + math.sin(angle) * r * 0.6
            points.append((x, y))

        if len(points) > 2:
            pygame.draw.polygon(surface, self.get_color(0, 0.2), points)
            pygame.draw.lines(surface, (255, 255, 255), True, points, 3)

        if is_beat:
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), int(60 + amplitude * 100), 3)


class NeuralMeshMode(VisualizerMode):
    """Connected node mesh that dances to the music."""

    def __init__(self, w, h):
        super().__init__(w, h)
        self.nodes = []
        for _ in range(50):
            self.nodes.append({
                'x': random.randint(0, w),
                'y': random.randint(0, h),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'base_x': random.randint(0, w),
                'base_y': random.randint(0, h),
            })

    def draw(self, surface, spectrum, amplitude, is_beat, sensitivity):
        self.update_palette()
        spec = self.smooth_spectrum(spectrum) * sensitivity

        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((5, 5, 10, 50))
        surface.blit(overlay, (0, 0))

        # Update nodes
        for i, node in enumerate(self.nodes):
            # Node moves based on its corresponding frequency band
            band = i % N_BARS
            intensity = spec[band]

            node['vx'] += (node['base_x'] - node['x']) * 0.001
            node['vy'] += (node['base_y'] - node['y']) * 0.001

            # Music reaction
            node['vx'] += random.uniform(-1, 1) * intensity * 2
            node['vy'] += random.uniform(-1, 1) * intensity * 2

            # Damping
            node['vx'] *= 0.95
            node['vy'] *= 0.95

            node['x'] += node['vx']
            node['y'] += node['vy']

            # Keep in bounds
            node['x'] = max(0, min(self.w, node['x']))
            node['y'] = max(0, min(self.h, node['y']))

        # Draw connections
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                dx = self.nodes[i]['x'] - self.nodes[j]['x']
                dy = self.nodes[i]['y'] - self.nodes[j]['y']
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < 150:
                    alpha = int(255 * (1 - dist / 150) * 0.5)
                    band = (i + j) % N_BARS
                    intensity = spec[band]
                    color = self.get_color(band, 0.3 + intensity * 0.7)
                    color = color + (alpha,)

                    # Draw line with alpha
                    line_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
                    pygame.draw.line(line_surf, color,
                                   (int(self.nodes[i]['x']), int(self.nodes[i]['y'])),
                                   (int(self.nodes[j]['x']), int(self.nodes[j]['y'])), 1)
                    surface.blit(line_surf, (0, 0))

        # Draw nodes
        for i, node in enumerate(self.nodes):
            band = i % N_BARS
            intensity = spec[band]
            size = int(3 + intensity * 8)
            color = self.get_color(band, 0.5 + intensity * 0.5)
            pygame.draw.circle(surface, color, (int(node['x']), int(node['y'])), size)

        if is_beat:
            for node in self.nodes[:10]:
                self.particles.emit(node['x'], node['y'], self.get_color(0), 5, 6)

        self.particles.update_and_draw(surface)


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class MusicVisualizer:
    def __init__(self, audio_file):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Generative Music Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.font_large = pygame.font.SysFont("monospace", 40, bold=True)

        self.audio = AudioProcessor(audio_file)

        self.modes = [
            FrequencyBarsMode(WIDTH, HEIGHT),
            CircularSpectrumMode(WIDTH, HEIGHT),
            ParticleBurstMode(WIDTH, HEIGHT),
            WaveformRingMode(WIDTH, HEIGHT),
            NeuralMeshMode(WIDTH, HEIGHT),
        ]
        self.current_mode = 0
        self.sensitivity = DEFAULT_SENSITIVITY
        self.paused = False
        self.fullscreen = False

        self.audio.start()

    def run(self):
        running = True

        while running:
            dt = self.clock.tick(FPS) / 1000.0

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_1:
                        self.current_mode = 0
                    elif event.key == pygame.K_2:
                        self.current_mode = 1
                    elif event.key == pygame.K_3:
                        self.current_mode = 2
                    elif event.key == pygame.K_4:
                        self.current_mode = 3
                    elif event.key == pygame.K_5:
                        self.current_mode = 4
                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        self.sensitivity = min(5.0, self.sensitivity + 0.2)
                    elif event.key == pygame.K_MINUS:
                        self.sensitivity = max(0.2, self.sensitivity - 0.2)

                elif event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.resize_modes(event.w, event.h)

            # Check if audio finished
            if self.audio.is_finished():
                running = False
                continue

            # Get audio data
            if not self.paused:
                spectrum, amplitude, is_beat = self.audio.get_spectrum()
            else:
                spectrum = np.zeros(N_BARS)
                amplitude = 0
                is_beat = False

            # Clear screen with dark background
            self.screen.fill((10, 10, 20))

            # Draw visualization
            mode = self.modes[self.current_mode]
            mode.draw(self.screen, spectrum, amplitude, is_beat, self.sensitivity)

            # Draw UI overlay
            self.draw_ui()

            pygame.display.flip()

        pygame.mixer.music.stop()
        pygame.quit()

    def resize_modes(self, w, h):
        self.modes = [
            FrequencyBarsMode(w, h),
            CircularSpectrumMode(w, h),
            ParticleBurstMode(w, h),
            WaveformRingMode(w, h),
            NeuralMeshMode(w, h),
        ]

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        info = pygame.display.Info()
        self.resize_modes(info.current_w, info.current_h)

    def draw_ui(self):
        # Mode name
        mode_names = ["Frequency Bars", "Circular Spectrum", "Particle Burst", 
                      "Waveform Ring", "Neural Mesh"]
        text = self.font_large.render(mode_names[self.current_mode], True, (255, 255, 255))
        self.screen.blit(text, (20, 20))

        # Controls
        controls = [
            "1-5: Mode | SPACE: Pause | F: Fullscreen | +/-: Sensitivity | ESC: Quit",
            f"Sensitivity: {self.sensitivity:.1f}x | Tempo: {self.audio.tempo:.1f} BPM"
        ]
        for i, line in enumerate(controls):
            text = self.font.render(line, True, (180, 180, 180))
            self.screen.blit(text, (20, self.screen.get_height() - 50 + i * 25))

        # Progress bar
        progress = self.audio.get_current_time() / self.audio.duration if self.audio.duration > 0 else 0
        bar_w = self.screen.get_width() - 40
        pygame.draw.rect(self.screen, (50, 50, 50), (20, self.screen.get_height() - 80, bar_w, 6))
        pygame.draw.rect(self.screen, (0, 200, 255), (20, self.screen.get_height() - 80, int(bar_w * progress), 6))


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = input("Drag and drop your audio file here (or type path): ").strip().strip('"')

    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}")
        print("\nUsage: python music_visualizer.py <audio_file.mp3/wav>")
        sys.exit(1)

    visualizer = MusicVisualizer(audio_file)
    visualizer.run()


if __name__ == "__main__":
    main()

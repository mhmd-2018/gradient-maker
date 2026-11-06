# 🎨 AI Pattern Generator

A desktop application for generating professional backgrounds and seamless patterns. Built with Python, Tkinter, and Pillow, it lets you create abstract art, gradients, textures, and seamless tiles through a simple GUI — no AI service or API key required (the "AI" in the name refers to the procedural/randomized generation engine).

> **Note:** The UI labels and source-code comments are written in Persian (Farsi). The app is fully functional regardless of system language.

---

## ✨ Features

- **4 pattern styles**
  - **Abstract** — random mix of circles, polygons, wavy lines, and geometric grids
  - **Gradient** — linear and radial gradients with optional overlaid shapes
  - **Texture** — paper, fabric, marble, and noise textures
  - **Seamless tile** — repeatable patterns with no visible seams (great for wallpapers, fabrics, websites)
- **Live preview** in the right panel (resized for display, full resolution on save)
- **Configurable output resolution** — 720p / 1080p / 4K presets or custom width × height
- **Complexity slider** (1–10) controls how many shapes/elements are drawn
- **Custom color palette** — pick 2–4 colors via the system color picker, or randomize
- **One-click randomization** — generate a fresh pattern with current settings
- **Batch generation** — produce 10 random patterns in a single run and save them to a folder
- **Save as PNG** at high quality (95)
- **Non-blocking UI** — generation runs in a background thread so the window stays responsive

---

## 📁 Project Structure

```
Ai_pattern/
├── main.py              # Entry point — launches the Tkinter UI
├── ui.py                # Full GUI: settings panel, preview, actions
├── pattern_engine.py    # Core engine: canvas, color gen, noise, blur, save
├── shape_generator.py   # Abstract shapes (circles, polygons, wavy lines, grids)
├── gradient_maker.py    # Linear, radial, and multi-stop gradients
├── texture_maker.py     # Paper, fabric, marble, and noise textures
├── seamless_title.py    # Seamless (tileable) pattern generator
└── requirement.txt      # Python dependencies
```

---

## 🧩 Modules at a Glance

| Module | Purpose | Key API |
| --- | --- | --- |
| `pattern_engine.py` | Canvas management, color generation, noise/blur, save | `PatternEngine`, `PatternStyle` |
| `shape_generator.py` | Random geometric and abstract shapes | `ShapeGenerator.random_style()` |
| `gradient_maker.py` | Numpy-powered gradient rendering | `GradientMaker.linear_gradient()`, `.radial_gradient()`, `.multi_gradient()` |
| `texture_maker.py` | Procedural textures (paper/fabric/marble/noise) | `TextureMaker.*_texture()` |
| `seamless_title.py` | 3×3 canvas trick to produce seamless tiles | `SeamlessTileGenerator.generate_seamless_pattern()` |
| `ui.py` | Tkinter interface wiring everything together | `AIPatternGeneratorUI` |
| `main.py` | Bootstraps the UI | — |

---

## 🚀 Installation

### 1. Requirements
- Python 3.8+
- A desktop environment with a display (Tkinter needs a GUI; will not run headless on a server without X11)

### 2. Install dependencies

```bash
pip install -r requirement.txt
```

`requirement.txt` contents:
```
Pillow>=10.0.0
numpy>=1.24.0
colour-science>=0.4.0
```

> Tkinter ships with standard Python on Windows and macOS. On some Linux distros you may need to install it separately:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## ▶️ Usage

Run from the project root:

```bash
python main.py
```

You'll see a startup banner in the console and the GUI window will open (default size 1200×700).

### Workflow

1. **Pick a style** — Abstract / Gradient / Texture / Seamless (left panel, radio buttons).
2. **Set the resolution** — use the 720p / 1080p / 4K buttons or type a custom width and height.
3. **Adjust complexity** — slider from 1 (minimal) to 10 (dense).
4. **Choose colors** — click any of the 4 color buttons to open the color picker, or hit "تصادفی‌سازی رنگ‌ها" to randomize the palette.
5. **Generate** — click the green "🎲 بساز! (تصادفی)" button. The preview appears on the right.
6. **Save** — click "💾 ذیره PNG" to export at full resolution, or "📦 تولید ۱۰ عدد تصادفی" to batch-generate 10 patterns into a folder you choose.

A status bar at the bottom reports progress and errors.

---

## 🔧 How It Works

### Pattern Engine (`pattern_engine.py`)
The `PatternEngine` class holds the active `PIL.Image` and `ImageDraw`. It exposes helpers to:
- Set resolution and create a blank canvas
- Generate harmonious random colors (HSV-based, then optionally mixed from the user palette)
- Add subtle Gaussian noise for organic feel
- Apply blur for soft transitions
- Save the final image as PNG

### Gradients (`gradient_maker.py`)
Gradients are computed vectorized with NumPy. For a linear gradient, the engine projects each pixel's normalized coordinate onto the gradient direction (`cos θ · x + sin θ · y`), then interpolates the color stops with `np.interp`. Radial gradients use Euclidean distance from a center point.

### Shapes (`shape_generator.py`)
`ShapeGenerator` draws onto a given `ImageDraw` context. `random_style()` randomly picks 2–4 of the available shape routines (circles, polygons, wavy lines, geometric grid) and runs them — that's why every abstract pattern looks different.

### Textures (`texture_maker.py`)
Each texture is a different procedural recipe:
- **Paper** — Gaussian noise added to a base color, with light salt-and-pepper specks
- **Fabric** — checkerboard weave pattern at a configurable thread density, slightly blurred
- **Marble** — `sin(x + sin(y + sin(x)))` turbulence function, blended between two colors
- **Noise** — Gaussian, uniform, or sinusoidal "Perlin-like"

### Seamless Tiles (`seamless_title.py`)
To guarantee a tile repeats seamlessly in all directions, the generator paints shapes onto a **3×3 canvas** and crops the center tile. Any shape that crosses the center tile's edge also appears on the opposite side, so wrapping is invisible. The class also includes a `create_seamless_preview()` helper that tiles the result 3×3 to verify the seamlessness visually.

### UI (`ui.py`)
The `AIPatternGeneratorUI` class assembles a two-panel layout: settings on the left, preview on the right. All generation runs in a daemon thread (`threading.Thread`) so the Tkinter main loop never freezes, and `self.root.after(0, ...)` is used to safely update widgets from the worker thread.

---

## 🧪 Examples

Generate a single 4K abstract pattern and save it:

```bash
python main.py
# In the GUI:
#   Style = Abstract, Resolution = 4K, Complexity = 7
#   Click "🎲 بساز!" then "💾 ذخیره PNG"
```

Programmatically (no GUI):

```python
from pattern_engine import PatternEngine
from shape_generator import ShapeGenerator

engine = PatternEngine(1920, 1080)
engine.create_canvas((20, 20, 40))
shape_gen = ShapeGenerator(engine.draw, engine.width, engine.height)
shape_gen.random_style([(255, 99, 71), (60, 179, 113), (255, 215, 0)], complexity=6)
engine.add_noise(0.02)
engine.save("my_pattern.png")
```

---

## ⚠️ Known Limitations

- **"Copy to clipboard"** currently shows an info dialog and does not actually copy the image to the system clipboard. Use **Save PNG** and then copy the file manually.
- **Batch generation** shares the live preview state with the main window, so the preview may flicker while the 10 patterns are being produced. Files are still saved correctly.
- **Persian text rendering** inside Tkinter buttons depends on system font support for Arabic-script characters; on minimal Linux installs the labels may look unstyled but remain functional.
- The `colour-science` package is listed as a dependency but isn't imported by any module — it can be removed if you want a leaner install.

---

## 📜 License

No license file is included in the project. Treat the code as **all rights reserved** by the original author ("تیم برنامه‌نویسی" / Programming Team) unless stated otherwise. Contact the author before redistributing or using it commercially.

---

## 👤 Credits

- **Author:** Programming Team (تیم برنامه‌نویسی)
- **Version:** 1.0
- **Tech stack:** Python, Tkinter, Pillow (PIL), NumPy

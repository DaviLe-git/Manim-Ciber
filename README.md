# Manim Cybersecurity

A Python-based animation project for creating educational cybersecurity videos using [Manim Community](https://www.manim.community/).

The goal is to develop a reusable visual language and component library for explaining cybersecurity concepts through clear, technical animations inspired by the educational approach of 3Blue1Brown.

## Project Goals

* Create educational cybersecurity animations with Manim.
* Develop a consistent visual identity across videos.
* Build reusable components for common cybersecurity concepts.
* Explain complex technical concepts through visual demonstrations.
* Eventually produce complete 5–10 minute cybersecurity explainer videos.

## Project Structure

```text
manim-ciber/
├── assets/
│
├── components/
│   ├── __init__.py
│   └── default.py
│
├── output/
│
├── scenes/
│   ├── __init__.py
│   ├── network_diagram.py
│   ├── test_default.py
│   └── website_request.py
│
├── .gitignore
└── README.md
```

### `components/`

Reusable visual components and design elements shared between scenes.

The `default.py` module currently contains:

* Color Pallete
* Typography
* Panels & Boxes
* Badges
* Diagram Parts
* Icons
* Terminal Window
* Composition 
* Scene base * Animation Helpers 

This will eventually evolve into a larger visual component library.

### `scenes/`

Individual Manim scenes and animations.

Each scene is designed to explain a specific concept or serve as part of a larger video.

### `assets/`

External assets used by animations, such as images, icons, or other media.

### `output/`

Local output directory for generated files. Rendered media is not tracked by Git.

## Rendering

Manim Community is used to render the animations.

For a fast development render:

```bash
PYTHONPATH="$PWD" manim -pql scenes/test_default.py TestDefault
```

For a higher-quality render:

```bash
PYTHONPATH="$PWD" manim -pqh scenes/test_default.py TestDefault
```

The `PYTHONPATH` configuration allows scenes to import reusable components from the project root.

## Development

The project is currently under active development.

The planned development path is:

```text
Basic Manim
    ↓
Visual Design System
    ↓
Reusable Components
    ↓
Network Animations
    ↓
Cybersecurity Visualizations
    ↓
Narration & Timing
    ↓
Complete Educational Videos
```

## Planned Components

Future versions are expected to include reusable components for:

* Network nodes
* Browsers
* Web servers
* Databases
* Firewalls
* Routers
* Packets
* HTTP requests and responses
* DNS
* TCP connections
* TLS
* Cryptographic keys
* Terminal windows
* Code blocks
* Attack/defense visualizations

## Planned Videos

The first complete video is planned around:

> **What Actually Happens When You Visit a Website?**

Topics will include:

* DNS resolution
* TCP connection establishment
* TLS
* HTTP
* Server-side processing
* HTTP responses
* Browser rendering
* Basic cybersecurity implications

## Requirements

* Python
* pipx
* Manim Community
* FFmpeg
* Git

Check the installed Manim version with:

```bash
manim --version
```

## Setup

If you don't have manim installed you can follow the [official Installation guide](https://docs.manim.community/en/stable/installation.html#local-installation).

Or you can follow these steps, to install and configure to run it easily:

Install manim and put in your path:
```bash
pipx install manim
pipx ensurepath
# close and reopen your terminal
```

From the project root, make components/ importable by manim
(installs this repo into manim's venv, in editable mode):
```bash
pipx inject manim --editable "$(pwd)"
```

Verify — this should render and open a test scene:
```bash
manim -pql scenes/test_default1.py TestIcons
```

## License

License information will be added as the project develops.


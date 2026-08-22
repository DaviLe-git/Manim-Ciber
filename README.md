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

## Current Visual System

The project currently defines standard typography sizes:

```text
Title:        52
Heading:      40
Large text:   32
Medium text:  26
Small text:   20
Code:         22
```

Standard box sizes are also defined:

```text
Small:   2.0 × 0.8
Medium:  3.0 × 1.4
Large:   4.0 × 2.0
```

These values are centralized in `components/default.py` so that the visual appearance can be changed consistently across scenes.

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
* Manim Community
* FFmpeg
* Git

Check the installed Manim version with:

```bash
manim --version
```

## License

License information will be added as the project develops.


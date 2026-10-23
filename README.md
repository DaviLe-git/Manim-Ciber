# Manim Ciber

A Manim-based project for creating educational cybersecurity animations, with reusable components and consistent visual styling inspired by 3Blue1Brown.

![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-6FA8A0?style=flat-square)
![Manim Community](https://img.shields.io/badge/manim-community-8FC4BC?style=flat-square)
![License TBD](https://img.shields.io/badge/license-TBD-9AA5B1?style=flat-square)

```sh
pipx install manim && pipx inject manim --editable "$(pwd)"
manim -pql scenes/test_default1.py TestIcons
```

The goal is to develop a reusable visual language and component library for explaining cybersecurity concepts through clear, technical animations — the same way 3Blue1Brown makes mathematics visible.

## Highlights

- **One design system.** Every scene draws from a single dark-editorial theme — deep slate background, muted teal accent, off-white text, semantic status colors — so a whole video series looks like it came from one hand.
- **A component library, not just scenes.** `components/default.py` ships ready-made building blocks: terminals, network diagrams, packets, badges, icons, oscilloscopes. Scenes compose them; they never redraw them.
- **Cybersecurity-native primitives.** Labeled connectors and traveling packets for data flows, `FailMark` for broken nodes and cut cables, a `Terminal` with typewriter animation for CLI demos, semantic badges (`safe` / `warning` / `danger`) for threat levels.
- **Signal-kit for the physical layer.** NRZ bit waves, PAM level waves, sine carriers and oscilloscope scopes — for explaining how bits actually become voltage, light, and radio.
- **Consistent typography hierarchy.** `Title` → `Heading` → `LargeText` → `MediumText` → `SmallText` → `CodeText`, plus `SectionHeader` openers and `Caption` narrators for every frame.
- **Just Manim Community.** No daemon, no database, no cloud. Python in, `.mp4` out.

## Screens

<details>
<summary><strong>Screens & render commands</strong> — click to expand</summary>

| Module | Scene | What it shows |
| --- | --- | --- |
| **Physical Layer** | `InformationAndSignal` | Bits → NRZ voltage → analog sine stacks → carrier modulation → multi-level symbols |
| **Networking** | `TCPIP` | IP vs. TCP as a story: handshake, sequencing, ACKs, retransmission of a lost packet |
| **Networking** | `TCPHandshakeV2` | The three-way handshake as a sequence diagram with lifelines |
| **Networking** | `NetworkTopologies` | Bus / ring / star / mesh — four shapes, one question: what happens when something breaks? |
| **Design System** | `TestIcons`, `TestTerminal`, `TestBadges`, … | Live test-suite rendering every component family |

```sh
# One scene, fast preview
manim -pql scenes/network/tcp_handshake.py TCPHandshakeV2

# All test-suite scenes at once
manim -pql -a scenes/test_default1.py
```

</details>

## Components

Everything below lives in `components/default.py` and is one import away:

```python
from manim import *
from components.default import *
```

### Theme & typography

| Helper | Purpose |
| --- | --- |
| `BACKGROUND_COLOR`, `ACCENT`, `TEXT_PRIMARY`, … | Named palette constants — never hardcode a hex |
| `SEMANTIC_COLORS` | Lookup for status colors (`info` / `safe` / `warning` / `danger` / `neutral`) |
| `Title` `Heading` `LargeText` `MediumText` `SmallText` `CodeText` | Six-level text hierarchy with theme fonts baked in |

### Panels, boxes & badges

| Helper | Purpose |
| --- | --- |
| `Panel(w, h, stroke_color)` | Rounded panel — `Panel(4, 2, COLOR_DANGER)` auto-tints red |
| `SmallBox` `MediumBox` `LargeBox` | Pre-sized containers |
| `LabeledBox(text, box_size=…)` | Box with a centered, auto-fitted label |
| `Badge(text, kind=…)` | Status pill: `Badge("ENCRYPTED", kind="safe")` |

### Devices & security icons

| Helper | Purpose |
| --- | --- |
| `LaptopIcon` `PhoneIcon` `ServerIcon` | Endpoint devices |
| `LockIcon` `ShieldIcon(checked=…)` `FirewallIcon` | Security concepts |

### Diagrams & data flow

| Helper | Purpose |
| --- | --- |
| `Connector(a, b, label=…)` | Labeled arrow; `dashed=True` for blocked/indirect flows |
| `Packet(text)` | Pill that travels along a path (`SYN`, `ACK`, `GET /` …) |
| `NetNode(label)` | Circular node for network diagrams |
| `Link(a, b, trim=…)` | Undirected connection that stops at node edges |
| `GraphDiagram(pos, edges)` | Whole node-link graph from a spec; animate `net.nodes["A"]`, `net.links[("A","B")]` by name |
| `circular_layout(names, radius)` | Evenly place nodes around a circle |
| `edge_toward(mobj, target)` | Bounding-box edge point — arrows stop at the icon, not its center |
| `FailMark(target)` | Red ✕ — "this node/link is down" |

### Terminal & code

| Helper | Purpose |
| --- | --- |
| `Terminal(lines, title=…)` | Dark terminal window with traffic-light dots; `add_line()` grows it live |
| `TypeIn(text)` | Typewriter reveal for terminal lines and code |

### Composition & narration

| Helper | Purpose |
| --- | --- |
| `CyberScene` | `Scene` subclass — the theme applies itself |
| `SectionHeader(title, kicker=…)` | Editorial section opener: kicker, title, accent rule |
| `InfoCard(title, body)` | Definition panel for key concepts |
| `BulletList(*items, marker=…)` | Styled lists — `dot`, `square`, or `number` |
| `Divider()` `Caption(text)` | Hairline rule; bottom-anchored narration line |

### Signal kit (physical layer)

| Helper | Purpose |
| --- | --- |
| `Scope(title=…)` | Oscilloscope panel with grid and center line |
| `BitWave(bits)` | NRZ encoding — `1 → +V`, `0 → −V` |
| `LevelWave(levels)` | Piecewise-constant wave (multilevel / PAM signals) |
| `SineWave(cycles=…)` `WaveCurve(fn)` | Analog waves and arbitrary functions |
| `BitRow(bits)` | Bit digits aligned above their wave segments |

## Install

Requires Python, [pipx](https://pipx.pypa.io/), FFmpeg and Git.

```sh
# Manim (Community edition) on your PATH
pipx install manim
pipx ensurepath
# close and reopen your terminal
```

From the project root, make `components/` importable by Manim (installs this repo into Manim's venv, in editable mode):

```sh
pipx inject manim --editable "$(pwd)"
```

Verify — this should render and open a test scene:

```sh
manim -pql scenes/test_default1.py TestIcons
```

If you prefer not to use pipx, follow the [official Manim installation guide](https://docs.manim.community/en/stable/installation.html) and run scenes with `PYTHONPATH="$PWD"` from the project root.

## Usage

```sh
# Fast preview (low quality, quick iteration)
manim -pql scenes/network/topologies.py NetworkTopologies

# High-quality render
manim -pqh scenes/network/tcp_ip.py TCPIP

# Render every scene in a file
manim -pql -a scenes/test_default1.py
```

The `pipx inject` step above is what lets `from components.default import *` work from any scene, with no `PYTHONPATH` juggling.

### Writing a scene

```python
from manim import *
from components.default import *


class MyScene(CyberScene):
    def construct(self):
        header = SectionHeader(
            "Defense in Depth", kicker="Module 04 · Security",
        ).to_corner(UL, buff=0.7)
        self.play(FadeIn(header, shift=0.3 * DOWN))

        term = Terminal([("$ nmap -sV 10.0.0.5", ACCENT_BRIGHT)], height=3.4)
        self.play(FadeIn(term[:4], shift=0.3 * UP))
        self.play(TypeIn(term.lines[0]))
```

## Project structure

```
manim-ciber/
├── assets/                 # images, icons, and other media
├── components/
│   ├── __init__.py
│   └── default.py          # the full visual design system
├── scenes/
│   ├── test_default1.py    # component test-suite (8 scenes)
│   └── network/            # educational modules
│       ├── information_signal.py
│       ├── tcp_ip.py
│       ├── tcp_handshake.py
│       └── topologies.py
├── output/                 # rendered media (not tracked by Git)
├── .gitignore
├── pyproject.toml
└── README.md
```

## Development

The project is under active development. The planned path:

```
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

### Planned components

Future versions are expected to add reusable pieces for browsers, web servers, databases, firewalls, routers, DNS, TLS, cryptographic keys, code blocks, and attack/defense visualizations.

### First video

The first complete 5–10 minute explainer is planned around:

> **What Actually Happens When You Visit a Website?**

Covering DNS resolution, TCP, TLS, HTTP, server-side processing, responses, browser rendering — and the basic cybersecurity implications of each step.

## Contributing

Issues and pull requests are welcome. For larger changes — new component families, theme changes, new modules — please open an issue first to discuss the approach.

When adding a component, also add a test scene to `scenes/test_default1.py` so it renders in the visual test-suite.

## Acknowledgments

- [3Blue1Brown](https://www.3blue1brown.com/) — the visual storytelling approach this project tries to follow.
- [Manim Community](https://www.manim.community/) — the animation engine.

## License

License information will be added as the project develops.

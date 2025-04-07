# NEO Close Approach Visualizer 🚀🌍

A Python application to **fetch, filter, and visualize Near-Earth Object (NEO)** close approach data from NASA JPL's public CAD API. Features an interactive GUI that lets users explore asteroid flybys by date, proximity, and measurement units.

---

## 📚 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Features

- 📡 **Live Data** — Pulls real-time NEO close approach data from NASA JPL's API
- 🖥️ **User Interface** — Simple Tkinter GUI with fields for date ranges, distance limits, and unit conversions
- 📊 **Visualization** — Scatter plot showing object approach dates vs. distance
- 🧮 **Flexible Units** — Supports km, miles, AU, lunar distances, and Earth radii
- 🎯 **Custom Filters** — Annotate the closest N NEOs, sort by proximity
- ⚠️ **Threshold Markers** — Highlights Earth radius, geosynchronous orbit, lunar orbit

---

## 💾 Requirements

- Python 3.7+
- Install required libraries:

```bash
pip install -r requirements.txt
```

> See [`requirements.txt`](requirements.txt) for full dependency list.

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/steveareno225/neo-close-approach.git
cd neo-close-approach
```

2. Fetch NEO data from NASA:

```bash
python fetch_nasa_cad_data.py
```

3. Launch the visualizer:

```bash
python neo_close_approach_plot.py
```

---

## 🧪 Examples

### GUI Interface
Set filters like date range, distance limit, units, and how many NEOs to annotate:

![GUI Input](https://raw.githubusercontent.com/steveareno225/neo-close-approach/main/Screenshot-neo-close-approach-input.jpg)

---

### Output Plot
Visualize closest NEOs with annotations and key orbital distance lines:

![Scatter Plot](https://raw.githubusercontent.com/steveareno225/neo-close-approach/main/Screenshot-neo-close-approach-output.jpg)

---

## 🤝 Contributing

Pull requests are welcome!  
If you have ideas for new features (e.g. orbit visualization, 3D rendering), feel free to open an issue or fork the project.

---

## 📄 License

MIT © 2025 Steven M Tilley  
See [`LICENSE`](LICENSE) for full terms.

---

> Developed by **Steven M Tilley** ([@steveareno225](https://github.com/steveareno225)),  
> this open-source project leverages AI-enhanced coding *(via ChatGPT / Cody)*  
> and is intended as a **starting point** for asteroid visualization and space data analytics.

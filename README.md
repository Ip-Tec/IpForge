# IpForge

**IpForge** is a modern, lightweight GUI tool built with **CustomTkinter** that allows users to easily convert Python scripts into Windows executable files (`.exe`) using PyInstaller.

Designed for simplicity and power, IpForge provides an intuitive interface, build options, and real-time build logs—making Python packaging accessible to everyone.

---

## Features

* 🖥️ **Modern CustomTkinter GUI**
* 📂 **Select Python script** to convert
* ⚙️ **Build options**:

  * `--onefile`
  * `--noconsole`
  * Custom icon support (`.ico`)
  * Output directory selection
* 📜 **Real-time build logs**
* 🔍 Auto-detect PyInstaller installation
* 🧱 Clean, user-friendly interface
* 🔧 Extendable architecture for future plugins

---

## 📦 Installation

### Prerequisites

* Python 3.9+
* Pip

### Clone the Repository

```bash
git clone https://github.com/yourusername/IpForge.git
cd IpForge
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running IpForge

```bash
python ipforge.py
```

---

## Project Structure

```
IpForge/
│
├── ipforge.py              # Main application
├── forge_core/             # Backend build logic
├── ui/                     # GUI components
├── assets/                 # Icons & resources
├── requirements.txt
└── README.md
```

---

## Build EXE using PyInstaller (for distributing IpForge)

```bash
pyinstaller --onefile --noconsole ipforge.py
```

The executable will appear in the `dist/` folder.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

MIT License © 2025 IpForge

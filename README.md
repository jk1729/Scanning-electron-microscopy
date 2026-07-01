# 🔬 Virtual Scanning Electron Microscope (SEM) Simulator with de Broglie Wave Visualization

## 📖 Overview

The **Virtual Scanning Electron Microscope (SEM) Simulator** is an educational Python application that simulates the fundamental operation of a **Scanning Electron Microscope (SEM)** while helping users understand the underlying physics of electron microscopy through **de Broglie wave visualization**.

The project combines three major modules:

* **Virtual SEM Simulator** – Simulates the workflow and controls of an SEM.
* **SEM Sample Image Generation & Processing** – Displays and manipulates SEM sample images using imaging parameters.
* **de Broglie Wave Visualization** – Animates electron wave behavior to illustrate the wave nature of electrons.

This project is intended for educational purposes, allowing students to explore SEM principles without requiring access to expensive laboratory equipment.

---

# 🎯 Objectives

* Simulate the working principle of a Scanning Electron Microscope.
* Demonstrate the effect of different SEM imaging parameters.
* Visualize the wave nature of electrons using de Broglie's hypothesis.
* Provide an interactive learning environment for microscopy and wave physics.
* Help students understand image formation in SEM.

---

# ✨ Features

## 🔬 Virtual SEM Simulator

The SEM simulator recreates the basic workflow of operating a scanning electron microscope.

### System Controls

* Chamber Evacuation
* High Voltage (HV) ON/OFF
* Accelerating Voltage Selection
* Spot Size Control
* Z-Height Adjustment

### Imaging Controls

* Brightness Adjustment
* Contrast Adjustment
* Focus Control
* Magnification (1×–10×)

---

## 🧪 Sample Image Module

Users can explore different SEM samples categorized into various groups.

### Available Categories

### Arthropods

* Ant Eye
* Spider Silk

### Everyday Materials

* Sugar Crystals
* Table Salt
* Kitchen Sponge

### Forensic Materials

* Human Hair
* Polyester Fiber
* Paper Fiber

### Hydrophobic Surfaces

* Butterfly Wing
* Gecko Skin
* Lotus Leaf

### Image Processing Features

The simulator dynamically modifies the selected image using:

* Brightness Enhancement
* Contrast Enhancement
* Gaussian Blur
* Focus Simulation
* Spot Size Blur
* Voltage-Based Contrast
* Magnification Simulation
* Z-Height Defocus

Users can also:

* Import Custom Images
* Save Processed Images
* Reset the Simulator

---

## 🌊 de Broglie Wave Visualization

The project includes an animated visualization demonstrating the **wave nature of electrons** based on **de Broglie's hypothesis**.

The animation illustrates:

* Circular Wave Propagation
* Multiple Wave Modes
* Harmonic Oscillation
* Radial Displacement
* Time-Varying Electron Waves

This visualization helps explain why electrons exhibit both particle-like and wave-like behavior inside an electron microscope.

---

# 🧠 Scientific Concepts Covered

## Scanning Electron Microscopy

* Electron Beam Generation
* Vacuum Chamber
* High Voltage Operation
* Accelerating Voltage
* Spot Size
* Magnification
* Image Formation
* Electron-Specimen Interaction

---

## Wave Physics

* de Broglie Hypothesis
* Matter Waves
* Harmonic Motion
* Circular Wave Propagation
* Sinusoidal Oscillation

---

## Digital Image Processing

* Brightness Adjustment
* Contrast Enhancement
* Gaussian Filtering
* Image Scaling
* Image Sharpening

---

# 🛠 Technologies Used

* Python 3.x
* Tkinter
* Pillow (PIL)
* NumPy
* Matplotlib
* Matplotlib Animation
* pathlib
* os

---

# 📂 Project Structure

```text
Virtual-SEM-Simulator/
│
├── main.py                      # SEM Simulator
├── debroglie_wave.py            # de Broglie Wave Visualization
├── samples/
│   ├── ant-eye.jpg
│   ├── spider-silk.jpg
│   ├── sugar-crystals.jpg
│   ├── table-salt.jpg
│   ├── kitchen-sponge.jpg
│   ├── human-hair.jpg
│   ├── polyester-fiber.jpg
│   ├── paper-fiber.jpg
│   ├── butterfly-wing.jpg
│   ├── gecko-skin.jpg
│   └── lotus-leaf.jpg
│
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Virtual-SEM-Simulator.git
```

Navigate to the project directory

```bash
cd Virtual-SEM-Simulator
```

Install the required libraries

```bash
pip install pillow numpy matplotlib
```

---

# ▶ Running the Project

Run the SEM Simulator

```bash
python main.py
```

Run the de Broglie Wave Visualization

```bash
python debroglie_wave.py
```

---

# 🖥 How to Use

1. Launch the SEM Simulator.
2. Select a specimen from the available sample database.
3. Evacuate the chamber.
4. Turn the High Voltage (HV) ON.
5. Adjust imaging parameters such as:

   * Voltage
   * Spot Size
   * Brightness
   * Contrast
   * Focus
   * Magnification
6. Observe how the SEM image changes in real time.
7. Save the processed image or import a custom specimen image.
8. Run the de Broglie Wave Visualization module to understand the wave behavior of electrons.

---

# 📚 Applications

* Electron Microscopy Education
* Physics Laboratory Demonstrations
* Engineering Education
* Scientific Visualization
* Computational Physics
* Image Processing Learning
* Classroom Simulations

---

# 🚀 Future Enhancements

* Real Electron Beam Scanning Animation
* Beam Raster Visualization
* Secondary Electron Detector Simulation
* Backscattered Electron Imaging
* Noise Simulation
* Scale Bar Generation
* Measurement Tools
* Live Histogram
* 3D Specimen Visualization
* Animation Export (GIF/MP4)
* AI-Based Image Analysis
* More SEM Sample Database

---

# 🎓 Educational Value

This project enables students to:

* Understand the working principle of a Scanning Electron Microscope.
* Learn how imaging parameters influence SEM images.
* Visualize the wave nature of electrons using de Broglie's theory.
* Explore scientific image processing techniques.
* Gain hands-on experience with computational simulations in Python.

---



---

# 📄 License

This project is developed for educational and academic purposes. It is intended for learning, demonstrations, and research. Users are free to modify and extend the project with proper attribution.

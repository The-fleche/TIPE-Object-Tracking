# 📷 Object Tracking & Slider Control (TIPE Project) -> 2024/2025

This repository contains my **TIPE** (*Travaux d'Initiative Personnelle Encadrés*), a research project developed during my CPGE (preparatory classes). The project focuses on real-time object tracking using a mobile camera mounted on a translation axis (slider).

<video src="docs/vidéo_résultat.mp4" controls="controls" style="max-width: 100%;">
</video>

## 🚀 Project Overview

The goal was to answer the following problem: **How to track a complex moving object in an uncontrolled environment using a mobile camera controlled on a translation axis?**

The project combines computer vision for detection and control theory (asservissement) for the physical movement of the camera.

## 🛠 Features

### 1. Computer Vision & Detection
- **Classic Methods:** Implementation of image processing filters (Sobel, Grayscale, Thresholding) to detect edges and shapes.
- **OpenCV Integration:** Transitioned to OpenCV for optimized performance in video stream acquisition and real-time processing.

### 2. Control System & Hardware
- **Servo Control (Asservissement):** Development of a control loop to sync the slider's position with the object's coordinates.
- **Energy & Information Chain:** Designed the hardware interface between the processing unit (Python) and the motor control.
- **Stability:** Implementation of a stabilization system (passive vs. active) to reduce camera shake during movement.

### 3. Physics & Modeling
- **Euler Integration:** Used numerical methods to simulate the motion and predict the object's trajectory.
- **Friction Modeling:** Calculated and modeled dry friction to improve the accuracy of the slider's response.

## 🧰 Tech Stack

- **Language:** Python
- **Libraries:** OpenCV, Matplotlib, NumPy, CSV (for data logging)
- **Physics:** Euler integration, Differential equations, Monte Carlo method

## 📂 Repository Structure

- `/src`: Python scripts for detection and motor control.
- `/docs`: Detailed TIPE report (PDF) and logbooks.
- `/data`: CSV files from experimental trials (position vs. time).
- `/simulations`: Matplotlib scripts for friction and oscillation modeling.

## 📊 Key Results

The system successfully tracks objects by calculating the center of gravity of the detected shape and sending velocity commands to the slider. The project highlights the trade-off between detection speed and movement stability.

# PRESENCE: People Recognition and Energy-Saving Control Engine

A smart appliance controller simulation using real-time presence detection to automatically manage appliances like lights and air conditioning units. This project is implemented using Python, Tkinter, and OpenCV.

## 📌 Project Description

**PRESENCE** is a simulation project designed for environmental awareness and energy efficiency. It detects the presence of people using a webcam and automatically toggles appliances on or off. If no presence is detected for a specific period, a warning is issued before the appliances are turned off. An admin panel allows for password-protected settings management, and the app logs daily appliance usage time with visual summaries.

## 🚀 Features

- Real-time camera feed with face and motion detection using OpenCV
- Automatic appliance control:
  - ON when presence is detected
  - OFF after 15 seconds of no detection
- Warning message before turning off appliances
- Daily logging of appliance ON duration (CSV format)
- Graphical summary of weekly appliance usage
- Admin panel with password management
- GUI designed using Tkinter
- Image-based appliance simulation

## 🛠 Tools & Technologies

- **Python 3.x**
- **Tkinter** – GUI framework
- **OpenCV** – Computer vision for face and motion detection
- **Pillow** – Image handling for appliance icons
- **Matplotlib** – Usage graph plotting
- **CSV** – Activity log format

## 🖼 GUI Layout

The interface includes:

- Live camera feed display
- Appliance icons that change based on ON/OFF state
- Control buttons for admin login, settings, graph, and exit
- Warning label when no presence is detected

## 🧠 Logic & Automation

1. Start camera feed on launch
2. Detect faces and/or motion in frames
3. Turn appliances ON if presence is detected
4. If no detection for 15 seconds:
   - Display warning
   - Turn appliances OFF if still undetected
5. Log ON durations for each appliance daily

## 🔐 Admin Panel

- Password-protected access
- Change current password
- Reset password to default
- Toggle camera and automation ON/OFF

## 📊 Activity Logs & Reports

- All ON durations are saved in `appliance_logs.csv`
- 7-day summary graphs are generated using matplotlib for visual review of appliance use




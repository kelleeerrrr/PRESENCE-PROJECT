<h1 align="center">
PRESENCE: People Recognition and Energy-Saving Control Engine
</h1>

<p align="center">
A smart appliance controller simulation that uses <b>real-time presence detection</b> to automatically manage appliances such as lights and air conditioning units.
</p>

<p align="center">
Built using <b>Python</b>, <b>Tkinter</b>, and <b>OpenCV</b> to demonstrate energy-efficient automation.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.x-blue?logo=python">
<img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv">
<img src="https://img.shields.io/badge/Tkinter-GUI-orange">
<img src="https://img.shields.io/badge/Status-Completed-brightgreen">
</p>

---

# 📌 Project Overview

**PRESENCE** is a simulation-based smart appliance controller designed to promote **energy efficiency and environmental awareness**.

The system uses a **webcam to detect human presence** through computer vision techniques. When a person is detected, appliances automatically turn **ON**. If no presence is detected for a certain period, the system issues a **warning notification** and eventually turns appliances **OFF** to conserve energy.

The application also includes an **admin panel**, **activity logging**, and **weekly usage visualization** to help monitor appliance usage patterns.

This project was developed as part of an **Environmental Science course project**.

---

# 🚀 Key Features

| Feature | Description |
|------|------|
| 📷 Real-time Presence Detection | Uses OpenCV to detect faces and motion through a webcam |
| 💡 Automatic Appliance Control | Appliances turn ON when a person is detected |
| ⏱ Idle Timeout | Appliances turn OFF after 15 seconds of no detection |
| ⚠ Warning System | Displays notification before turning appliances OFF |
| 📊 Usage Analytics | Generates weekly usage graphs using Matplotlib |
| 📁 Activity Logging | Records appliance ON duration in CSV format |
| 🔐 Admin Panel | Password-protected settings management |
| 🖥 GUI Interface | Built with Tkinter for a user-friendly interface |

---

# 🛠 Technologies Used

| Technology | Purpose |
|------|------|
| **Python 3.x** | Core programming language |
| **Tkinter** | Graphical User Interface |
| **OpenCV** | Face and motion detection |
| **Pillow** | Image handling for appliance icons |
| **Matplotlib** | Data visualization for appliance usage |
| **CSV** | Logging appliance activity data |

---

# 🖼 Application Interface

The graphical interface includes:

- 📷 **Live Camera Feed**
- 💡 **Appliance Icons** that change depending on ON/OFF status
- ⚙ **Admin Controls** for settings and system management
- ⚠ **Warning Indicator** when no presence is detected
- 📊 **Graph Button** to view appliance usage analytics

---

# 🧠 System Logic

The automation follows this workflow:

1. Start webcam feed on application launch
2. Detect faces and motion in camera frames
3. If presence is detected:

   * Turn appliances **ON**
4. If no presence is detected for **15 seconds**:

   * Display warning notification
5. If absence continues:

   * Turn appliances **OFF**
6. Record appliance ON duration into the activity log

---

# 🔐 Admin Panel

The admin panel allows users to manage system settings:

* Password-protected access
* Change current admin password
* Reset password to default
* Enable/disable camera detection
* Enable/disable appliance automation

---

# 📊 Activity Logs & Reports

Appliance usage is automatically tracked.

**Data stored in:**

```
appliance_logs.csv
```

Logs include:

* Date
* Appliance name
* Total ON duration

The system generates a **7-day usage graph** using **Matplotlib** to help visualize energy consumption patterns.

---

# ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/PRESENCE.git
cd PRESENCE
```

### 2️⃣ Install Dependencies

```bash
pip install opencv-python pillow matplotlib
```

### 3️⃣ Run the Program

```bash
python main.py
```

Make sure your **webcam is connected and accessible**.

---

# 📁 Project Structure

```
PRESENCE
│
├── main.py
├── appliance_logs.csv
├── icons/
│   ├── light_on.png
│   ├── light_off.png
│   ├── ac_on.png
│   └── ac_off.png
│
├── admin/
│   └── admin_panel.py
│
└── graphs/
    └── weekly_usage.py
```

---

# 🌱 Significance of the Project

This project demonstrates how **computer vision and automation** can contribute to **energy conservation**. By automatically controlling appliances based on human presence, unnecessary power consumption can be reduced.

Although the project is a **simulation**, it presents a concept that could be expanded into real-world **smart home or smart building systems**.

---

# ⭐ Future Improvements

Possible enhancements include:

* Integration with **IoT hardware (Arduino / Raspberry Pi)**
* Support for **multiple rooms or cameras**
* Cloud-based usage analytics
* Mobile application control
* Machine learning-based presence recognition

---

# 🎓 Academic Project

Developed as part of an **Environmental Sciences project** focusing on **technology-driven sustainability and smart energy solutions**.



# 🎨 Picture Editor

A browser-based image editor built with Streamlit and Pillow, with a **live before/after preview**.

## Features
- **Crop** by margin percentages
- **Resize** with optional aspect-ratio lock (high-quality Lanczos resampling)
- **Rotate** any angle (canvas expands to fit), **flip** horizontally / vertically
- **Adjust** brightness, contrast, saturation and sharpness
- **12 filters**: grayscale, sepia, invert, blur, Gaussian blur (adjustable radius), sharpen,
  detail, edge enhance, find edges, emboss, contour, smooth
- **Transparency preserved**: PNG/WebP alpha channels survive every edit
- Correct phone-photo orientation (EXIF)
- **Export** as PNG, JPEG or WebP with a quality setting (JPEG transparency flattened onto white)
- One-click **reset** of all edits

## Processing order
```
EXIF orientation -> crop -> resize -> rotate -> flip -> tone adjustments -> filter
```

## Run locally
```bash
cd Picture-Editor-App
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface (sidebar controls, preview, export) |
| `editor.py` | Pillow processing pipeline driven by an `EditSettings` dataclass |
| `tests/` | Unit tests for every filter on RGB and RGBA images + headless UI test |

## Tests
```bash
pip install pytest
python -m pytest
```

---
## 👤 About the Author

**Faizan Saleem Siddiqui**, Embedded Firmware Engineer | Research Scholar

Electronics engineer with 2+ years of experience in embedded systems and firmware development.
I build production firmware for **BLE wearables and biosignal devices** on Nordic nRF52 (Zephyr / nRF
Connect SDK), including **secure OTA updates (MCUboot, signed images)**, **low-power battery
management** and **true-wireless Bluetooth audio**. My background also covers STM32 and ESP32 with
FreeRTOS, real-time data acquisition, digital signal processing, industrial IoT, and Python tooling
for data, automation and machine learning.

- 🎓 MS Electronics, Quaid-i-Azam University, Islamabad (BS Electronics: 1st position, merit scholar)
- 🧑‍🏫 Former Visiting Faculty, Embedded Systems, and Research Assistant, Autonomous Vehicles (COMSIP Lab)
- 🌍 Open to embedded / firmware engineering opportunities worldwide

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Faizan%20Saleem%20Siddiqui-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/faizan-saleem-siddiqui-4411bb247/)
[![GitHub](https://img.shields.io/badge/GitHub-FaizanSSDQ-181717?logo=github&logoColor=white)](https://github.com/FaizanSSDQ)
[![Email](https://img.shields.io/badge/Email-faizansaleemsdq%40gmail.com-D14836?logo=gmail&logoColor=white)](mailto:faizansaleemsdq@gmail.com)

Licensed under the [MIT License](../LICENSE).

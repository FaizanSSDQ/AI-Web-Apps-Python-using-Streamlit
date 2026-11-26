# 🔗 URL Shortener

A Streamlit app that shortens long links with free public services and generates a QR code for each.

## Features
- **3 key-free services**: TinyURL, da.gd, clck.ru (switch if one is unavailable)
- **URL validation and normalisation**: adds `https://` when missing; rejects spaces,
  non-web schemes and malformed hosts before any network call
- **One-click copy** (works on servers, unlike clipboard libraries), "open link" button and
  "characters saved" metric
- **QR code** for every short link, downloadable as PNG
- **Session history** of the last 10 links with CSV export

## Run locally
```bash
cd URL-Shortener-App
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `shortener.py` | Validation, provider abstraction (`pyshorteners`) and QR generation |
| `tests/` | Unit tests with an injected fake client (no network) + headless UI tests |

## Tests
```bash
pip install pytest
python -m pytest
```

---
## 👤 About the Author

**Faizan Saleem Siddiqui**, Embedded Firmware Engineer | Visiting Faculty | Research Scholar

Electronics engineer with 2+ years of experience in embedded systems and firmware development.
I build firmware for **BLE wearables** and **Bluetooth TWS audio devices** on Nordic nRF52 (Zephyr /
nRF Connect SDK), including **secure OTA updates (MCUboot, signed images)**, **low-power battery
management** and **charging-case firmware**. My background also covers STM32 and ESP32 with
FreeRTOS, real-time data acquisition, digital signal processing, industrial IoT, and Python tooling
for data, automation and machine learning.

- 🎓 MS Electronics, Quaid-i-Azam University, Islamabad (BS Electronics: 1st position, merit scholar)
- 🧑‍🏫 Visiting Faculty Member, Quaid-i-Azam University: teaching Real-Time Systems (STM32, FreeRTOS),
  Microcontroller Interfacing (ESP32) and AI/ML on Embedded Devices (TinyML)
- 🔬 Former Research Assistant, Autonomous Vehicle Engineering (COMSIP Lab, QAU)
- 🌍 Open to embedded / firmware engineering opportunities worldwide

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Faizan%20Saleem%20Siddiqui-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/faizan-saleem-siddiqui-4411bb247/)
[![GitHub](https://img.shields.io/badge/GitHub-FaizanSSDQ-181717?logo=github&logoColor=white)](https://github.com/FaizanSSDQ)
[![Email](https://img.shields.io/badge/Email-faizansaleemsdq%40yahoo.com-6001D2?logo=yahoo&logoColor=white)](mailto:faizansaleemsdq@yahoo.com)

Licensed under the [MIT License](../LICENSE).

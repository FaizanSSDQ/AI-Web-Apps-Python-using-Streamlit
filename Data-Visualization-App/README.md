# 📊 Data Visualization App

Upload a dataset and explore it with interactive Plotly charts, without writing any code.

## Features
- Upload **CSV** (auto-detects `,` `;` tab separators), **Excel** or **JSON**; several files at once
- Built-in **sample dataset** (IoT sensor nodes: temperature, humidity, battery voltage, packet loss),
  so the app is useful immediately
- **7 chart types**: line, bar (with sum/mean/median/count/min/max aggregation), scatter, histogram,
  box plot, pie/donut, correlation heatmap
- Optional **colour grouping** by any categorical column
- **Column profile**: detected type, missing %, unique values, mean/min/max
- **Row filtering** with pandas query syntax, e.g. `temperature_c > 24 and node == 'Node-B'`
- Export charts as **interactive HTML** and filtered data as **CSV**
- Automatic date detection for columns named `date` / `time`

## Run locally
```bash
cd Data-Visualization-App
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `viz.py` | Loading, type detection, profiling and chart building (UI-independent) |
| `tests/` | Unit tests + headless UI test that renders every chart type |

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

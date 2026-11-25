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

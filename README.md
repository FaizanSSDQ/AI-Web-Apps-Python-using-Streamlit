# Streamlit Web Apps in Python

[![CI](https://github.com/FaizanSSDQ/AI-Web-Apps-Python-using-Streamlit/actions/workflows/ci.yml/badge.svg)](https://github.com/FaizanSSDQ/AI-Web-Apps-Python-using-Streamlit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-FF4B4B)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Seven self-contained web apps for speech, web data, data visualisation, text analytics and image
processing. Each app is a complete project with its own README, dependencies and automated tests,
and keeps its logic separate from its user interface.

## Apps

| App | What it does | Key techniques |
|---|---|---|
| 🎙️ [Audio to Text Converter](Audio-to-Text-Converter-App) | Transcribes recordings in 7 languages, with optional timestamps | Silence-based segmentation, in-memory audio pipeline, speech recognition |
| 🕸️ [Web Data Scraper](Data-Scraper-App) | Extracts text, links, images and tables from a web page; CSV/ZIP export | BeautifulSoup + lxml, `pandas.read_html`, URL normalisation |
| 📊 [Data Visualization App](Data-Visualization-App) | Uploads CSV/Excel/JSON and builds 7 interactive chart types | Plotly, automatic type detection, column profiling, pandas queries |
| 🔑 [Keyword Density Checker](Keywords-Density-Checker-App) | Keyword and phrase frequency, density and target-keyword SEO check | Unicode tokenizer, n-grams, stopword filtering |
| 🎨 [Picture Editor](Picture-Editor-App) | Crop, resize, rotate, adjust and apply 12 filters with live preview | Pillow pipeline, alpha-channel preservation, EXIF orientation |
| 🔗 [URL Shortener](URL-Shortener-App) | Shortens links through 3 services and generates QR codes | Validation, provider abstraction, QR generation |
| ▶️ [YouTube Keyword Extractor](Youtube-Keyword-Extractor-App) | Reveals a video's hidden tags, stats and hashtags | Embedded-JSON extraction, 10 link formats, meta-tag fallback |

## Quick start
```bash
git clone https://github.com/FaizanSSDQ/AI-Web-Apps-Python-using-Streamlit.git
cd AI-Web-Apps-Python-using-Streamlit/Data-Visualization-App   # or any other app
pip install -r requirements.txt
streamlit run app.py
```

## Repository layout
```
<App-Name>/
├── app.py            # Streamlit UI only
├── <logic>.py        # UI-independent logic (transcriber, scraper, viz, density, editor, ...)
├── requirements.txt  # this app's dependencies
├── README.md
└── tests/            # unit tests + headless UI test (streamlit.testing.v1.AppTest)
```

## Quality
- **115 automated tests**: logic unit tests plus headless UI tests that run every app with
  Streamlit's `AppTest`. Network services are replaced with fakes, so tests are fast and reliable.
- **CI** on every push: `ruff` lint and format checks and the full test suite on Python 3.11 to 3.13.

```bash
pip install -r requirements-dev.txt
python -m pytest        # all apps
ruff check . && ruff format --check .
```

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

Licensed under the [MIT License](LICENSE).

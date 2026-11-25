# 🕸️ Web Data Scraper

A Streamlit app that extracts structured data from any public web page and exports it.

## Features
- **Page overview**: title, meta description, word / link / image / table counts
- **Text**: heading outline (H1 to H4) and clean readable text (scripts and styles removed), .txt export
- **Links**: absolute, de-duplicated, classified as *internal / external / email*, filterable, CSV export
- **Images**: gallery preview, lazy-loaded images supported (`data-src`), CSV of URLs,
  **one-click ZIP download** (up to 50 images)
- **Tables**: every HTML `<table>` converted to a DataFrame with per-table CSV export

## How it works
```
URL -> normalise & validate -> HTTP GET (browser user agent, timeout) -> BeautifulSoup + lxml
    -> metadata / headings / links / images  +  pandas.read_html for tables
```

## Run locally
```bash
cd Data-Scraper-App
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `scraper.py` | Fetching and parsing logic (UI-independent, unit-tested) |
| `tests/` | Offline unit tests on static HTML + headless UI test |

## Tests
```bash
pip install pytest
python -m pytest
```

## Responsible use
Only scrape pages you are allowed to. Respect `robots.txt`, rate limits and the website's terms.
JavaScript-rendered content is not executed: the app sees the page as the server delivers it.

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

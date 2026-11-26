# 🔑 Keyword Density Checker

An SEO and writing tool that measures how often words and phrases appear in a text.

## Features
- Three input sources: **paste text**, **upload .txt/.md**, or **fetch a web page** (visible text only)
- Text statistics: words, unique words, sentences, words per sentence, reading time
- Keyword frequency for **single words, 2-word and 3-word phrases**
- Built-in English **stopword filter** (phrases may not start or end with a stopword), minimum word
  length, top-N selection
- Sortable table with **density %**, horizontal bar chart, **CSV export**
- **Target keyword check**: occurrences, density and a verdict (not found / low / good / stuffing)
- Unicode-aware tokenizer that keeps contractions (`isn't`) and hyphenated terms (`low-power`) intact

## Density formula
```
density % = occurrences x words_in_phrase / total_words x 100
```

## Run locally
```bash
cd Keywords-Density-Checker-App
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `density.py` | Tokenizer, statistics, n-gram density, target keyword report |
| `tests/` | Unit tests + headless UI test |

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

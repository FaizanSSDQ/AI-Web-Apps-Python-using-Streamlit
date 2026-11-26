# 🎙️ Audio to Text Converter

A Streamlit app that turns speech recordings into editable, downloadable text.

## Features
- Upload **WAV, MP3, M4A, OGG, FLAC or WebM** audio
- **Silence-based segmentation**: long recordings are split at natural pauses, so each request stays short and accurate
- **7 languages** (English US/UK, Urdu, Arabic, German, French, Spanish)
- Optional **timestamps** per segment (`[00:12 - 00:19] ...`)
- Live **progress bar**, recognition statistics, editable transcript, **.txt download**
- Fully in-memory processing: no temporary files are written to disk

## How it works
```
upload -> decode (pydub/ffmpeg) -> detect non-silent regions -> pad & cap length (50 s)
       -> export each region as mono WAV in memory -> Google Web Speech API -> join text
```
Tune the segmentation in the sidebar: minimum pause length, silence threshold (dB below the clip's
average loudness) and padding around speech.

## Run locally
```bash
cd Audio-to-Text-Converter-App
pip install -r requirements.txt
streamlit run app.py
```
Non-WAV formats need [ffmpeg](https://ffmpeg.org/download.html) on your PATH
(`packages.txt` installs it automatically on Streamlit Community Cloud).

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `transcriber.py` | Segmentation and transcription logic (UI-independent, unit-tested) |
| `tests/` | Unit tests (fake recognizer, no network) + headless UI test |

## Tests
```bash
pip install pytest
python -m pytest
```

## Notes
- The free Google Web Speech API needs an internet connection and is intended for light use.
- Segments with no intelligible speech are skipped and counted in the statistics.

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

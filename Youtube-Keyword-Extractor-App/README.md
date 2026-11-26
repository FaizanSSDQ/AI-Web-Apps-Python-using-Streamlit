# ▶️ YouTube Keyword Extractor

Reveal the hidden tags of any public YouTube video, an everyday tool for creators and SEO work.

## Features
- Accepts **every common link form**: `watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`, `/live/`,
  mobile and YouTube Music links, or a bare 11-character video ID
- Extracts **tags**, title, channel, views, duration, category, publish date and description
- **Tag budget meter**: characters used out of YouTube's 500-character tag limit
- Tags shown as chips, as a copyable comma-separated list, and as a **CSV download**
- Lists **hashtags** found in the description
- Video thumbnail and "open on YouTube" button

## How it works
The public watch page embeds a JSON object, `ytInitialPlayerResponse`, which contains the video
details including the tags. The app decodes that JSON exactly (with `json.JSONDecoder.raw_decode`,
not a fragile regex) and falls back to the page's HTML `<meta>` tags if the JSON is unavailable.
A consent cookie skips the EU cookie wall, so it works from any region.

## Run locally
```bash
cd Youtube-Keyword-Extractor-App
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `youtube.py` | Video ID parsing, page fetching, metadata extraction |
| `tests/` | Offline tests (10 link formats, JSON and meta-tag parsing) + headless UI tests |

## Tests
```bash
pip install pytest
python -m pytest
```

## Notes
Only publicly visible data is read. Private, removed or age-restricted videos cannot be analysed.
YouTube may change its page structure; the parser is isolated in `youtube.py` to make updates easy.

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

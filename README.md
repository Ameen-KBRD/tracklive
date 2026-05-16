# 🎯 TrackLive

[![Version](https://img.shields.io/badge/version-1.3.1-blue.svg)](https://github.com/Ameen-KBRD/tracklive/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-yellow.svg)](https://python.org)
[![PHP](https://img.shields.io/badge/php-7.0+-purple.svg)](https://php.net)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey)]()

> **TrackLive** - A sophisticated real-time GPS location tracking tool with device fingerprinting, multiple notification methods, and beautiful templates.

<div align="center">
  <img src="https://img.shields.io/badge/status-active-success.svg">
  <img src="https://img.shields.io/badge/maintained-yes-success.svg">
  <img src="https://img.shields.io/github/stars/Ameen-KBRD/tracklive?style=social">
  <img src="https://img.shields.io/github/forks/Ameen-KBRD/tracklive?style=social">
</div>

---

## ⚠️ LEGAL NOTICE & DISCLAIMER

<div align="center">
  <strong>
    <p style="color: red; font-size: 1.2em;">
      🚨 READ THIS BEFORE USING 🚨
    </p>
  </strong>
</div>

**By downloading, installing, or using TrackLive, you explicitly agree to the following:**

### 📜 Legal Terms

1. **Educational Purpose Only**
   - This tool is developed STRICTLY for educational and security research purposes
   - It is designed to help security professionals understand location tracking vulnerabilities

2. **Consent Required**
   - You MUST obtain **explicit, written consent** from any individual before tracking
   - Tracking without consent is ILLEGAL in most jurisdictions
   - Unauthorized tracking may violate:
     - Computer Fraud and Abuse Act (CFAA)
     - GDPR (Europe)
     - Privacy Act (Various countries)
     - Stalking laws worldwide

3. **Prohibited Uses**
   The following uses are STRICTLY PROHIBITED:
   - ❌ Stalking or harassing individuals
   - ❌ Tracking without consent
   - ❌ Corporate espionage
   - ❌ Domestic surveillance
   - ❌ Any illegal activities
   - ❌ Monitoring employees without disclosure
   - ❌ Tracking minors (without parental consent)

4. **Liability Waiver**
   - The author (Ameen KBRD) assumes **ZERO LIABILITY** for misuse
   - Users are solely responsible for legal compliance
   - The author does not condone illegal activities

5. **Jurisdiction**
   - You are responsible for understanding your local laws
   - Some countries prohibit any form of location tracking
   - Ignorance of the law is not a defense


### ✅ Acceptable Use Examples

- Security research on your own devices
- Parental monitoring with child's consent
- Tracking company devices with employee consent
- Educational demonstrations in controlled environments
- Penetration testing with written authorization

### ❌ Unacceptable Use Examples

- Tracking an ex-partner without consent
- Monitoring employees secretly
- Spying on neighbors
- Any use without explicit permission

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Real-time GPS** | Live location tracking with accuracy, altitude, direction & speed |
| 📱 **Device Fingerprinting** | OS, CPU cores, RAM, GPU, browser & screen resolution |
| 🌍 **IP Geolocation** | City, region, country, ISP & organization details |
| 🤖 **Telegram Bot** | Instant notifications to your Telegram |
| 💬 **Discord Webhook** | Send data to Discord channels |
| 🌐 **Custom Webhook** | POST data to any endpoint |
| 📍 **KML Export** | Save locations for Google Earth |
| 🎨 **Multiple Templates** | 7+ UI templates for different scenarios |
| 🔄 **Live Updates** | Continuous tracking with timestamps |

---

## 📋 Requirements

- **Python** 3.6+
- **PHP** 7.0+
- **Internet Connection**
- **Ngrok** (optional, for external access)

---

## 🚀 Quick Installation

### Linux / macOS / Termux
```bash
git clone https://github.com/Ameen-KBRD/tracklive.git
cd tracklive
pip install -r requirements.txt
chmod +x tracklive.py
python3 tracklive.py

# ✝️ Daily Saint integration for Home Assistant

[![HACS Badge](https://img.shields.io/badge/Available%20in-HACS-41BDF5?logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pa-martin&repository=ha-dailysaint&category=integration)
[![Home Assistant](https://img.shields.io/badge/Home--Assistant-2026.7+-blue?logo=home-assistant)](https://www.home-assistant.io/blog/2026/07/01/release-20267/)

[![MIT License](https://img.shields.io/github/license/pa-martin/ha-dailysaint?label=License&logo=github)](https://github.com/pa-martin/ha-dailysaint/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/pa-martin/ha-dailysaint?label=Version&logo=github)](https://github.com/pa-martin/ha-dailysaint/releases)
[![Last Commit](https://img.shields.io/github/last-commit/pa-martin/ha-dailysaint?label=Last%20update&logo=github)](https://github.com/pa-martin/ha-dailysaint/commits/main)
[![GitHub Stars](https://img.shields.io/github/stars/pa-martin/ha-dailysaint?label=Stars&style=social)](https://github.com/pa-martin/ha-dailysaint/stargazers)
<br>

Get the saint of the day from one or more providers in Home Assistant.

This documentation is also available in:
- [French - Français](./README.fr.md)

---

## 📦 Installation

### 1. Via HACS (recommended)

> Requires HACS installed in Home Assistant

1. Open **HACS**
2. Search for **Daily Saint**
3. Install it, then restart Home Assistant

### 2. Manual (without HACS)

1. Download this repository
2. Copy the `dailysaint` folder into `config/custom_components/`
3. Restart Home Assistant

---

## ⚙️ Configuration

1. Go to **Settings → Devices & services → Add integration**
2. Search for **Daily Saint**
3. Select the providers you want to enable

This integration allows only **one configuration entry**.
You can update enabled providers later from the integration options.

---

## 🌐 Supported providers

- **Nominis** (`nominis.cef.fr`)
- **Fête du jour** (`fetedujour.fr`)

---

## 📊 Sensors created

One sensor is created per enabled provider.

Typical entity IDs:
- `sensor.nominis_saint_of_the_day`
- `sensor.fete_du_jour_saint_of_the_day`

Sensor state:
- **State**: saint name

Sensor attributes:
- `attribution`: provider label
- `provider`: provider key
- `description`: saint description (if available)
- `link`: provider link (if available)
- `day`, `month`, `year`: provider date fields (if available)

---

## 🛠 Development

Compatible with Home Assistant `2026.7+`.
See [DEV.md](./DEV.md) for local development details.

Structure:
- `translations/*.json`: integration translations
- `__init__.py`: integration setup / unload
- `api.py`: providers API client
- `config_flow.py`: UI configuration flow
- `const.py`: constants
- `coordinator.py`: polling and data refresh logic
- `manifest.json`: metadata and dependencies
- `sensor.py`: sensor entities

---

## 👨‍💻 Author

Developed by [pa-martin](https://github.com/pa-martin)
Contributions are welcome via **Pull Requests** and **Issues**.

---

## 📄 License

Open-source under the **MIT** license.

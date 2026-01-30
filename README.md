# GridFlow Solar ☀️⚡

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Frappe-7575FF.svg)
![Blockchain](https://img.shields.io/badge/Blockchain-Stellar-black.svg)
![Status](https://img.shields.io/badge/Status-Live_Pilot-success)

**GridFlow Solar** is a FOSS (Free and Open Source) decentralized energy operating system designed for African microgrids. We bridge the gap between physical solar infrastructure and global liquidity by combining the **Frappe Framework** with the **Stellar Blockchain**.

---

## 🌍 The Mission
GridFlow addresses the "Trust Gap" in African energy projects. By using IoT-verified data to trigger financial actions, we ensure that every watt generated is accounted for and every cent invested is protected.

* **Frappe Framework:** Powers our robust backend, device management (Digital Twin), and M-Pesa API integrations.
* **Stellar Network:** Handles the minting of on-chain Carbon Credits and performance-based escrow releases via smart contracts.
* **Open Source:** We believe energy transparency should be a public good.

---

## 🚀 Live Pilot Traction
We are currently managing a live pilot installation in Nairobi with the following verified metrics:
* **Energy Generated:** 9.5 MWh
* **Carbon Offset:** ~4.75 Metric Tonnes of CO2 avoided
* **Uptime:** 99.8% via GPRS-enabled SIM800L telemetry

---

## 🛠️ MVP Roadmap & Milestones

### ✅ Phase 1: Foundation (Completed)
* [x] **Frappe App Setup:** Created `gridflow` custom app with `GridFlow Device` and `Energy Log` DocTypes.
* [x] **Hardware Prototyping:** ESP32 integration with PZEM-004T sensors and SIM800L GPRS modules.
* [x] **Historical Data Backfill:** Successfully imported 9.5 MWh of legacy inverter data into the system.

### 🏗️ Phase 2: The Fintech Layer (In Progress)
* [ ] **M-Pesa C2B Integration:** Automated wallet top-ups using Safaricom's Daraja API linked to `phone_number`.
* [ ] **Stellar Asset Minting:** Automated Python scripts to mint Carbon Credit tokens based on verified kWh logs.
* [ ] **Pilot Site Retrofit:** Deploying GPRS units to provide real-time data sync to the Frappe backend.

### 🔭 Phase 3: Scaling & Governance (Q3 2026)
* [ ] **Decentralized Dashboard:** A Next.js frontend allowing donors to see real-time impact.
* [ ] **Soroban Smart Contracts:** Implementing performance-based escrow that releases funds only when energy is generated.
* [ ] **Community Nodes:** Allowing other solar providers to use the GridFlow stack.

---

## Contributing

GridFlow Solar is a FOSS project, and we welcome contributors from all backgrounds:

- Python / Frappe developers
- Stellar / Soroban blockchain engineers
- IoT & embedded systems builders (ESP32 / C++)

### Contribution Workflow

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. Push to your branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

---

## Installation (Developer Preview)

Full installation documentation coming soon.

### High-level setup

1. Install the Frappe Framework
2. Create a new Frappe site
3. Install the gridflow app
4. Configure IoT devices and API keys:
   - M-Pesa (Daraja API)
   - Stellar network credentials
5. Start telemetry ingestion

---

## License

Distributed under the MIT License.
See the LICENSE file for more information.

---

**Made in Kenya** 🇰🇪
**Samuel Ogera & Ryan Kinuthia**

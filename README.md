<h1 align="center">🛡️ Home SIEM Lab - Wazuh Detection & Response Project</h1>

<p align="center">
  <img src="https://img.shields.io/badge/SIEM-Wazuh%20v4.14-blue?style=for-the-badge&logo=linux" alt="Wazuh"/>
  <img src="https://img.shields.io/badge/OS-Ubuntu%20Server-orange?style=for-the-badge&logo=ubuntu" alt="Ubuntu"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Type-Portfolio%20Project-purple?style=for-the-badge" alt="Type"/>
  <img src="https://img.shields.io/badge/MITRE-ATT%26CK%20Mapped-red?style=for-the-badge" alt="MITRE"/>
</p>

<p align="center">
  A hands-on, home-built Security Information and Event Management (SIEM) lab demonstrating real-world SOC workflows - from infrastructure deployment to live attack simulation and automated incident response.
</p>

---

## 📖 Table of Contents

- [Project Summary](#-project-summary)
- [Lab Architecture](#️-lab-architecture)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [What Was Built](#-what-was-built)
- [Attack Simulations](#-attack-simulations)
- [SOAR - Automated Response](#-soar---automated-incident-response)
- [Custom Detection Rules](#-custom-detection-rules)
- [Screenshots](#-screenshots)
- [What I Learned](#-what-i-learned)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)

---

## 📌 Project Summary

This project builds a small, realistic **security monitoring lab** designed to simulate a Security Operations Center (SOC) environment using physical hardware and open-source tools. The goal is to:

- Deploy a fully operational SIEM platform on real hardware
- Monitor live endpoints and forward logs centrally
- Simulate realistic cyber attacks and validate detection capabilities
- Build and tune custom Wazuh detection rules
- Implement automated SOAR-style incident response

> This project is **100% free** and runs on consumer-grade hardware, demonstrating that effective security monitoring does not require expensive infrastructure.

---

## 🏗️ Lab Architecture

![Lab Architecture Diagram](./Infrastructure/Diagrams/DIAGRAM%20v2.png)

> **Log Flow:** `Activity on Endpoint` -> `Sysmon & Auditd capture logs` -> `Logs written to local log files` -> `Wazuh Agent reads & sends to Manager` -> `Wazuh Manager processes & applies rules` -> `Alerts generated in Dashboard`

---

## 🧰 Tech Stack

| Tool | Role |
|------|------|
| 🛡️ **Wazuh v4.14** | SIEM platform - log collection, alerting, dashboards |
| 🐧 **Ubuntu Server** | OS for SIEM host |
| 📡 **Wazuh Agent** | Endpoint telemetry forwarding |
| 🔬 **Sysmon for Linux** | Enhanced process and network telemetry |
| 📋 **Auditd** | Linux kernel-level syscall audit logging |
| 🌐 **Suricata** | Network IDS/IPS - detects Nmap scans and network threats |
| 🐉 **Kali Linux** | Attack simulation node (Hydra, Nmap) |
| 🐍 **Python** | SOAR automated response scripting |

---

## 📁 Repository Structure

```
📦 Home SIEM Lab
│
├── 📄 README.md                        # This file - project overview
├── 📄 AI-PROMPTS.md                    # AI prompts used during the project
├── 📄 License                          # Project license
├── 📄 .gitignore                       # Git ignore rules
│
├── 📂 Infrastructure/                  # Core SIEM setup & architecture
│   ├── 📄 PROJECT_OUTLINE.md           # Full project outline and build plan
│   ├── 📂 Diagrams/                    # Network and lab architecture diagrams
│   │   ├── 🖼️  DIAGRAM v1.png          # Initial architecture diagram
│   │   ├── 🖼️  DIAGRAM v2.png          # Updated architecture diagram
│   │   └── 🖼️  Attack Simulation 1.png # Attack simulation diagram
│   └── 📂 config/                      # Configuration files (reserved)
│
├── 📂 attack-simulations/              # All attack scenarios & detection work
│   ├── 📄 Rules.md                     # Custom Wazuh detection rule documentation
│   │
│   ├── 📂 SSH Attack/                  # Full SSH brute-force attack pipeline
│   │   ├── 📄 Outline.md               # Attack simulation plan & phase breakdown
│   │   ├── 📄 Full Attack Simulation Steps.md  # Step-by-step execution log
│   │   ├── 📄 What I did.md            # Detailed session journal (Jul 5-23, 2026)
│   │   ├── 📄 What I learned.md        # Key takeaways from this simulation
│   │   ├── 📄 SOAR Response Plan.md    # Automated response plan for Rule 100012
│   │   ├── 📄 Rule Outline.md          # Detection rule design notes
│   │   ├── 📄 Prompt.txt               # AI prompts used for this module
│   │   ├── 📄 ruletest.txt             # Rule testing notes
│   │   ├── 📂 Scripts/                 # SOAR response scripts
│   │   │   └── 📄 SSH SOAR response script.md  # Python/Bash remediation script doc
│   │   ├── 📂 Screenshots/             # Evidence of attack detection
│   │   ├── 📂 Video Demo/              # Attack simulation video recordings
│   │   └── 📂 DEMO edit/               # Edited demo footage
│   │
│   └── 📂 Linux Privilege Escalation Detection/  # Privilege escalation module
│       ├── 📄 README.md                # Module overview and achievements
│       ├── 📄 Outline.md               # Detection strategy and phase plan
│       ├── 📄 Next Steps.md            # Upcoming phases (SUID, chmod abuse)
│       ├── 📄 What I learned.md        # Technical takeaways
│       ├── 📄 Problems Encountered.md  # Issues encountered and resolved
│       ├── 📄 Prompt.txt               # AI prompts used for this module
│       ├── 🖼️  Attack Simulation 1.png # Simulation diagram
│       ├── 📂 Screenshots/             # Detection evidence (Wazuh alerts)
│       └── 📂 Video Demo/              # Module video demonstrations
│
├── 📂 docs/                            # Project-wide documentation
│   ├── 📄 PROGRESS.md                  # Chronological build log (May-Jul 2026)
│   ├── 📄 NEXT_STEPS.md                # Task tracker with completion status
│   ├── 📄 WHAT_I_LEARNED.md            # Skills and concepts gained
│   ├── 📄 PROJECT_LOGS.md              # High-level project log
│   └── 📄 SCREENSHOTS_CAPTURE.md      # Screenshot collection checklist
│
├── 📂 project-upgrades/                # Planned enhancements & future modules
│   ├── 📄 Attack_Simulations.md        # 12 planned high-impact SIEM additions
│   ├── 📄 Next Steps.md                # Upgrade roadmap
│   ├── 📄 Progress.md                  # Upgrade tracking log
│   ├── 📄 SCREENSHOTS_CAPTURE_UPGRADE.md  # Upgrade screenshot checklist
│   └── 📂 Upgrade Screenshots/         # Screenshots from upgrades
│
├── 📂 screenshots/                     # Infrastructure & setup screenshots
│   ├── 🖼️  Wazuh Dashboard.png
│   ├── 🖼️  Wazuh Dashboard Active.jpg
│   ├── 🖼️  Wazuh Login Page.png
│   ├── 🖼️  Wazuh Manager Active.png
│   ├── 🖼️  Wazuh Indexer Active.jpg
│   ├── 🖼️  Wazuh Agents Section.png
│   ├── 🖼️  Ubuntu Agent Logs.png
│   ├── 🖼️  Sysmon Running on endpoint.png
│   ├── 🖼️  auditd active on endpoint.png
│   ├── 🖼️  Server Host Information.png
│   ├── 🖼️  IP of Wazuh Server.png
│   ├── 🖼️  Endpoint Information.png
│   ├── 🖼️  Ubuntu_Laptop_Overview.png
│   ├── 🖼️  Available Storage on Server.jpg
│   ├── 🖼️  Ram on Server.jpg
│   └── 📄 README.md                    # Screenshot index & descriptions
│
└── 📂 videos/                          # Full project demo recordings
    └── 🎬 DEMO.mp4                     # Main SIEM lab demo video
```

---

## 🔨 What Was Built

### Phase 1 - Infrastructure Setup ✅

1. **Installed Ubuntu Server** on a physical desktop PC to serve as the centralized SIEM host
2. **Deployed Wazuh All-in-One** (Manager + Indexer + Dashboard) on the Ubuntu Server
3. **Configured the Wazuh Dashboard** and verified remote web access from the network
4. **Prepared the Ubuntu endpoint laptop** as the monitored client machine
5. **Installed and registered the Wazuh Agent** on the Ubuntu laptop endpoint
6. **Verified log ingestion** - confirmed the endpoint appeared active in the Wazuh dashboard

### Phase 2 - Endpoint Telemetry Enhancement ✅

7. **Installed Sysmon for Linux** via the Microsoft package repository for enhanced process and network telemetry
8. **Installed and configured Auditd** for kernel-level syscall monitoring
9. **Configured command logging** - solved archive configuration issues to surface commands like `whoami`, `ls`, etc. in the Wazuh dashboard
10. **Installed Suricata IDS** and configured it to detect Nmap port scans targeting SSH (port 22)

### Phase 3 - Attack Simulations & Detection ✅

> See [Attack Simulations](#-attack-simulations) section below.

---

## ⚔️ Attack Simulations

### 🔐 Simulation 1 - SSH Brute-Force Attack Pipeline

**Status:** ✅ Fully Simulated & Documented

**Objective:** Simulate a realistic multi-stage SSH attack and validate end-to-end detection in Wazuh.

| Phase | Description | Detection |
|-------|-------------|-----------|
| **Phase 1: Reconnaissance** | Nmap scan targeting port 22 from Kali Linux VM | Suricata rule triggers on SYN packets to port 22 |
| **Phase 2: Brute-Force** | Hydra SSH password guessing from Kali Linux | Wazuh detects multiple failed auth events from same IP |
| **Phase 3: Successful Login** | Login using compromised credentials | Wazuh correlates success after failure burst |
| **Phase 4: Persistence** | Attacker injects SSH key into `~/.ssh/authorized_keys` | Wazuh FIM + Auditd detect unauthorized file modification |
| **Phase 5: Lock Triggered** | Custom Rule 100012 fires on full attack chain | SOAR automated response executed |

**Key Technical Highlights:**
- Developed **Suricata custom rule** to detect Nmap scans, with false-positive suppression for the admin IP
- Identified and resolved Kali Linux **NAT vs Bridge mode** issue affecting rule triggering
- Configured Kali Linux VM in **Bridge mode** so it uses a unique IP on the network (critical for accurate detection)
- Built a **composite Wazuh detection rule** chaining brute-force + persistence detection into a single high-severity alert
- Implemented and debugged **SOAR automated response** - a Python script triggered by Wazuh active response

---

### 🔑 Simulation 2 - Linux Privilege Escalation Detection

**Status:** ✅ Phases 1–4 Complete | 🔄 Phases 5–6 In Progress

**Objective:** Validate Wazuh's ability to detect Linux privilege escalation techniques mapped to MITRE ATT&CK.

| Phase | Technique | Detection |
|-------|-----------|-----------|
| **Phase 1: Failed Sudo** | Password guessing against sudo | Custom Rule 100002 - 3 failures in 120 seconds |
| **Phase 2: Successful Sudo** | Monitoring legitimate privilege escalation | Wazuh Rule 5403 - sudo session detection |
| **Phase 3: Sudoers FIM** | Unauthorized `/etc/sudoers` modification | Wazuh FIM alert + Auditd syscall monitoring |
| **Phase 4: Persistence** | Adding a user account to the `sudo` group | Wazuh Rule 510 - user group modification alert |
| **Phase 5: SUID Binaries** | SUID binary creation | 🔄 In Progress |
| **Phase 6: Defense Evasion** | Suspicious `chmod`/`chown` abuse | 🔄 In Progress |

**MITRE ATT&CK Mapping:**
- `T1110` - Brute Force
- `T1548.003` - Abuse Elevation Control Mechanism: Sudo and Sudo Caching
- `T1078` - Valid Accounts
- `T1098` - Account Manipulation

---

## 🤖 SOAR - Automated Incident Response

When **Rule 100012** (Full SSH Attack Chain Detected) is triggered, a custom automated response executes the following containment actions:

| Step | Action | Target |
|------|--------|--------|
| 1️⃣ | **Clear SSH authorized keys** | `~/.ssh/authorized_keys` |
| 2️⃣ | **Reset the compromised user's password** | Affected account via `chpasswd` |
| 3️⃣ | **Block attacker IP with iptables** | All ports and protocols |
| 4️⃣ | **Terminate the attacker's active session** | Kill sessions by source IP |

**Implementation:** The response is a **Python script** (wrapped in a Bash active response handler) deployed at `/var/ossec/active-response/bin/soar-remediate-100012.py`, invoked by Wazuh's active response framework when the rule fires.

> 📄 Full details in [`attack-simulations/SSH Attack/SOAR Response Plan.md`](./attack-simulations/SSH%20Attack/SOAR%20Response%20Plan.md)

---

## 📏 Custom Detection Rules

| Rule ID | Name | Trigger | Severity |
|---------|------|---------|----------|
| `100002` | Sudo Password Guessing | 3× failed sudo in 120 seconds | `10` (Critical) |
| `100012` | Full SSH Attack Chain | Brute-force + successful login + key injection | High |
| Custom Suricata | Nmap SSH Port Scan | SYN packet to port 22 from non-admin IP | Alert |

---

## 📸 Screenshots

Screenshots are organized in the [`screenshots/`](./screenshots/) directory and cover:

- ✅ Wazuh Dashboard active and running
- ✅ Wazuh Manager, Indexer, and Dashboard service status
- ✅ Endpoint agent connected and active
- ✅ Sysmon running on Ubuntu endpoint
- ✅ Auditd active and logging
- ✅ Ubuntu Laptop overview and specs
- ✅ Server hardware specs and storage
- ✅ Log ingestion from endpoint visible in Wazuh

Attack simulation detection screenshots are located within each simulation's `Screenshots/` subfolder.

---

## 🧠 What I Learned

### 🔧 Technical Skills
- **Wazuh SIEM** - Full deployment, configuration, agent management, and custom rule authoring
- **Linux systemd / systemctl** - Managing, troubleshooting, and validating service states
- **Sysmon for Linux** - Installing via Microsoft package repos and configuring telemetry collection
- **Auditd** - Kernel-level syscall monitoring and log archiving to surface terminal commands
- **Suricata IDS** - Writing custom network detection rules and managing false positives with suppression lists
- **Wazuh FIM** - File Integrity Monitoring configuration for critical paths (`/etc/sudoers`, `~/.ssh/authorized_keys`)
- **SOAR Scripting** - Writing Python active response scripts integrated with Wazuh's active response framework
- **Networking (nmcli)** - Managing interfaces via CLI, debugging NAT vs Bridge mode in VM environments
- **SSH Key Authentication** - Generating keys with `ssh-keygen`, using `ssh-copy-id`, understanding `authorized_keys`

### 🔐 Security Concepts
- SIEM log pipeline: `Endpoint → Agent → Manager → Indexer → Dashboard`
- Correlation rules - chaining multiple events with `frequency`, `timeframe`, and `if_matched_sid`
- MITRE ATT&CK framework mapping for detection engineering
- False positive management and rule tuning in real environments
- PII awareness and handling sensitive data in logs

### 💼 Professional Development
- SOC-style structured documentation of lab activities
- GitHub project organization for security engineering portfolios
- Patience and systematic troubleshooting in complex multi-service environments


## 📊 Project Timeline

| Date | Milestone |
|------|-----------|
| May 2026 | Project initialized - GitHub structure, outline created |
| May 10, 2026 | Wazuh services verified; identified v4.7.5 -> v4.14 upgrade needed |
| May 11-12, 2026 | Wazuh upgraded and all services restored |
| May 12, 2026 | Ubuntu laptop endpoint connected and actively forwarding logs |
| May 14, 2026 | Sysmon for Linux installed; endpoint telemetry enabled |
| May 15, 2026 | Auditd installed and configured for command logging |
| May 17, 2026 | Diagrams refined; documentation polished |
| May 23, 2026 | Screenshots captured, PII removed, project made public |
| May 25, 2026 | Demo video recorded; uploaded to portfolio and LinkedIn |
| July 2-23, 2026 | SSH brute-force attack simulation built, tuned, and fully executed |
| July 2026 | Linux Privilege Escalation module - Phases 1-4 completed |
| July 22-23, 2026 | SOAR automated response built, debugged, and verified working |

---

## 📄 License

This project is licensed under the terms found in the [`License`](./License) file.

---

<p align="center">
  <em>Built as a hands-on cybersecurity portfolio project. Documenting the real process - including the failures, the troubleshooting, and the wins.</em>
</p>

<p align="center">
  <strong>📫 Documentation maintained by Zayan Parpia</strong>
</p>

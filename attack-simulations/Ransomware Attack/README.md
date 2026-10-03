# 🦠 Ransomware Attack Simulation

<p align="center">
  <img src="Ransomware Diagram.png" alt="Ransomware detection and response architecture" width="1000">
</p>

> Defensive ransomware simulation and detection-engineering lab using Wazuh SIEM, File Integrity Monitoring, and automated recovery.

![Platform](https://img.shields.io/badge/Platform-Wazuh%20SIEM-4C9AFF)
![Language](https://img.shields.io/badge/Language-Python-3776AB)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-T1486-red)
![Status](https://img.shields.io/badge/Status-Completed-success)
![Environment](https://img.shields.io/badge/Environment-Home%20Lab-orange)

---

## 📅 Project Summary

| Field | Details |
|---|---|
| **Date** | September 2026 |
| **Platform** | Wazuh SIEM |
| **Attack Type** | Ransomware / Mass Encryption |
| **MITRE ATT&CK** | `T1486 — Data Encrypted for Impact` |
| **Language** | Python |
| **Lab Type** | Home SIEM lab / isolated test environment |
| **Primary Goal** | Detect, correlate, and recover from simulated ransomware behavior |

---

## 🔍 Overview

This project simulates a ransomware attack against a monitored directory in a Wazuh environment. The attack does not rely on a real malware sample; instead, it recreates the observable behavior of ransomware on a Linux endpoint by recursively encrypting files and creating a ransom-style notice.

The purpose is to validate how a SIEM can detect malicious behavior based on correlation, not just single indicators. The simulation focuses on:

- rapid file modification
- same-process mass change behavior
- ransom note creation
- Wazuh rule correlation
- process-level alerting via audit data
- recovery from snapshot or backup storage

> This is a defensive, lab-based simulation intended for detection engineering and incident response practice.

---

## 🎯 Attack Flow

The simulation follows a realistic sequence:

```text
Victim endpoint
   ↓
Python ransomware script executes
   ↓
Files in target folders are encrypted in place
   ↓
Ransom note is created in affected directories
   ↓
Wazuh syscheck detects mass file changes
   ↓
Auditd captures the process and PID
   ↓
Custom rule correlates events
   ↓
Alert is generated in the Wazuh dashboard
   ↓
Recovery script restores files from backup
```

---

## 🧠 Detection Logic

The custom Wazuh rule logic is built around behavioral indicators rather than a static malware signature.

### Stage 1: Mass File Change Detection

A burst of file modifications from the same process in a short window is treated as suspicious activity. This is the first indication of possible mass encryption.

Example correlation logic:

- same `ppid`
- `10+` modified files
- within a short time window
- rule `550` as the base event

### Stage 2: Ransomware Correlation

The final alert is triggered when a mass-change event is followed by a ransom-style file creation or other suspicious file activity in the monitored directory.

This creates a stronger detection signal and reduces noise from routine file activity.

---

## 🛡️ Wazuh Rule Components

The project uses a custom rule set in `rules/Ransomwhere Attack.xml`.

Primary rules include:

| Rule ID | Description | Level |
|---|---|---:|
| `550` | File change event | baseline |
| `100234` | Possible mass encryption detected | `15` |
| `100235` | Ransomware detected | `16` |

A common rule pattern in this lab is:

```xml
<rule id="100234" level="15" frequency="10" timeframe="2">
  <if_matched_sid>550</if_matched_sid>
  <same_field>ppid</same_field>
  <description>Possible Mass Encryption Detected</description>
</rule>
```

This rule checks for multiple file-change events tied to the same process in a short time window. The second rule then correlates that activity with suspicious file creation and raises the ransomware alert.

---

## 🧪 Lab Architecture

The environment modeled in this project follows a simple but realistic detection pipeline:

```text
Attacker / Kali host
        ↓
Victim endpoint (Ubuntu)
        ↓
Python ransomware simulator
        ↓
Sysmon / auditd / FIM collection
        ↓
Wazuh Manager
        ↓
Indexer + Dashboard
        ↓
Alert / rule correlation / automated response
```

This matches the project goal of demonstrating how endpoint telemetry is turned into actionable detections and recovery workflows.

---

## 🔐 Tools & Technologies

| Component | Role |
|---|---|
| **Wazuh Manager** | Central SIEM, correlation, dashboards, active response |
| **Wazuh Agent** | Collects endpoint telemetry and forwards it to the manager |
| **Ubuntu endpoint** | Victim host used for the simulated ransomware activity |
| **Kali Linux** | Optional attacker host for delivery/execution testing |
| **auditd** | Captures process activity and file access behaviors |
| **File Integrity Monitoring** | Monitors changes to files and directories |
| **Python** | Simulates encryption and backup restore workflows |
| **cron + rsync** | Maintains backup snapshots for recovery |
| **MITRE ATT&CK** | Maps the activity to real-world ransomware behaviors |

---

## 📁 Folder Structure

```text
Ransomware Attack/
├── README.md
├── Outline.md
├── Techstack.md
├── What I did and next steps.md
├── Ransomware Diagram.png
├── rules/
│   └── Ransomwhere Attack.xml
├── scripts/
│   ├── Mock_data.py
│   ├── Ransomware Script.py
│   └── RestoreBackup.py
├── screenshots/
│   └── evidence and dashboard captures
├── Video/
│   └── demonstration footage
└── .vscode/
```

---

## 🚨 Response and Recovery Workflow

The malware simulation is not just about detection; it is tied to an operational recovery flow.

```text
Ransomware alert triggered
        ↓
Wazuh identifies malicious process and file activity
        ↓
Recovery script executes
        ↓
Files are restored from backup/snapshot
        ↓
System returns to a known-good state
```

This demonstrates the practical connection between SIEM detection and actual incident response, which is one of the primary goals of the project.

---

## 📸 Evidence Included

This project includes:

- dashboard screenshots of detection activity
- endpoint file-change evidence
- process and file modification events
- ransomware alert screenshots
- backup/restore workflow captures
- attack simulation and recovery footage

The visual evidence in the `screenshots/` folder shows the lifecycle from pre-attack state to encrypted files, detection alerts, and final restoration.

---

## 🧩 Project Purpose

This project is part of a broader home-lab SIEM practice environment and demonstrates how to:

- simulate realistic ransomware behavior safely
- monitor suspicious file activity in real time
- correlate events using Wazuh rules
- identify suspicious process behavior with audit data
- respond to malicious activity by restoring known-good files
- document findings in a portfolio-ready format

---

## 🏁 Conclusion

This ransomware simulation shows how endpoint telemetry, rule correlation, and recovery workflows can be combined into a practical defensive lab. Instead of relying on a single alert, the project emphasizes a layered detection model where rapid file changes, process context, and file creation behavior are combined into a stronger signal.

The lab demonstrates a realistic detection and response cycle:

> Attack simulation → suspicious file activity → Wazuh alerting → recovery workflow

This project is useful for both learning and portfolio documentation because it shows the full SOC workflow: detection, investigation, response, and containment in a home lab environment.

---

## 📎 Related Files

- `Outline.md` — project planning and attack phases
- `Techstack.md` — infrastructure and tool summary
- `What I did and next steps.md` — implementation update and next steps
- `rules/Ransomwhere Attack.xml` — custom detection rules
- `scripts/Ransomware Script.py` — simulated encryption behavior
- `scripts/RestoreBackup.py` — remediation and restore workflow

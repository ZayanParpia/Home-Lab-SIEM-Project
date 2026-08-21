# 🛡️ SIEM + SOAR SSH Attack Detection & Automated Response

A cybersecurity lab project demonstrating how **Wazuh SIEM**, **Suricata**, custom detection rules, and a **SOAR-style automated response** can work together to detect and respond to an SSH attack chain.

The simulation focuses on:

- SSH brute-force activity
- SSH reconnaissance against port 22
- Unauthorized SSH key persistence
- File Integrity Monitoring (FIM)
- Custom Wazuh and Suricata rules
- Automated incident response through Wazuh Active Response

---

## 📌 Project Overview

The goal of this project was to build and test an attack-detection pipeline where an attacker:

1. Performs SSH reconnaissance.
2. Attempts to brute-force SSH credentials.
3. Gains access to the target.
4. Adds an SSH public key to `~/.ssh/authorized_keys`.
5. Maintains access even if the account password is changed.
6. Triggers a custom Wazuh rule when the SSH key file is modified.
7. Automatically launches a SOAR-style remediation script.

The project was tested using a **Kali Linux attacker machine**, an **Ubuntu target endpoint**, and a **Wazuh SIEM environment**. The project documentation records the development, testing, troubleshooting, and final simulation. 

---

## 🏗️ Attack & Response Flow

![SOAR Response Diagram](SOAR%20RESPONSE%20DIAGRAM.png)

### High-Level Flow

```text
Attacker
   │
   ├── SSH Recon / Nmap
   │
   ├── SSH Brute Force
   │
   ├── Successful SSH Login
   │
   └── Add SSH Key
          │
          ▼
Target Endpoint
          │
          ▼
     Wazuh / Suricata
          │
          ├── Detect SSH activity
          ├── Detect port 22 reconnaissance
          └── Detect authorized_keys modification
                    │
                    ▼
             Custom Wazuh Rule
                Rule 100012
                    │
                    ▼
              SOAR Response
                    │
                    ▼
          Automated Remediation
```

The project specifically uses Wazuh FIM/Auditd monitoring for changes to `authorized_keys`, while Suricata is used to detect reconnaissance against SSH port 22. fileciteturn0file1L20-L25

---

# 📂 Project Structure

```text
.
├── SOAR RESPONSE DIAGRAM.png
│
├── rules/
│   ├── local_rules.xml
│   └── suricata-nmal.rules
│
├── Screenshots/
│   ├── Edited Ossec.conf so it tracks for new ssh keys.png
│   ├── Hydra Username List.png
│   ├── Hydra Password List.png
│   ├── key copy on target.png
│   ├── ssh authorized key file being changed detail.png
│   ├── Rule 100012 Triggerd.png
│   └── Nmap Scan port 22 Running on EndpointIV.png
│
└── Scripts/
    ├── soar-remediate-100012.py
    └── soar-remediate-100012
```

---

# 🔍 Detection Components

## Wazuh

Wazuh acts as the primary **SIEM and detection platform**.

It collects and analyzes security events from the target endpoint and evaluates them against custom rules.

The project uses Wazuh to monitor:

- SSH authentication activity
- SSH key changes
- File modifications
- Attack-related events
- Custom rule triggers

The project documentation specifically describes configuring Wazuh FIM to monitor:

```text
/home/*/.ssh/authorized_keys
/root/.ssh/authorized_keys
```

for modifications. fileciteturn0file1L37-L39

---

## Suricata

Suricata is used to detect **network-level reconnaissance against SSH**.

The custom Suricata rule detects traffic directed toward TCP port `22`:

```text
alert tcp any any -> any 22 (msg:"SIEM PROJECT: Nmap Scan to SSH Port 22"; flags:S; sid:1000002; rev:1;)
```

This allows the SIEM pipeline to identify reconnaissance targeting the SSH service.

During testing, a false positive was discovered because normal SSH connections could also trigger the detection. The rule was adjusted by suppressing the administrator's IP address. fileciteturn0file0L69-L95

---

# 🧩 Custom Rules

## `rules/local_rules.xml`

Contains the custom **Wazuh detection rules** created for this project.

One of the important rules is:

```text
Rule 100012
```

This rule is associated with the final attack stage and triggers the automated response when the suspicious SSH persistence activity is detected.

The project notes that the full attack pipeline eventually triggered rule `100012`, which was intended to initiate the lockdown/remediation response. fileciteturn0file0L95-L99

---

## `rules/suricata-nmal.rules`

Contains the custom Suricata rule used for **SSH reconnaissance detection**.

The rule is designed to alert when a scanner sends a TCP SYN toward port `22`.

This provides an early detection point before the later SSH authentication and persistence stages.

---

# ⚙️ SOAR Response

The automated response is split into two files.

## `Scripts/soar-remediate-100012.py`

This is the **Python SOAR remediation script**.

It is executed when the Wazuh rule triggers the active response.

During development, the script was changed to use non-interactive commands and proper subprocess handling so it could execute automatically without waiting for user input.

The documented changes included replacing interactive `passwd` behavior with `chpasswd`, passing the emergency password securely, redirecting command output, and explicitly terminating the script. fileciteturn0file0L137-L155

---

## `Scripts/soar-remediate-100012`

This is the **Bash/Wazuh Active Response wrapper**.

Its purpose is to receive the event from Wazuh and launch the Python remediation script.

The wrapper was refined to:

1. Read the JSON event from Wazuh.
2. Store the incoming payload.
3. Pass the payload to the Python script.
4. Run the Python process separately so Wazuh's execution queue does not become blocked.

These changes resolved an input starvation issue encountered during testing. fileciteturn0file0L163-L173

---

# 🖼️ Screenshots

## `Edited Ossec.conf so it tracks for new ssh keys.png`

Shows the modification of `ossec.conf` so Wazuh monitors:

```text
~/.ssh/authorized_keys
```

The purpose is to detect when an attacker adds or changes an SSH public key.

This is important because an attacker can use an authorized SSH key as a persistence mechanism. The project testing showed that changing the password alone did not remove access provided through the added SSH key. fileciteturn0file0L49-L53

---

## `Hydra Username List.png`

Shows the username list used during the SSH brute-force simulation.

---

## `Hydra Password List.png`

Shows the password list used during the SSH brute-force simulation.

The project documentation records the creation of username and password lists and testing Hydra against the endpoint. fileciteturn0file0L5-L11

---

## `key copy on target.png`

Shows the SSH public key being copied to the target system.

This represents the persistence stage of the attack.

---

## `ssh authorized key file being changed detail.png`

Shows the `~/.ssh/authorized_keys` file being modified.

This is the event that Wazuh is configured to monitor.

---

## `Rule 100012 Triggerd.png`

Shows the custom Wazuh rule being triggered.

The detection of the SSH key file modification causes the SOAR response to execute.

---

## `Nmap Scan port 22 Running on EndpointIV.png`

Shows an Nmap scan identifying SSH port `22` on the target endpoint.

This represents the reconnaissance stage of the simulation.

---

# 🔄 Attack Simulation

The complete simulation follows this general sequence:

### 1. Reconnaissance

The attacker scans the target and identifies SSH running on port `22`.

### 2. Brute Force

A username and password list are used to simulate repeated SSH authentication attempts.

The project documentation records a successful SSH brute-force attack and the resulting SIEM logs. fileciteturn0file0L5-L11

### 3. Initial Access

The attacker successfully authenticates to the target through SSH.

### 4. Persistence

The attacker adds an SSH public key to:

```text
~/.ssh/authorized_keys
```

This creates a persistent authentication method.

### 5. Detection

Wazuh detects the modification to the SSH authorized key file.

### 6. Automated Response

The custom Wazuh rule triggers:

```text
Rule 100012
```

which launches the Active Response wrapper and Python remediation script.

---

# 🧪 Testing & Troubleshooting

This project was developed through multiple rounds of testing.

Some of the issues discovered and fixed included:

- SSH key authentication initially not working as expected.
- Wazuh not detecting changes to `authorized_keys`.
- Suricata rules generating false positives.
- Network configuration affecting IP-based rule exclusions.
- Active Response scripts not triggering consistently.
- The Python response script hanging because of interactive commands.
- Wazuh's execution queue being affected by the response process.
- The response triggering from previous log events after the environment was reset.

The project eventually reached a working state, with the final simulation successfully triggering the response. fileciteturn0file0L115-L133

---

# 🎯 What This Project Demonstrates

This project demonstrates several real-world defensive security concepts:

- **SIEM monitoring**
- **Network intrusion detection**
- **SSH attack detection**
- **Brute-force detection**
- **File Integrity Monitoring**
- **Persistence detection**
- **Custom detection rules**
- **False-positive reduction**
- **Automated incident response**
- **SOAR concepts**
- **Wazuh Active Response**
- **Suricata integration**
- **Security event correlation**

The overall objective is not just to detect a single attack, but to demonstrate how multiple security controls can work together as an automated detection and response pipeline.

---

# 📚 Project Documentation

The project was developed through iterative testing and documentation. The development notes cover the progression from SSH brute-force detection, through SSH key persistence detection, Suricata integration, custom rule development, and finally the automated response implementation. 

---

# ⚠️ Disclaimer

This project is intended for **authorized cybersecurity research, education, and lab environments only**.

All attacks and automated responses should be performed against systems that you own or have explicit permission to test.

\# Tech Stack — Ransomware Detection \& Automated Response Project



\## Core Infrastructure

| Component | Role |

|---|---|

| Wazuh (Manager + Agent) | SIEM/XDR — FIM, log analysis, correlation rules, active response |

| Ubuntu Server 24.04 LTS | Victim host — runs Wazuh agent, target directory, backups |

| Kali Linux | Attacker host — delivers/executes the simulator, optional reverse shell |

| VMware (host-only/NAT network) | Virtualization/isolation for the lab |



\## Detection Layer

| Component | Role |

|---|---|

| Wazuh syscheck (FIM) | Real-time monitoring of the target directory for mass file changes |

| auditd | Linux audit subsystem — watches the target directory, captures `exe=` and PID of the process making changes |

| Wazuh local\_rules.xml | Custom correlation rule: mass FIM events + auditd exe/PID → high-severity alert |



\## Attack Simulation

| Component | Role |

|---|---|

| Python 3 + `cryptography` (Fernet) | Safe ransomware simulator — recursive file encryption + ransom note |

| Netcat / Metasploit (msfvenom) | Optional — reverse shell from Kali to execute the simulator remotely |

| Atomic Red Team | Optional — standardized technique tests to validate detections beyond the custom script |



\## Response / Recovery Layer

| Component | Role |

|---|---|

| Wazuh Active Response | Triggers the kill + delete + restore script on rule match |

| Bash script (active response) | Kills PID, deletes/quarantines offending exe, rsyncs snapshot back |

| cron + rsync | Scheduled snapshot backups of the target directory (`/backup/snapshots/<timestamp>/`) |



\## SOAR / Orchestration Layer

| Component | Role |

|---|---|

| Shuffle (self-hosted, free/open-source) or n8n | Receives Wazuh webhook, orchestrates notification/case creation |

| Slack or Email | Incident notification (process killed, file deleted, snapshot restored) |



\## Frameworks / References

| Component | Role |

|---|---|

| MITRE ATT\&CK | T1486 (Data Encrypted for Impact) primary mapping; T1059, T1490 as supporting techniques |

| Atomic Red Team | Technique-aligned test cases referenced for detection validation |



\## Documentation / Version Control

| Component | Role |

|---|---|

| Git / GitHub | Version control, portfolio repo, README, architecture diagram |


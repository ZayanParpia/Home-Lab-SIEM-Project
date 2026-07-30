Web Server Attack Detection (Atomic Red Team )
Host:


Apache or NGINX
simple vulnerable web apps in isolated lab containers


Detect:


- suspicious requests


- directory traversal attempts


SQL injection indicators


repeated 404 scanning


DDOS/DOS


unusual user agents


Zeek


Suricata


Wazuh rules


custom parsing
# Security Simulation Report: SSH Attack Detection Pipeline



\*\*Date:\*\* July 30, 2026

\*\*Target:\*\* TBD

\*\*Status:\*\* In Progress



\## 1. Overview



This simulation validates SIEM/Wazuh capability to detect and respond to attacks such as, SQL injections, DDOS attacks, and Repeated 404 scanning on a vulnerable web server.



\## 2. Infrastructure \& Scope



\- \*\*SIEM Infrastructure:\*\* Wazuh Manager \& Dashboard, Sysmon for Linux, Auditd, journald

\- \*\*Target:\*\* Vulnerable Server (TBD)

\- \*\*Attacker Node:\*\* Kali Linux VM acting as adversary \*\*



\## 3. Simulation Execution \& Results (Planned Outline)



This simulation validates SIEM/Wazuh capability to detect and respond to attacks against a vulnerable web server running Apache or NGINX. The objective is to demonstrate detection and correlation of \*\*web application attacks, network anomalies, and endpoint security events\*\* through centralized monitoring.



| Phase                                                          | Attack Simulation                                                                                                                                             | Target Log Source                                                | Detection / Rule Logic Blueprint                                                                                                                                         |

| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

| \*\*Phase 1: Reconnaissance \& Web Scanning\*\*                     | Attacker performs automated discovery against the vulnerable web application, including directory enumeration and repeated requests to non-existent resources | Apache/NGINX access logs, Zeek HTTP logs                         | Detect abnormal request frequency, repeated 404 responses, suspicious user agents, and scanning patterns from a single source IP                                         |

| \*\*Phase 2: SQL Injection Attempt\*\*                             | Attacker sends malicious SQL payloads through vulnerable application parameters to test database input validation                                             | Apache/NGINX access logs, application logs, Wazuh archives       | Detect SQL injection indicators such as suspicious query parameters, encoded payloads, database-related keywords, and abnormal request patterns using custom Wazuh rules |

| \*\*Phase 3: Directory Traversal Attempt\*\*                       | Attacker attempts unauthorized file access by manipulating URL paths to access restricted files or directories                                                | Apache/NGINX access logs, Wazuh agent logs                       | Alert on traversal indicators, encoded path manipulation, sensitive file access attempts, and repeated unauthorized requests                                             |

| \*\*Phase 4: Denial-of-Service (DoS/DDoS) Simulation\*\*           | Attacker generates excessive HTTP requests against the vulnerable web server to simulate service disruption behavior                                          | Apache/NGINX logs, Zeek connection logs, Suricata IDS alerts     | Detect abnormal traffic volume, request spikes, connection bursts, and repeated requests exceeding normal baseline behavior                                              |

| \*\*Phase 5: Post-Exploitation Activity \& Endpoint Correlation\*\* | Simulated attacker activity after successful exploitation, including suspicious commands, file changes, or abnormal processes on the web server               | Wazuh agent logs, Linux Auditd, Syslog                           | Correlate web attacks with endpoint activity, detecting suspicious processes, file modifications, privilege changes, and attacker behavior                               |

| \*\*Phase 6: Incident Investigation \& Response Validation\*\*      | Security analyst investigates generated alerts and reconstructs the attack timeline using collected telemetry                                                 | Wazuh Dashboard, OpenSearch, archived logs, Zeek/Suricata events | Validate SIEM visibility by correlating source IPs, timestamps, attack techniques, affected systems, and producing an incident response workflow                         |




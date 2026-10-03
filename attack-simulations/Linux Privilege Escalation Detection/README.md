# Linux Privilege Escalation Detection

This project documents a controlled security simulation used to evaluate how Wazuh detects privilege escalation and persistence activity on a Linux endpoint. The work combines endpoint telemetry, Wazuh alerting, Auditd, and file integrity monitoring (FIM).

---

## Project Overview

The simulation is organized into phases that exercise different sudo and privilege-related behaviors:

| Phase | Activity | Status | Detection approach |
| --- | --- | --- | --- |
| 1 | Failed sudo attempts | Verified | Custom Wazuh rule `100002` correlates three failed attempts within 300 seconds. |
| 2 | Successful sudo usage | Verified | Standard Wazuh alerts record successful sudo activity. |
| 3 | Sudoers file modification | Verified | Wazuh FIM reports changes to `/etc/sudoers`. |
| 4 | Sudo group persistence | Verified | Auditd records the group membership change. |
| 5-6 | SUID and permission-change testing | Planned | Additional attack vectors are documented for future testing. |

The project is a defensive validation exercise. Testing is performed against the lab's Ubuntu CLI endpoint, identified as Endpoint II.

---

## Detection Notes

- **Failed sudo attempts:** Rule `100002` uses the failed sudo event `5557` as its match condition, with a frequency of three events in a 300-second window.
- **Configuration integrity:** FIM provides visibility into changes to the sudoers configuration.
- **Persistence monitoring:** Auditd provides evidence of changes to sudo group membership.
- **Account behavior:** Adding an account to the `sudo` group can grant elevated access and may change which failed-sudo detections apply to that account.
- **ATT&CK context:** The simulation is organized around privilege escalation and persistence behaviors; consult the project outline for the documented scope and results.

---

## Lab Environment

- **SIEM:** Wazuh Manager and Dashboard
- **Endpoint monitoring:** Wazuh agent, Sysmon for Linux, and Auditd
- **Target:** Ubuntu CLI Endpoint II

---

## Project Files

- [Outline and simulation results](Outline.md)
- [Next steps](Next%20Steps.md)
- [Problems encountered](Problems%20Encountered.md)
- [What I learned](What%20I%20learned.md)
- [Screenshots](Screenshots/)
- [Video demo](Video%20Demo/)

---

## Status

Phases 1-4 are verified. SUID binary and permission-change testing remain planned follow-up work; the project notes track the remaining documentation and simulation tasks.

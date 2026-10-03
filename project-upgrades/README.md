# Upgrade Screenshot Index

This folder contains screenshots documenting the upgrades made to the SIEM lab environment, including endpoint validation, service health checks, and evidence of improved monitoring coverage.

---

## 1. Overview

The upgrade work focused on improving the lab environment by verifying that:

- all agents are connected and active
- Linux and Windows endpoints are reporting correctly
- core monitoring services remain online
- system configuration and network information are captured for documentation
- future attack simulations can be tested against a stronger baseline environment

---

## 2. Laboratory Upgrade Evidence

### `All Agents Active.png`

Shows all enrolled endpoints connected and active in the Wazuh dashboard.

### `SCREENSHOT_CAPTURE_UPGRADE`

This section acts as a checklist for documenting the upgrade work and ensuring that the most important evidence is captured for the project record.

---

## 3. Attack Simulation Roadmap

### `Attack_Simulations.md`

This file outlines future and planned attack simulations that will be used to validate the upgraded lab environment, including detection coverage, log quality, and alert generation.

---

## 4. Endpoint 2–4 (Linux Agents)

These screenshots document the validation of Linux endpoints after upgrades and monitoring changes.

- `auditd_status.png` — Shows the status of `auditd` and confirms audit logging is active.
- `hostnamectl.png` — Displays hostname and operating system information using `hostnamectl`.
- `ip_conf.png` — Shows the system network configuration (`ip addr` / `ipconfig` equivalent context).
- `sysmon_status.png` — Confirms Sysmon is running and collecting telemetry on the endpoint.
- `Wazuh-agent.status.png` — Confirms the Wazuh agent service is active and reporting to the manager.

---

## 5. Windows Endpoint

These screenshots document the validation of the Windows endpoint in the upgraded lab environment.

- `ipconfig.png` — Shows the Windows network configuration output.
- `sysmon_status.png` — Confirms Sysmon is running on Windows.
- `WazuhSvcStatus.png` — Shows the Wazuh agent service status on the Windows host.

---

## 6. Summary

These screenshots provide visual proof that the lab upgrades were implemented successfully and that the environment remains operational for future attack simulation and detection work.

The upgrade documentation is intended to support a clear evidence trail for:

- service validation
- agent connectivity
- monitoring health
- endpoint readiness
- future security testing
